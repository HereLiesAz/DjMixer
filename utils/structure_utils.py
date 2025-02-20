import librosa
import numpy as np


def detect_phrases(beats, phrase_length):
    beats_per_phrase = phrase_length * 4
    return [beats[i:i + beats_per_phrase] for i in range(0, len(beats), beats_per_phrase)]


def detect_sections(audio, sr):
    novelty = librosa.onset.onset_strength(y=audio, sr=sr)
    frames = librosa.util.frame(novelty, frame_length=2048, hop_length=512)
    section_boundaries = librosa.segmentation.agglomerative(frames, 10)
    return _label_sections(section_boundaries, audio, sr)


def _label_sections(boundaries, audio, sr):
    sections = []
    for i, boundary in enumerate(boundaries):
        start = boundary[0] * 512 / sr
        end = boundary[1] * 512 / sr
        section_audio = audio[int(start * sr):int(end * sr)]

        energy = np.mean(librosa.feature.rms(y=section_audio))
        novelty = np.mean(librosa.onset.onset_strength(y=section_audio, sr=sr))

        if i == 0:
            label = 'intro'
        elif i == len(boundaries) - 1:
            label = 'outro'
        elif energy < 0.1 and novelty < 0.1:
            label = 'breakdown'
        elif energy > 0.5 and novelty > 0.5:
            label = 'chorus'
        else:
            label = 'verse'

        sections.append((label, (start, end)))
    return sections