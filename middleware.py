import copy

from flask import request
from datetime import datetime
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
        log_data = request_log_manager.get_all()

        # Check if is classified already
        manual_classification = self.get_classification(req_data)

        # Block if marked as unsafe
        if manual_classification is not None and not manual_classification:
            return {"error": "Request blocked (manually classified as unsafe)"}, 403

        # Check with AI
        # Every request will be checked against AI
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
            "timestamp": datetime.now().isoformat(),
            "path": request.path,
            "method": request.method,
            "headers": dict(request.headers),
            "ip": request.remote_addr,
            "body": request.get_json(silent=True) or request.form.to_dict()
        }
        
        return request_log_manager.save(request_log)
    
    def get_classification(self, req_data):
        classifications = classification_manager.get_all()

        # No classifications exists yet
        if len(classifications) == 0: return None

        for classification in classifications:
            local_classification = copy.deepcopy(classification["request"])
            local_req = copy.deepcopy(req_data)

            del local_classification["timestamp"]
            del local_req["timestamp"]

            if local_classification == local_req:
                return local_classification["is_safe"]
        
        return None

    
