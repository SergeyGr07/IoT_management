from flask import Flask, request, jsonify
import time
import os
from prometheus_client import Counter, Gauge, generate_latest, REGISTRY

app = Flask(__name__)

# Метрики Prometheus
ESP_UPTIME = Gauge('esp_uptime_seconds', 'ESP32 uptime in seconds')
ESP_FREE_HEAP = Gauge('esp_free_heap_bytes', 'ESP32 free heap memory in bytes')
ESP_WIFI_RSSI = Gauge('esp_wifi_rssi_dbm', 'ESP32 WiFi RSSI in dBm')
WATER_LEVEL = Gauge('water_level', 'Water level value')
REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP Requests', ['method', 'endpoint', 'status'])


@app.route('/metrics', methods=['GET'])
def metrics():
    """
    Эндпоинт для Prometheus метрик.
    
    Returns:
        Метрики в формате Prometheus
    """
    return generate_latest(REGISTRY), 200, {'Content-Type': 'text/plain'}


@app.route('/health', methods=['GET'])
def health_check():
    """
    Эндпоинт проверки работоспособности сервиса.

    Returns:
        JSON с статусом сервиса
    """
    REQUEST_COUNT.labels(method='GET', endpoint='/health', status=200).inc()
    return jsonify({"status": "healthy"}), 200


@app.route('/esp-metrics', methods=['POST'])
def esp_metrics():
    """
    Обработка метрик от ESP устройства.
    
    Ожидаемый формат JSON:
    {
        "uptime": 3600,
        "free_heap": 180000,
        "wifi_rssi": -55
    }
    
    Returns:
        JSON с статусом выполнения запроса
    """
    if not request.is_json:
        REQUEST_COUNT.labels(method='POST', endpoint='/esp-metrics', status=400).inc()
        return jsonify({"error": "Отсутствуют данные JSON"}), 400

    try:
        data = request.get_json(silent=True)
        if data is None or data == {}:
            REQUEST_COUNT.labels(method='POST', endpoint='/esp-metrics', status=400).inc()
            return jsonify({"error": "Отсутствуют данные JSON"}), 400

        # Проверка и обновление метрик
        if "uptime" in data:
            try:
                uptime = float(data["uptime"])
                ESP_UPTIME.set(uptime)
            except (ValueError, TypeError):
                pass
                
        if "free_heap" in data:
            try:
                free_heap = float(data["free_heap"])
                ESP_FREE_HEAP.set(free_heap)
            except (ValueError, TypeError):
                pass
                
        if "wifi_rssi" in data:
            try:
                wifi_rssi = float(data["wifi_rssi"])
                ESP_WIFI_RSSI.set(wifi_rssi)
            except (ValueError, TypeError):
                pass

        REQUEST_COUNT.labels(method='POST', endpoint='/esp-metrics', status=200).inc()
        return jsonify({"status": "ok"}), 200

    except Exception as e:
        print(f"Ошибка при обработке метрик ESP: {str(e)}")
        REQUEST_COUNT.labels(method='POST', endpoint='/esp-metrics', status=500).inc()
        return jsonify({"error": "Внутренняя ошибка сервера"}), 500


@app.route('/water-level', methods=['POST'])
def water_level():
    """
    Обработка POST-запроса с данными об уровне воды.

    Ожидаемый формат JSON:
    {
        "water_level": 450
    }

    Returns:
        JSON с статусом выполнения запроса
    """
    if not request.is_json:
        REQUEST_COUNT.labels(method='POST', endpoint='/water-level', status=400).inc()
        return jsonify({"error": "Отсутствуют данные JSON"}), 400

    try:
        data = request.get_json(silent=True)
        if data is None or data == {}:
            REQUEST_COUNT.labels(method='POST', endpoint='/water-level', status=400).inc()
            return jsonify({"error": "Отсутствуют данные JSON"}), 400

        if "water_level" not in data:
            REQUEST_COUNT.labels(method='POST', endpoint='/water-level', status=400).inc()
            return jsonify({"error": "Отсутствует параметр 'water_level'"}), 400

        try:
            water_level_value = float(data["water_level"])
            WATER_LEVEL.set(water_level_value)
        except (ValueError, TypeError):
            REQUEST_COUNT.labels(method='POST', endpoint='/water-level', status=400).inc()
            return jsonify({"error": "Параметр 'water_level' должен быть числом"}), 400

        if water_level_value > 350:
            print(f" Пора выключать! Уровень воды: {water_level_value}")

        REQUEST_COUNT.labels(method='POST', endpoint='/water-level', status=200).inc()
        return jsonify({"status": "ok"}), 200

    except Exception as e:
        print(f"Ошибка при обработке запроса: {str(e)}")
        REQUEST_COUNT.labels(method='POST', endpoint='/water-level', status=500).inc()
        return jsonify({"error": "Внутренняя ошибка сервера"}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5055)
