import numpy as np

MAJOR_PROFILE = [6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19, 2.39, 3.66, 2.29, 2.88]
MINOR_PROFILE = [6.33, 2.68, 3.52, 5.38, 2.60, 3.53, 2.54, 4.75, 3.98, 2.69, 3.34, 3.17]
CAMELOT_WHEEL = {
    '1A': 'B', '2A': 'F', '3A': 'C', '4A': 'G', '5A': 'D', '6A': 'A',
    '7A': 'E', '8A': 'B', '9A': 'F#', '10A': 'C#', '11A': 'G#', '12A': 'D#',
    '1B': 'G#', '2B': 'D#', '3B': 'A#', '4B': 'F', '5B': 'C', '6B': 'G',
    '7B': 'D', '8B': 'A', '9B': 'E', '10B': 'B', '11B': 'F#', '12B': 'C#'
}


def convert_to_camelot(chroma_mean):
    major_corrs = [np.correlate(chroma_mean, np.roll(MAJOR_PROFILE, i))[0] for i in range(12)]
    minor_corrs = [np.correlate(chroma_mean, np.roll(MINOR_PROFILE, i))[0] for i in range(12)]

    if np.max(major_corrs) > np.max(minor_corrs):
        key = (np.argmax(major_corrs), 'major')
    else:
        key = (np.argmax(minor_corrs), 'minor')

    key_map = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    note, mode = key
    base_note = key_map[note]

    for camelot, note_val in CAMELOT_WHEEL.items():
        if note_val == base_note and camelot.endswith('A' if mode == 'minor' else 'B'):
            return key, camelot
    return key, None