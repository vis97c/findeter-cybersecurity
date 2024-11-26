import json
from datetime import datetime
from flask import request
from ia_tasks import analyze_request

REQUEST_LOG = "logs/requests_log.json"
CLASSIFICATIONS_LOG = "logs/classifications.json"
CONFIDENCE_THRESHOLD = 0.6  # Umbral de confianza

def load_logs(filepath):
    try:
        with open(filepath, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_log(filepath, data):
    logs = load_logs(filepath)
    logs.append(data)
    with open(filepath, "w") as f:
        json.dump(logs, f)

def log_request():
    return {
        "timestamp": datetime.utcnow().isoformat(),
        "path": request.path,
        "method": request.method,
        "headers": dict(request.headers),
        "ip": request.remote_addr,
        "body": request.get_json(silent=True)
    }

def classify_request(req_data, classifications):
    """Determina si una solicitud coincide con una clasificación previa."""
    for classification in classifications:
        if classification["request"] == req_data:
            return classification["is_safe"]
    return None

def middleware(app):
    @app.before_request
    def before_request():
        req_data = log_request()
        log_data = load_logs(REQUEST_LOG)
        classifications = load_logs(CLASSIFICATIONS_LOG)

        # Verificar si la solicitud ya está clasificada
        manual_classification = classify_request(req_data, classifications)

        if manual_classification is not None:
            if manual_classification:
                save_log(REQUEST_LOG, req_data)  # Registrar como segura
                return
            else:
                return {"error": "Request blocked (manually classified as unsafe)"}, 403

        # Solicitudes no clasificadas: usar IA
        analysis = analyze_request(req_data, log_data)
        save_log(REQUEST_LOG, req_data)

        if analysis["confidence"] < CONFIDENCE_THRESHOLD:
            return {
                "error": "Request blocked",
                "confidence": analysis["confidence"],
                "required_threshold": CONFIDENCE_THRESHOLD,
                "frequency": analysis["frequency"]
            }, 403
