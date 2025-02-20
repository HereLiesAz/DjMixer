from itertools import combinations
from sklearn.metrics.pairwise import cosine_similarity
from analyzer.transition_suggester import TransitionSuggester
from utils.user_preferences import UserPreferences


class MixAnalyzer:
    def __init__(self, song_files):
        self.songs = [SongAnalyzer(f) for f in song_files]
        [song.analyze() for song in self.songs]
        self.transition_suggester = TransitionSuggester()
        self.user_prefs = UserPreferences()

    def _camelot_compatibility(self, a, b):
        a_num = int(a.camelot[:-1])
        a_type = a.camelot[-1]
        b_num = int(b.camelot[:-1])
        b_type = b.camelot[-1]

        if a.camelot == b.camelot: return 100
        if a_type == b_type and abs(a_num - b_num) in [1, 11]: return 80
        if a_type != b_type and a_num == b_num: return 60
        return 0

    def analyze_matches(self):
        results = []
        for (a, b) in combinations(self.songs, 2):
            if abs(a.tempo - b.tempo) > self.user_prefs.get_preference('bpm_tolerance'):
                continue

            camelot_match = self._camelot_compatibility(a, b)
            tempo_diff = abs(a.tempo - b.tempo)
            energy_diff = abs(a.energy - b.energy)
            atmosphere_sim = cosine_similarity([a.vggish_features], [b.vggish_features])[0][0] * 100

            weights = {
                'harmonic': 0.3,
                'tempo': 0.25,
                'energy': 0.2,
                'atmosphere': 0.25
            }

            overall = (
                    camelot_match * weights['harmonic'] +
                    (100 - tempo_diff) * weights['tempo'] +
                    (100 - energy_diff * 10) * weights['energy'] +
                    atmosphere_sim * weights['atmosphere']
            )

            if overall >= 60:
                transition_suggestions = self.transition_suggester.suggest_transitions(
                    a.genre, {'tempo_diff': tempo_diff, 'camelot_match': camelot_match}
                )
                results.append({
                    'tracks': (a, b),
                    'camelot_match': camelot_match,
                    'tempo_diff': tempo_diff,
                    'energy_diff': energy_diff,
                    'atmosphere_sim': atmosphere_sim,
                    'overall': overall,
                    'transition_suggestions': transition_suggestions
                })
        return sorted(results, key=lambda x: x['overall'], reverse=True)