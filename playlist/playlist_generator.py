import json

class PlaylistGenerator:
    def __init__(self):
        self.playlist = []

    def add_track(self, track, bpm, key, energy):
        """
        Add a track to the playlist.
        """
        self.playlist.append({
            'track': track,
            'bpm': bpm,
            'key': key,
            'energy': energy
        })

    def generate_playlist(self, filename='playlist.json'):
        """
        Generate a playlist file.
        """
        with open(filename, 'w') as f:
            json.dump(self.playlist, f, indent=4)
        print(f"Playlist saved to {filename}.")

    def load_playlist(self, filename='playlist.json'):
        """
        Load a playlist from a file.
        """
        with open(filename, 'r') as f:
            self.playlist = json.load(f)
        print(f"Playlist loaded from {filename}.")