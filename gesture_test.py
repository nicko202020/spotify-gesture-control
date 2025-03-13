import cv2
from gesture_control import GestureControl
from spotify_control import SpotifyControl  # Ensure this import is correct

def test_gesture_recognition():
    # Initialize the gesture control and spotify control instances
    gesture_control = GestureControl()
    spotify_control = SpotifyControl(client_id='your_client_id', 
                                     client_secret='your_client_secret', 
                                     redirect_uri='your_redirect_uri')
    
    cap = cv2.VideoCapture(0)  # Use the correct camera index

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        gesture, frame = gesture_control.process_frame(frame, spotify_control)  # Pass spotify_control as well

        # Display the recognized gesture on the frame
        if gesture:
            cv2.putText(frame, f"Gesture: {gesture}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
            print(f"Recognized Gesture: {gesture}")

        cv2.imshow('Gesture Recognition Test', frame)

        # Press 'Esc' to exit the test
        if cv2.waitKey(5) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    test_gesture_recognition()