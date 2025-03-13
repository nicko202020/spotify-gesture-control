import cv2
import mediapipe as mp
import math
import time
import numpy as np

class GestureControl:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils
        self.hands = self.mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
        self.current_volume = 0  # Placeholder for volume
        self.last_gesture = None
        self.last_volume = None  # To track the last volume level

    def find_distance(self, p1, p2, lmList):
        """
        Calculate the distance between two points given their landmark IDs.
        """
        x1, y1 = lmList[p1][1], lmList[p1][2]
        x2, y2 = lmList[p2][1], lmList[p2][2]
        length = math.hypot(x2 - x1, y2 - y1)
        return length

    def fingers_up(self, lmList):
        """
        Returns a list indicating which fingers are up (1) or down (0).
        """
        fingers = []
        # Thumb
        if lmList[4][1] > lmList[3][1]:  # Thumb is up if it's to the right of the thumb CMC
            fingers.append(1)
        else:
            fingers.append(0)
        # Other fingers
        for id in range(8, 21, 4):  # Check tips of the index, middle, ring, and pinky
            if lmList[id][2] < lmList[id - 2][2]:  # Finger is up if tip is above PIP joint
                fingers.append(1)
            else:
                fingers.append(0)
        return fingers

    def recognize_gesture(self, lmList):
        """
        Recognize gestures based on the hand landmarks list (lmList).
        """
        fingers = self.fingers_up(lmList)

        # Peace sign (only index and middle fingers up)
        if fingers == [0, 1, 1, 0, 0]:
            return "play_pause"

        # Volume control gesture (thumb and index finger distance)
        if fingers == [1, 1, 0, 0, 0]:  # Thumb and index finger up, others down
            return "adjust_volume"

        return None

    def process_frame(self, frame, spotify_control):
        imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(imgRGB)
        lmList = []
        gesture = None
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                self.mp_drawing.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
                for id, lm in enumerate(hand_landmarks.landmark):
                    h, w, c = frame.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    lmList.append([id, cx, cy])

                if lmList:
                    detected_gesture = self.recognize_gesture(lmList)

                    if detected_gesture == "adjust_volume":
                        length = self.find_distance(4, 8, lmList)
                        self.current_volume = np.interp(length, [50, 200], [0, 100])
                        self.current_volume = max(0, min(100, self.current_volume))  # Clamp between 0 and 100

                        # Send the volume command only if it's significantly different from the last volume
                        if self.last_volume is None or abs(self.current_volume - self.last_volume) >= 1:
                            spotify_control.adjust_volume(self.current_volume)
                            self.last_volume = self.current_volume

                    # Prevent sending the same command repeatedly
                    if detected_gesture != self.last_gesture:
                        gesture = detected_gesture
                        self.last_gesture = detected_gesture

        return gesture, frame