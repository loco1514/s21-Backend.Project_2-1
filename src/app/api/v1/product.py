from flask import Blueprint, Response, current_app, jsonify, request
from app.repositories.product import ProductRepository
from app.mappers.product import ProductMapper
from app.dto.product import ProductDTO

product_bp = Blueprint('product', __name__, url_prefix='/api/v1/product')

# Add a new product
@product_bp.route('/', methods=['POST'])
def create_product():
    data = request.get_json()

    required_fields = ["name", "category", "price", "available_stock", "supplier_id"]
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return jsonify({"error": f"Missing fields: {', '.join(missing_fields)}"}), 400

    try:
        product_dto = ProductDTO(
            name=data["name"],
            category=data["category"],
            price=data["price"],
            available_stock=data["available_stock"],
            supplier_id=data["supplier_id"],
            image_id=data.get("image_id")
        )

        product = ProductMapper.to_entity(product_dto)
        saved_product = ProductRepository.create(product)
        product_dto = ProductMapper.to_dto(saved_product)

        product_dict = product_dto.to_dict()
        json_data = current_app.json.dumps(product_dict, sort_keys=False, ensure_ascii=False)
        return Response(json_data, content_type="application/json"), 201

    except ValueError as e:
        return jsonify({"error": str(e)}), 400

# Reduce product stock
@product_bp.route('/<uuid:product_id>', methods=['PATCH'])
def reduce_stock(product_id):
    try:
        product_id = str(product_id)  # Преобразование UUID в строку
    except ValueError:
        return jsonify({"error": "Invalid product ID format"}), 400

    data = request.get_json()
    quantity = data.get('quantity')

    if not isinstance(quantity, int) or quantity <= 0:
        return jsonify({"error": "Invalid quantity value"}), 400

    try:
        updated_product = ProductRepository.reduce_stock(product_id, quantity)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    return jsonify(ProductMapper.to_dto(updated_product).to_dict())


# Get a product by ID
@product_bp.route('/<uuid:product_id>', methods=['GET'])
def get_product_by_id(product_id):
    product = ProductRepository.get_by_id(product_id)

    if not product:
        return jsonify({"error": "Product not found"}), 404

    product_dto = ProductMapper.to_dto(product)
    product_dict = product_dto.to_dict()
    json_data = current_app.json.dumps(product_dict, sort_keys=False, ensure_ascii=False)
    return Response(json_data, content_type="application/json")

# Get all available products
@product_bp.route('/', methods=['GET'])
def get_products():
    products = ProductRepository.get_all()
    
    if not products:
        return jsonify([]), 200

    product_dicts = [ProductMapper.to_dto(product).to_dict() for product in products]
    json_data = current_app.json.dumps(product_dicts, sort_keys=False, ensure_ascii=False)
    return Response(json_data, content_type="application/json")

# Delete a product by ID
@product_bp.route('/<uuid:product_id>', methods=['DELETE'])
def delete_product(product_id):
    product = ProductRepository.get_by_id(product_id)

    if not product:
        return jsonify({"error": "Product not found"}), 404

    ProductRepository.delete(product)
    return jsonify({"message": "Product deleted successfully"}), 204

