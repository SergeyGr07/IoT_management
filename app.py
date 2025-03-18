from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/health', methods=['GET'])
def health_check():
    """
    Эндпоинт проверки работоспособности сервиса.

    Returns:
        JSON с статусом сервиса
    """
    return jsonify({"status": "healthy"}), 200


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
    # Проверка на наличие JSON данных
    if not request.is_json:
        return jsonify({"error": "Отсутствуют данные JSON"}), 400
        
    # Проверка на пустые данные
    try:
        data = request.get_json(silent=True)
        if data is None or data == {}:
            return jsonify({"error": "Отсутствуют данные JSON"}), 400
            
        # Проверка наличия параметра water_level
        if "water_level" not in data:
            return jsonify({"error": "Отсутствует параметр 'water_level'"}), 400
            
        # Проверка типа параметра water_level
        try:
            water_level = float(data["water_level"])
        except (ValueError, TypeError):
            return jsonify({"error": "Параметр 'water_level' должен быть числом"}), 400

        # Проверка превышения критического уровня
        if water_level > 350:
            print(f" Пора выключать! Уровень воды: {water_level}")

        return jsonify({"status": "ok"}), 200
        
    except Exception as e:
        print(f"Ошибка при обработке запроса: {str(e)}")
        return jsonify({"error": "Внутренняя ошибка сервера"}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5055)
