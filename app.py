from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/water-level', methods=['POST'])
def water_level():
    data = request.json
    water_level = data.get("water_level", 0)

    if water_level > 350:  # Проверяем превышение порога
        print(f" Пора выключать! Уровень воды: {water_level}")

    return jsonify({"status": "ok"}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5055)
