from sklearn.ensemble import RandomForestRegressor
import numpy as np

class CrowdEnergyPredictor:
    def __init__(self):
        self.model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.track_features = []
        self.energy_labels = []

    def train(self, historical_data):
        """
        Train the crowd energy prediction model.

        Args:
            historical_data (list): A list of dictionaries containing:
                - 'features': List of track features (e.g., VGGish embeddings)
                - 'energy': Crowd energy level (1-10)
        """
        self.track_features = [data['features'] for data in historical_data]
        self.energy_labels = [data['energy'] for data in historical_data]
        self.model.fit(self.track_features, self.energy_labels)

    def predict_energy(self, track_features):
        """
        Predict crowd energy for a single track.

        Args:
            track_features (list): List of features for the track.

        Returns:
            float: Predicted energy level (1-10).
        """
        return self.model.predict([track_features])[0]

    def predict_sequence_energy(self, sequence_features):
        """
        Predict crowd energy for a sequence of tracks.

        Args:
            sequence_features (list): List of track features for the sequence.

        Returns:
            list: Predicted energy levels for each track.
        """
        return [self.predict_energy(features) for features in sequence_features]

    def save_model(self, file_path='crowd_energy_model.pkl'):
        """
        Save the trained model to a file.
        """
        import joblib
        joblib.dump(self.model, file_path)
        print(f"Model saved to {file_path}.")

    def load_model(self, file_path='crowd_energy_model.pkl'):
        """
        Load a trained model from a file.
        """
        import joblib
        self.model = joblib.load(file_path)
        print(f"Model loaded from {file_path}.")