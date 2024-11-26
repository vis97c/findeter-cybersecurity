import random

# Simulación de procesamiento de IA
def analyze_request(request_data, log_data):
    # Aquí iría la lógica para comunicarte con el modelo IA
    # Simulamos una decisión con un porcentaje de seguridad
    similarity_score = random.uniform(0, 1)  # Ejemplo de similitud
    frequency = len(log_data)  # Ejemplo basado en frecuencia
    decision = {
        "is_safe": similarity_score > 0.5,
        "confidence": similarity_score * 100,
        "frequency": frequency,
    }
    return decision
