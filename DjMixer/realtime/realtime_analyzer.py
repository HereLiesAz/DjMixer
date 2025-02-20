import sounddevice as sd
import numpy as np
import librosa
from analyzer.song_analyzer import SongAnalyzer
from analyzer.mix_analyzer import MixAnalyzer


class RealTimeAnalyzer:
    def __init__(self, sample_rate=44100, block_size=1024):
        self.sample_rate = sample_rate
        self.block_size = block_size
        self.buffer = np.array([])
        self.current_track = None
        self.mix_analyzer = MixAnalyzer([])

    def start_monitoring(self):
        def callback(indata, frames, time, status):
            self.buffer = np.append(self.buffer, indata[:, 0])
            if len(self.buffer) >= self.sample_rate * 10:  # Analyze every 10 seconds
                self._analyze_buffer()
                self.buffer = np.array([])

        with sd.InputStream(callback=callback,
                            samplerate=self.sample_rate,
                            channels=1,
                            blocksize=self.block_size):
            print("=== Real-Time Analysis Started ===")
            while True: pass

    def _analyze_buffer(self):
        temp_file = "temp_buffer.wav"
        librosa.output.write_wav(temp_file, self.buffer, self.sample_rate)
        current_analysis = SongAnalyzer(temp_file)
        current_analysis.analyze()

        if self.current_track:
            match = self.mix_analyzer.analyze_matches([self.current_track, current_analysis])[0]
            self._display_real_time_feedback(match)

        self.current_track = current_analysis

    def _display_real_time_feedback(self, match):
        print("\n=== Real-Time Mix Feedback ===")
        print(f"Tempo Match: {100 - match['tempo_diff']}%")
        print(f"Key Match: {match['camelot_match']}%")
        print(f"Recommended Effects: {', '.join(match['transition_suggestions']['effects'])}")
        print("=============================\n")