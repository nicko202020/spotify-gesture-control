import cv2
from spotify_control import SpotifyControl
from gesture_control import GestureControl
import time
in
SPOTIPY_CLIENT_ID = ''
SPOTIPY_CLIENT_SECRET = ''
SPOTIPY_REDIRECT_URI = 'http://localhost:8888/callback'

# Initiinalize Spotify and Gesture control objects
spotify_control = SpotifyControl(SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI)
gesture_control = GestureControl()

cap = cv2.VideoCapture(0)

# Variables to manage cooldowns and debouncing
last_command_time = 0
command_cooldown = 2  # seconds

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    gesture, frame = gesture_control.process_frame(frame, spotify_control)

    current_time = time.time()
    if gesture and current_time - last_command_time > command_cooldown:
        if gesture == "play_pause":
            spotify_control.play_pause()
        elif gesture == "add_to_playlist":
            playback = spotify_control.sp.current_playback()
            if playback and playback['is_playing']:
                track_id = playback['item']['id']
                playlist_id = 'your_playlist_id'
                spotify_control.add_to_playlist(track_id, playlist_id)

        last_command_time = current_time

    cv2.imshow('Spotify Gesture Control', frame)
    if cv2.waitKey(5) & 0xFF == 27:  # Press 'Esc' to exit
        break

cap.release()
cv2.destroyAllWindows()
