import json
from app import app


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
        response = client.post(
            '/water-level',
            data='',
            content_type='application/json'
        )
        assert response.status_code == 400
        assert "Отсутствуют данные JSON" in response.json["error"]


def test_missing_water_level():
    """Тестирование обработки запроса без параметра water_level"""
    with app.test_client() as client:
        response = client.post(
            '/water-level',
            data=json.dumps({}),
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
