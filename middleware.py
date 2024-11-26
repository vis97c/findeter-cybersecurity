from flask import request
from utils.storage import RequestsStorageManager, ClassificationsStorageManager
from validator import analyze_request


CONFIDENCE_THRESHOLD = 0.6

# GET LOGS
request_log_manager = RequestsStorageManager()
classification_manager = ClassificationsStorageManager()

class Middleware:
    def __init__(self, app):
        self.app = app
        self.app.before_request(self.before_request)

    def before_request(self):
        req_data = self.log_request() # Always log current request
        log_data = request_log_manager.get_all

        # Check if is classified already
        manual_classification = self.classify_request(req_data)

        if manual_classification is not None:
            if manual_classification: return # Already classified as safe
            else: return {"error": "Request blocked (manually classified as unsafe)"}, 403

        # Unclassified, use IA
        analysis = analyze_request(req_data, log_data)

        if analysis["confidence"] < CONFIDENCE_THRESHOLD:
            # Require manual clasificacion
            classification_manager.save({
                "request": req_data,
                "is_safe": None
            })

            return {
                "error": "Request blocked",
                "confidence": analysis["confidence"],
                "required_threshold": CONFIDENCE_THRESHOLD,
                "frequency": analysis["frequency"]
            }, 403

    def log_request(self):
        # Log current request
        request_log = {
            "timestamp": request.headers.get("Date", "Unknown"),
            "path": request.path,
            "method": request.method,
            "headers": dict(request.headers),
            "ip": request.remote_addr,
            "body": request.get_json(silent=True) or request.form.to_dict()
        }
        
        return self.log_manager.save(request_log)
    
    def classify_request(req_data):
        classifications = classification_manager.get_all

        for classification in classifications:
            if classification["request"] == req_data:
                return classification["is_safe"]
        return None

    
