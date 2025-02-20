import networkx as nx
import matplotlib.pyplot as plt
from itertools import permutations


class MultiTrackMixer:
    def __init__(self, tracks):
        self.tracks = tracks
        self.graph = nx.DiGraph()
        self._build_compatibility_graph()

    def _build_compatibility_graph(self):
        for i, track_a in enumerate(self.tracks):
            for j, track_b in enumerate(self.tracks):
                if i != j:
                    compatibility = self._calculate_pair_compatibility(track_a, track_b)
                    self.graph.add_edge(i, j, weight=compatibility)

    def _calculate_pair_compatibility(self, a, b):
        tempo_diff = abs(a.tempo - b.tempo)
        key_match = 1 if abs(a.key[0] - b.key[0]) in [0, 1, 11] else 0
        energy_diff = abs(a.energy - b.energy) / 10
        return 0.4 * (100 - tempo_diff) + 0.3 * key_match * 100 + 0.3 * (100 - energy_diff * 10)

    def find_optimal_sequence(self):
        try:
            return nx.approximation.traveling_salesman_problem(self.graph, cycle=False)
        except nx.NetworkXError:
            return []

    def visualize_mix_graph(self):
        pos = nx.spring_layout(self.graph)
        edge_labels = {(i, j): f"{self.graph[i][j]['weight']:.1f}"
                       for i, j in self.graph.edges()}

        plt.figure(figsize=(12, 8))
        nx.draw(self.graph, pos, with_labels=True, node_size=2000, node_color='skyblue')
        nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=edge_labels)
        plt.title("Track Compatibility Graph")
        plt.show()

    def generate_mix_report(self, sequence):
        report = []
        for i in range(len(sequence) - 1):
            current = sequence[i]
            next_track = sequence[i + 1]
            edge_data = self.graph[current][next_track]

            report.append({
                'from_track': current,
                'to_track': next_track,
                'compatibility_score': edge_data['weight'],
                'recommended_transition_point': self._find_best_transition_point(
                    self.tracks[current], self.tracks[next_track]
                )
            })
        return report

    def _find_best_transition_point(self, a, b):
        a_phrase_end = a.phrases[-1][-1] if a.phrases else a.beats[-1]
        b_phrase_start = b.phrases[0][0] if b.phrases else b.beats[0]
        return (a_phrase_end, b_phrase_start)