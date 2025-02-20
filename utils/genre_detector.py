import numpy as np
from sklearn.neighbors import KNeighborsClassifier

class GenreDetector:
    def __init__(self):
        self.genres = ['house', 'techno', 'drum_and_bass', 'dubstep', 'trance']
        self._train_dummy_model()

    def _train_dummy_model(self):
        # Replace with actual trained model in production
        X = np.random.rand(100, 128)  # Mock VGGish features
        y = np.random.choice(self.genres, 100)
        self.model = KNeighborsClassifier(n_neighbors=3)
        self.model.fit(X, y)

    def detect_genre(self, features):
        return self.model.predict([features])[0]