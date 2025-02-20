from sklearn.neighbors import NearestNeighbors
import numpy as np

class TrackRecommender:
    def __init__(self):
        self.model = NearestNeighbors(n_neighbors=5, metric='cosine')
        self.tracks = []
        self.features = []

    def add_track(self, track, features):
        self.tracks.append(track)
        self.features.append(features)

    def train_model(self):
        self.model.fit(np.array(self.features))

    def recommend_tracks(self, track_index, n=3):
        distances, indices = self.model.kneighbors([self.features[track_index]], n_neighbors=n+1)
        return [self.tracks[i] for i in indices[0][1:]]  # Exclude the input track