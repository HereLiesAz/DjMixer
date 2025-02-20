import numpy as np
import soundfile as sf


class MixExporter:
    def export_mix(self, tracks, transitions, output_file='mix_output.wav'):
        mix_audio = np.array([])

        for i, track in enumerate(tracks):
            mix_audio = np.append(mix_audio, track.audio)

            if i < len(transitions):
                transition = transitions[i]
                mix_audio = self._apply_transition(mix_audio, track, transitions[i])

        sf.write(output_file, mix_audio, tracks[0].sr)
        print(f"Mix exported to {output_file}.")

    def _apply_transition(self, mix_audio, track, transition):
        fade_out = np.linspace(1, 0, len(track.audio[-transition['fade_samples']:]))
        fade_in = np.linspace(0, 1, len(track.audio[:transition['fade_samples']]))

        mix_audio[-transition['fade_samples']:] *= fade_out
        mix_audio = np.append(mix_audio, track.audio[:transition['fade_samples']] * fade_in)
        return mix_audio