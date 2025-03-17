import json
from app import app


def test_water_level_endpoint():
    with app.test_client() as client:
        response = client.post('/water-level',
                             data=json.dumps({'water_level': 450}),
                             content_type='application/json')
        assert response.status_code == 200
        assert response.json == {"status": "ok"}


def test_water_level_validation():
    with app.test_client() as client:
        response = client.post('/water-level',
                             data=json.dumps({'water_level': 360}),
                             content_type='application/json')
        assert response.status_code == 200
