from app.models.clients import Client
from uuid import UUID
from app.dto.clients import ClientDTO

class ClientMapper:
    @staticmethod
    def to_entity(dto):
        address_id = UUID(dto.address_id) if dto.address_id else None
        return Client(
            client_name=dto.client_name,
            client_surname=dto.client_surname,
            birthday=dto.birthday,
            gender=dto.gender,
            address_id=address_id  # Убедитесь, что передаете UUID, если оно есть
        )

    @staticmethod
    def to_dto(client):
        return ClientDTO(
            client_name=client.client_name,
            client_surname=client.client_surname,
            birthday=client.birthday,
            gender=client.gender,
            address_id=str(client.address_id) if client.address_id else None,
            id=str(client.id) if client.id else None
        )
