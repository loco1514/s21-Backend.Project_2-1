from flask import Flask, send_from_directory
from flask_swagger_ui import get_swaggerui_blueprint
from app import create_app

SWAGGER_URL = '/swagger'  # URL для Swagger UI
API_SPEC_PATH = '/swagger.yaml'  # Путь для swagger.yaml

# Создаем приложение через фабрику
app = create_app()

# Настройка маршрута для swagger.yaml
@app.route('/swagger.yaml')
def swagger_spec():
    return send_from_directory('.', 'swagger.yaml')  # '.' указывает на текущую директорию

# Настройка Swagger UI
swagger_ui = get_swaggerui_blueprint(SWAGGER_URL, API_SPEC_PATH)
app.register_blueprint(swagger_ui, url_prefix=SWAGGER_URL)

if __name__ == "__main__":
    # Запускаем приложение
    app.run(host="0.0.0.0", port=5000, debug=True)
