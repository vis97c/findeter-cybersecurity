import json

CLASSIFICATIONS_LOG = "logs/classifications.json"

def load_classifications():
    try:
        with open(CLASSIFICATIONS_LOG, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_classification(classification):
    classifications = load_classifications()
    classifications.append(classification)
    with open(CLASSIFICATIONS_LOG, "w") as f:
        json.dump(classifications, f)

def classify_request(request_data, is_safe):
    classification = {
        "request": request_data,
        "is_safe": is_safe
    }
    save_classification(classification)

# Ejemplo de uso manual
if __name__ == "__main__":
    example_request = {
        "path": "/example",
        "method": "GET",
        "headers": {"Content-Type": "application/json"},
        "ip": "192.168.1.1",
        "body": {"key": "value"}
    }
    classify_request(example_request, False)  # Clasificar como insegura
    classify_request(example_request, True)   # Clasificar como segura
