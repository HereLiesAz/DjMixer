class TransitionSuggester:
    def __init__(self):
        self.genre_transitions = {
            'house': {
                'effects': ['filter', 'echo', 'loop'],
                'energy_tips': {0: 'Maintain groove', 2: 'Build energy'}
            },
            'techno': {
                'effects': ['hardcut', 'reverb', 'stutter'],
                'energy_tips': {0: 'Keep driving', 2: 'Add layers'}
            }
        }

    def suggest_transitions(self, genre, analysis):
        base = self.genre_transitions.get(genre.lower(), {})
        return {
            'effects': base.get('effects', ['crossfade']),
            'energy_tip': base.get('energy_tips', {}).get(
                analysis.get('energy_diff', 0) // 2, 'Use default transition')
        }