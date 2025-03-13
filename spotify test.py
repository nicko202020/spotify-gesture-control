import spotipy
from spotipy.oauth2 import SpotifyOAuth
import time

# Spotify credentials
SPOTIPY_CLIENT_ID = ''
SPOTIPY_CLIENT_SECRET = ''
SPOTIPY_REDIRECT_URI = 'http://localhost:8888/callback'

# Spotify authentication
scope = "user-modify-playback-state user-read-playback-state playlist-modify-public playlist-modify-private"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                                               client_secret=SPOTIPY_CLIENT_SECRET,
                                               redirect_uri=SPOTIPY_REDIRECT_URI,
                                               scope=scope))

# Test Spotify functions
def test_spotify_functions():
    # Play/Pause
    print("Toggling play/pause...")
    playback = sp.current_playback()
    if playback and playback['is_playing']:
        sp.pause_playback()
        print("Paused playback.")
    else:
        sp.start_playback()
        print("Started playback.")

    # Next Track
    input("Press Enter to skip to the next track...")
    sp.next_track()
    print("Skipped to the next track.")

    # Previous Track
    input("Press Enter to go back to the previous track...")
    sp.previous_track()
    print("Went back to the previous track.")

    # Add to Playlist
    input("Press Enter to add the current track to a playlist...")
    playback = sp.current_playback()
    if playback and playback['is_playing']:
        track_id = playback['item']['id']
        playlist_id = '3ffNlYMlObBwkmKyaqixUE'  # Replace with your actual playlist ID
        sp.playlist_add_items(playlist_id, [track_id])
        print(f"Added track {track_id} to playlist {playlist_id}.")
    else:
        print("No track is currently playing.")

    # Scrub to Positions (15 sections of 3 seconds each)
    input("Press Enter to start scrubbing...")
    playback = sp.current_playback()
    if playback and playback['is_playing']:
        duration_ms = playback['item']['duration_ms']
        section_duration_ms = 3000  # 3 seconds in milliseconds
        num_sections = 15
        total_scrub_time = section_duration_ms * num_sections

        for i in range(num_sections):
            position_ms = i * section_duration_ms
            if position_ms < duration_ms:
                sp.seek_track(position_ms)
                print(f"Scrubbed to {position_ms} ms in the current track.")
                time.sleep(section_duration_ms / 1000)  # Wait for 3 seconds
            else:
                print("End of track reached.")
                break
    else:
        print("No track is currently playing.")

if __name__ == "__main__":
    test_spotify_functions()
