import ipaddress
from sklearn.preprocessing import StandardScaler
import pandas as pd
import random

# Simulación de procesamiento de IA
def analyze_request(request_data, log_data):
    request_data = preprocess_features(request_data)

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

def extract_features(request_data):
    base_url, query_string = request_data.path.split("?", 1)

    return {
        # Características temporales
        'hour_of_day': request_data.timestamp.hour,
        'day_of_week': request_data.timestamp.weekday(),


        # Características de red
        'source_ip': request_data.ip,
        'url_length': len(base_url),
        'query_length': len(query_string),
    }

def preprocess_features(request_data):
    features_df = pd.DataFrame(request_data)

    # Codificación de IPs
    features_df['ip_risk_score'] = encode_ip_risk(features_df['ip'])

    # Codificación de métodos HTTP
    method_encoded = pd.get_dummies(features_df['method'])

    # Normalización de características numéricas
    scaler = StandardScaler()
    numeric_features = ['url_length', 'query_length']
    features_df[numeric_features] = scaler.fit_transform(features_df[numeric_features])

    return request_data

def encode_ip_risk(ip):
    try:
        ip_obj = ipaddress.ip_address(ip)

        if ip_obj.is_private:
            risk_score = 0.1  # Las direcciones IP privadas tienen un riesgo bajo
        elif ip_obj.is_global:
            if ip_obj.version == 4:
                # Para direcciones IPv4 públicas, asigna un riesgo basado en el bloque de IP
                if ip_obj in ipaddress.IPv4Network('1.0.0.0/8'):
                    risk_score = 0.3
                elif ip_obj in ipaddress.IPv4Network('2.0.0.0/8'):
                    risk_score = 0.4
                elif ip_obj in ipaddress.IPv4Network('5.0.0.0/8'):
                    risk_score = 0.5
                else:
                    risk_score = 0.6
            else:
                # Para direcciones IPv6 públicas, asigna un riesgo basado en el prefijo
                if ip_obj in ipaddress.IPv6Network('2000::/3'):
                    risk_score = 0.4
                elif ip_obj in ipaddress.IPv6Network('3000::/4'):
                    risk_score = 0.5
                else:
                    risk_score = 0.6
        else:
            risk_score = 0.8  # Otros tipos de direcciones IP tienen un riesgo alto
    except ValueError:
        risk_score = 1.0  # Direcciones IP inválidas tienen el riesgo más alto

    return (risk_score)

