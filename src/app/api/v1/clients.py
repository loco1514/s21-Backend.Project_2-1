from flask import Blueprint, Response, current_app, json, jsonify, request
from app.repositories.clients import ClientRepository
from app.mappers.clients import ClientMapper
from app.dto.clients import ClientDTO

client_bp = Blueprint('clients', __name__, url_prefix='/api/v1/clients')

# Получение списка всех клиентов
@client_bp.route('/', methods=['GET'])
def get_clients():
    # Получаем параметры пагинации из строки запроса
    limit = request.args.get('limit', default=None, type=int)
    offset = request.args.get('offset', default=None, type=int)

    # Получаем все клиенты или с учетом пагинации
    if limit is not None and offset is not None:
        clients = ClientRepository.get_all(limit=limit, offset=offset)
    else:
        clients = ClientRepository.get_all(limit=None, offset=None)

    if not clients:
        return jsonify([]), 200

    # Преобразуем клиентов в список словарей
    clients_dict = [client.to_dict() for client in clients]
    
    # Возвращаем результат в формате JSON
    json_data = current_app.json.dumps(clients_dict, sort_keys=False, ensure_ascii=False)
    return Response(json_data, content_type="application/json")

# Получение клиента по имени и фамилии
@client_bp.route('/<string:client_name>&<string:client_surname>', methods=['GET'])
def get_client_by_name_and_surname(client_name, client_surname):
    client = ClientRepository.get_by_name_and_surname(client_name, client_surname)
    if not client:
        return jsonify({"error": "Client not found"}), 404

    client_dict = ClientMapper.to_dto(client).__dict__
    json_data = current_app.json.dumps(client_dict, sort_keys=False, ensure_ascii=False)
    return Response(json_data, content_type="application/json")

# Создание нового клиента
@client_bp.route('/', methods=['POST'])
def create_client():
    data = request.get_json()

    # Проверка наличия всех необходимых данных
    required_fields = ["client_name", "client_surname", "birthday", "gender", "address_id"]
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return jsonify({"error": f"Missing fields: {', '.join(missing_fields)}"}), 400

    # Создаем DTO из данных
    client_dto = ClientDTO(
        client_name=data.get("client_name"),
        client_surname=data.get("client_surname"),
        birthday=data.get("birthday"),
        gender=data.get("gender"),
        address_id=data.get("address_id")
    )

    # Преобразуем DTO в модель клиента
    client = ClientMapper.to_entity(client_dto)

    # Сохраняем клиента в базе данных
    saved_client = ClientRepository.create(client)

    # Возвращаем сохраненный клиент как DTO
    client_dto = ClientMapper.to_dto(saved_client)

    return Response(
        json.dumps(client_dto.to_dict(), sort_keys=False, ensure_ascii=False),
        content_type="application/json"
    ), 201

# Обновление адреса клиента
@client_bp.route('/<uuid:client_id>', methods=['PATCH'])
def update_client_address(client_id):
    data = request.json

    if not data or not data.get('address_id'):
        return jsonify({"error": "Address ID is required"}), 400

    client = ClientRepository.get_by_id(client_id)
    if not client:
        return jsonify({"error": "Client not found"}), 404

    try:
        updated_client = ClientRepository.update(client, data['address_id'])
        updated_client_dict = ClientMapper.to_dto(updated_client).__dict__
        json_data = current_app.json.dumps(updated_client_dict, sort_keys=False, ensure_ascii=False)
        return Response(json_data, content_type="application/json")
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

# Удаление клиента
@client_bp.route('/<uuid:client_id>', methods=['DELETE'])
def delete_client(client_id):
    client = ClientRepository.get_by_id(client_id)
    if not client:
        return jsonify({"error": "Client not found"}), 404

    ClientRepository.delete(client)
    return jsonify({"message": "Client deleted successfully"}), 200
