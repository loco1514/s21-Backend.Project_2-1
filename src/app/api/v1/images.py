import base64
from flask import Blueprint, Response, jsonify, request
from app.repositories.images import ImageRepository
from app.dto.images import ImageDTO
from app.dto.product import ProductDTO
from app.mappers.product import ProductMapper
from app.mappers.images import ImageMappers
from app.api.v1.product import get_product_by_id

image_bp = Blueprint('image', __name__, url_prefix='/api/v1/images')

# Add a new image
@image_bp.route('/', methods=['POST'])
def add_image():
    # Проверяем, что Content-Type корректный
    if request.content_type != 'application/octet-stream':
        return jsonify({"error": "Content-Type must be application/octet-stream"}), 415

    try:
        # Считываем бинарные данные из тела запроса
        image_binary = request.data  # Читаем сырые данные запроса

        # Проверяем, что тело запроса не пустое
        if not image_binary:
            return jsonify({"error": "Request body is empty"}), 400

        # Создаем DTO и сохраняем изображение
        image_dto = ImageDTO(image=image_binary)
        image_entity = ImageMappers.to_entity(image_dto)
        saved_image = ImageRepository.add_image(image_entity.image)

        # Преобразуем сохранённое изображение в DTO
        image_dto = ImageMappers.to_dto(saved_image)

        # Возвращаем успешный ответ
        return Response(image_dto.image, content_type="application/octet-stream", status=201)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Get image by ID
@image_bp.route('/<uuid:image_id>', methods=['GET'])
def get_image_by_id(image_id):
    try:
        # Получаем изображение по ID
        image = ImageRepository.get_by_id(image_id)

        if not image:
            return jsonify({"error": "Image not found"}), 404

        # Возвращаем бинарные данные изображения с корректным Content-Type
        return Response(image.image, content_type="application/octet-stream")

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Update image by ID
@image_bp.route('/<uuid:image_id>', methods=['PATCH'])
def update_image(image_id):
    if request.content_type != 'application/octet-stream':
        return jsonify({"error": "Content-Type must be application/octet-stream"}), 415

    try:
        # Считываем новые бинарные данные изображения
        new_image_binary = request.data

        if not new_image_binary:
            return jsonify({"error": "Request body is empty"}), 400

        # Обновляем изображение
        updated_image = ImageRepository.update(image_id, new_image_binary)

        if not updated_image:
            return jsonify({"error": "Image not found"}), 404

        # Возвращаем обновленное изображение
        return Response(updated_image.image, content_type="application/octet-stream")

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Delete image by ID
@image_bp.route('/<uuid:image_id>', methods=['DELETE'])
def delete_image(image_id):
    try:
        image = ImageRepository.get_by_id(image_id)

        if not image:
            return jsonify({"error": "Image not found"}), 404

        ImageRepository.delete(image)
        return jsonify({"message": "Image deleted successfully"}), 204

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@image_bp.route('/product/<uuid:product_id>', methods=['GET'])
def get_image_by_product_id(product_id):
    try:
        # Используем метод репозитория для получения изображения по ID продукта
        image = ImageRepository.get_image_by_product_id(product_id)

        if not image:
            return jsonify({"error": "Image not found for the given product"}), 404

        return Response(image.image, content_type="application/octet-stream")
    except Exception as e:
        return jsonify({"error": str(e)}), 500
