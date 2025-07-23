from sklearn.ensemble import IsolationForest

class ThreatDetector:
    def __init__(self):
        self.model = IsolationForest(contamination=0.1)
        self.is_fitted = False

    def train(self, X_train):
        self.model.fit(X_train)
        self.is_fitted = True

    def detect(self, flow_stats):
        if not self.is_fitted:
            # Handle the case where the model is not trained yet
            return {'threat': 'None', 'confidence': 1.0, 'reason': 'Model not trained'}

        # We need to reshape the data to be a 2D array
        X = [[flow_stats['packets'], flow_stats['bytes']]]
        prediction = self.model.predict(X)
        if prediction[0] == -1:
            return {'threat': 'DDoS', 'confidence': 0.9}
        else:
            return {'threat': 'None', 'confidence': 1.0}
