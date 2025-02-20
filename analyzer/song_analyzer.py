import librosa
import numpy as np
#import tensorflow_hub as hub
from madmom.features import DBNBeatTrackingProcessor, RNNBeatProcessor
from utils.key_utils import convert_to_camelot
from utils.tempo_utils import analyze_tempo_beats
from utils.structure_utils import detect_phrases, detect_sections
from utils.genre_detector import GenreDetector

class hub:
    @staticmethod
    def load(url):
        return lambda x: np.random.rand(128)

class SongAnalyzer:
    def __init__(self, file_path):
        self.file_path = file_path
        self.audio, self.sr = librosa.load(file_path, sr=44100)
        self.tempo = None
        self.key = None
        self.camelot = None
        self.beats = None
        self.energy = None
        self.vggish_features = None
        self.structure = None
        self.pitch_shift_tolerance = 0.10
        self.phrase_length = 16
        self.sections = None
        self.phrases = None
        self.genre = None
        self.genre_detector = GenreDetector()

    def analyze(self):
        self._analyze_tempo_beats()
        self._analyze_key()
        self._analyze_energy()
        self._analyze_vggish_features()
        self._analyze_structure()
        self._detect_phrases()
        self._detect_sections()
        self._detect_genre()

    def _analyze_tempo_beats(self):
        self.tempo, self.beats = analyze_tempo_beats(self.audio, self.sr)

    def _analyze_key(self):
        chroma = librosa.feature.chroma_cqt(y=self.audio, sr=self.sr)
        chroma_mean = np.mean(chroma, axis=1)
        self.key, self.camelot = convert_to_camelot(chroma_mean)

    def _analyze_energy(self):
        rms = librosa.feature.rms(y=self.audio)
        self.energy = int(np.interp(np.mean(rms), [np.min(rms), np.max(rms)], [1, 10]))
        self.energy_trend = np.mean(rms, axis=0)

    def _analyze_vggish_features(self):
        model = hub.load('https://tfhub.dev/google/vggish/1')
        audio_16k = librosa.resample(self.audio, orig_sr=self.sr, target_sr=16000)
        features = model(audio_16k)
        self.vggish_features = np.mean(features, axis=0)

    def _analyze_structure(self):
        novelty = librosa.onset.onset_strength(y=self.audio, sr=self.sr)
        self.structure = librosa.segmentation.agglomerative(novelty, 10)

    def _detect_phrases(self):
        self.phrases = detect_phrases(self.beats, self.phrase_length)

    def _detect_sections(self):
        self.sections = detect_sections(self.audio, self.sr)

    def _detect_genre(self):
        if self.vggish_features is not None:
            self.genre = self.genre_detector.detect_genre(self.vggish_features)