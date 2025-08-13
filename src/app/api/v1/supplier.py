from flask import Blueprint, Response, current_app, jsonify, request
from app.repositories.supplier import SupplierRepository
from app.mappers.supplier import SupplierMapper
from app.dto.supplier import SupplierDTO

supplier_bp = Blueprint('supplier', __name__, url_prefix='/api/v1/supplier')  # Добавлен ведущий слэш

# Получение списка всех поставщиков
@supplier_bp.route('/', methods=['GET'])
def get_suppliers():
    suppliers = SupplierRepository.get_all()
    if not suppliers:
        return jsonify([]), 200
    
    supplier_dict = [supplier.to_dict() for supplier in suppliers]
    json_data = current_app.json.dumps(supplier_dict, sort_keys=False, ensure_ascii=False)
    return Response(json_data, content_type="application/json")

@supplier_bp.route('/<uuid:supplier_id>', methods=['GET'])
def get_supplier_by_id(supplier_id):
    supplier = SupplierRepository.get_by_id(supplier_id)
    
    if not supplier:
        return jsonify({"error": "Supplier not found"}), 404

    # Преобразуем объект Supplier в DTO
    supplier_dto = SupplierMapper.to_dto(supplier)
    supplier_dict = supplier_dto.__dict__
    json_data = current_app.json.dumps(supplier_dict, sort_keys=False, ensure_ascii=False)
    return Response(json_data, content_type="application/json")


@supplier_bp.route('/', methods=['POST'])
def create_supplier():
    data = request.get_json()

    required_field = ["name", "address_id", "phone_number"]
    missing_fields = [field for field in required_field if field not in data]
    if missing_fields:
        return jsonify({"error": f"Missing fields: {', '.join(missing_fields)}"}), 400
    
    supplier_dto = SupplierDTO(
        name=data.get("name"),
        address_id=data.get("address_id"),
        phone_number=data.get("phone_number")
    )

    supplier = SupplierMapper.to_entity(supplier_dto)
    saved_supplier = SupplierRepository.create(supplier)
    supplier_dto = SupplierMapper.to_dto(saved_supplier)

    supplier_dict = supplier_dto.to_dict()
    json_data = current_app.json.dumps(supplier_dict, sort_keys=False, ensure_ascii=False)
    return Response(json_data, content_type="application/json"), 201

@supplier_bp.route('/<uuid:supplier_id>', methods=['DELETE'])
def delete_supplier(supplier_id):
    supplier = SupplierRepository.get_by_id(supplier_id)
    if not supplier:
        return jsonify({"error": "Supplier not found"}), 404
    
    SupplierRepository.delete(supplier)
    return jsonify({"message": "Supplier deleted successfully"}), 200

@supplier_bp.route('/<uuid:supplier_id>', methods=['PATCH'])
def update_supplier_address(supplier_id):
    data = request.json

    if not data or not data.get('address_id'):
        return jsonify({"error": "Supplier not found"}), 404
    
    supplier = SupplierRepository.get_by_id(supplier_id)
    if not supplier:
        return jsonify({"error": "Supplier not found"}), 404
    
    try:
        updated_supplier = SupplierRepository.update(supplier, data['address_id'])
        updated_supplier_dict = SupplierMapper.to_dto(updated_supplier).__dict__
        json_data = current_app.json.dumps(updated_supplier_dict, sort_keys=False, ensure_ascii=False)
        return Response(json_data, content_type="application/json")
    except ValueError as e:
        return jsonify({"error": str(e)}), 400