class ThreatDetector:
    def __init__(self):
        self.model = GradientBoostingClassifier(
            n_estimators=100,
            learning_rate=0.1,
            max_depth=3,
            random_state=42
        )
        self.scaler = StandardScaler()

    def train(self, X_train, y_train):
        self.model.fit(X_train, y_train)

    def predict_threat(self, request):
        features = extract_features(request)
        processed_features = preprocess_features(pd.DataFrame([features]))
        return self.model.predict_proba(processed_features)[0][1]
