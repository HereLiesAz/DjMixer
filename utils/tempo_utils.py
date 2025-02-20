from madmom.features import DBNBeatTrackingProcessor, RNNBeatProcessor

def analyze_tempo_beats(audio, sr):
    proc = DBNBeatTrackingProcessor(fps=100)
    act = RNNBeatProcessor()(audio)
    beats = proc(act)
    tempo = librosa.beat.tempo(onset_envelope=act, sr=sr)[0]
    return tempo, beats