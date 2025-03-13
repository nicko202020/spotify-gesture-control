import spotipy
from spotipy.oauth2 import SpotifyOAuth

class SpotifyControl:
    def __init__(self, client_id, client_secret, redirect_uri):
        scope = "user-modify-playback-state user-read-playback-state"
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                                            client_secret=client_secret,
                                                            redirect_uri=redirect_uri,
                                                            scope=scope))

    def play_pause(self):
        playback = self.sp.current_playback()
        if playback and playback['is_playing']:
            self.sp.pause_playback()
        else:
            self.sp.start_playback()

    def adjust_volume(self, volume_percent):
        """
        Adjust the volume for the current Spotify playback.
        :param volume_percent: Volume percentage (0 to 1).
        """
        volume = int(volume_percent * 100)  # Convert to Spotify's volume scale (0 to 100)
        self.sp.volume(volume)

    def next_track(self):
        self.sp.next_track()

    def previous_track(self):
        self.sp.previous_track()

    def add_to_playlist(self, track_id, playlist_id):
        self.sp.playlist_add_items(playlist_id, [track_id])

    def scrub_to_position(self, position_fraction):
        playback = self.sp.current_playback()
        if playback and playback['is_playing']:
            duration_ms = playback['item']['duration_ms']
            position_ms = int(duration_ms * position_fraction)
            self.sp.seek_track(position_ms)

    def adjust_volume(self, volume_percent):
        """
        Adjust the volume for the current Spotify playback.
        :param volume_percent: Volume percentage (0 to 1).
        """
        volume = int(volume_percent * 100)  # Convert to Spotify's volume scale (0 to 100) and ensure it's an integer
        self.sp.volume(volume)
