import json
from app import app


def test_health_check():
    """Тестирование эндпоинта проверки работоспособности сервиса"""
    with app.test_client() as client:
        response = client.get('/health')
        assert response.status_code == 200
        assert response.json == {"status": "healthy"}


def test_metrics_endpoint():
    """Тестирование эндпоинта Prometheus метрик"""
    with app.test_client() as client:
        response = client.get('/metrics')
        assert response.status_code == 200
        assert 'text/plain' in response.content_type


def test_water_level_endpoint():
    """Тестирование эндпоинта /water-level с корректными данными"""
    with app.test_client() as client:
        response = client.post(
            '/water-level',
            data=json.dumps({'water_level': 450}),
            content_type='application/json'
        )
        assert response.status_code == 200
        assert response.json == {"status": "ok"}


def test_water_level_validation():
    """Тестирование обработки уровня воды выше критического значения"""
    with app.test_client() as client:
        response = client.post(
            '/water-level',
            data=json.dumps({'water_level': 360}),
            content_type='application/json'
        )
        assert response.status_code == 200


def test_missing_json_data():
    """Тестирование обработки запроса без JSON данных"""
    with app.test_client() as client:
        # Тест с пустым телом запроса
        response = client.post(
            '/water-level',
            data='',
            content_type='application/json'
        )
        assert response.status_code == 400
        assert "Отсутствуют данные JSON" in response.json["error"]

        # Тест с пустым JSON объектом
        response = client.post(
            '/water-level',
            data=json.dumps({}),
            content_type='application/json'
        )
        assert response.status_code == 400
        assert "Отсутствуют данные JSON" in response.json["error"]

        # Тест с неверным content-type
        response = client.post(
            '/water-level',
            data='not-json',
            content_type='text/plain'
        )
        assert response.status_code == 400
        assert "Отсутствуют данные JSON" in response.json["error"]


def test_missing_water_level():
    """Тестирование обработки запроса без параметра water_level"""
    with app.test_client() as client:
        response = client.post(
            '/water-level',
            data=json.dumps({"some_other_field": "value"}),
            content_type='application/json'
        )
        assert response.status_code == 400
        assert "Отсутствует параметр 'water_level'" in response.json["error"]


def test_invalid_water_level():
    """Тестирование обработки некорректного значения water_level"""
    with app.test_client() as client:
        response = client.post(
            '/water-level',
            data=json.dumps({'water_level': "не число"}),
            content_type='application/json'
        )
        assert response.status_code == 400
        assert "должен быть числом" in response.json["error"]


def test_float_water_level():
    """Тестирование обработки дробного значения water_level"""
    with app.test_client() as client:
        response = client.post(
            '/water-level',
            data=json.dumps({'water_level': 450.5}),
            content_type='application/json'
        )
        assert response.status_code == 200
        assert response.json == {"status": "ok"}


def test_esp_metrics_endpoint():
    """Тестирование эндпоинта /esp-metrics с корректными данными"""
    with app.test_client() as client:
        response = client.post(
            '/esp-metrics',
            data=json.dumps({
                'uptime': 3600,
                'free_heap': 180000,
                'wifi_rssi': -55
            }),
            content_type='application/json'
        )
        assert response.status_code == 200
        assert response.json == {"status": "ok"}


def test_esp_metrics_partial_data():
    """Тестирование эндпоинта /esp-metrics с частичными данными"""
    with app.test_client() as client:
        response = client.post(
            '/esp-metrics',
            data=json.dumps({
                'uptime': 3600
            }),
            content_type='application/json'
        )
        assert response.status_code == 200
        assert response.json == {"status": "ok"}


def test_esp_metrics_invalid_data():
    """Тестирование эндпоинта /esp-metrics с некорректными данными"""
    with app.test_client() as client:
        response = client.post(
            '/esp-metrics',
            data=json.dumps({
                'uptime': "не число",
                'free_heap': "не число",
                'wifi_rssi': "не число"
            }),
            content_type='application/json'
        )
        assert response.status_code == 200  # Должен вернуть 200, так как мы обрабатываем ошибки внутри
        assert response.json == {"status": "ok"}
