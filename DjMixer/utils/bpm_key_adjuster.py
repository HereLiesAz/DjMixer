import librosa
import numpy as np

class BPMKeyAdjuster:
    def __init__(self):
        self.bpm_tolerance = 5  # Max BPM difference for auto-adjustment
        self.key_tolerance = 1  # Max key difference for auto-adjustment

    def adjust_sequence(self, tracks, sequence):
        """
        Adjust BPM and key for a sequence of tracks.
        """
        adjusted_tracks = []
        for i in range(len(sequence) - 1):
            current = tracks[sequence[i]]
            next_track = tracks[sequence[i + 1]]

            # Adjust BPM if needed
            if abs(current.tempo - next_track.tempo) > self.bpm_tolerance:
                next_track = self._adjust_bpm(current, next_track)

            # Adjust key if needed
            if abs(current.key[0] - next_track.key[0]) > self.key_tolerance:
                next_track = self._adjust_key(current, next_track)

            adjusted_tracks.append(next_track)
        return adjusted_tracks

    def _adjust_bpm(self, current, next_track):
        """
        Adjust BPM of next_track to match current.
        """
        stretch_factor = current.tempo / next_track.tempo
        next_track.audio = librosa.effects.time_stretch(next_track.audio, stretch_factor)
        next_track.tempo = current.tempo
        print(f"Adjusted BPM of {next_track.file_path} to {current.tempo}.")
        return next_track

    def _adjust_key(self, current, next_track):
        """
        Adjust key of next_track to match current.
        """
        key_diff = current.key[0] - next_track.key[0]
        next_track.audio = librosa.effects.pitch_shift(next_track.audio, next_track.sr, n_steps=key_diff)
        next_track.key = current.key
        print(f"Adjusted key of {next_track.file_path} to {current.key}.")
        return next_track