
import os
from sklearn.ensemble import IsolationForest
from loguru import logger
from dotenv import load_dotenv

load_dotenv()

class ThreatDetector:
    def __init__(self):
        contamination = float(os.getenv('THREAT_MODEL_CONTAMINATION', '0.1'))
        self.model = IsolationForest(contamination=contamination)
        self.is_fitted = False
        logger.info(f"ThreatDetector initialized with contamination={contamination}")

    def train(self, X_train):
        try:
            self.model.fit(X_train)
            self.is_fitted = True
            logger.info("ThreatDetector model trained successfully.")
        except Exception as e:
            logger.exception(f"Error training ThreatDetector: {e}")
            self.is_fitted = False

    def detect(self, flow_stats):
        if not self.is_fitted:
            logger.warning("ThreatDetector model not trained.")
            return {'threat': 'None', 'confidence': 1.0, 'reason': 'Model not trained'}

        try:
            X = [[flow_stats['packets'], flow_stats['bytes']]]
            prediction = self.model.predict(X)
            if prediction[0] == -1:
                logger.info(f"Threat detected: {flow_stats}")
                return {'threat': 'DDoS', 'confidence': 0.9}
            else:
                return {'threat': 'None', 'confidence': 1.0}
        except Exception as e:
            logger.exception(f"Error in threat detection: {e}")
            return {'threat': 'error', 'confidence': 0.0, 'reason': str(e)}
