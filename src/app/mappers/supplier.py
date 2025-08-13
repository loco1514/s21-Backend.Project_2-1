from uuid import UUID
from app.models.supplier import Supplier
from app.dto.supplier import SupplierDTO

class SupplierMapper:
    @staticmethod
    def to_entity(dto):
        address_id = UUID(dto.address_id) if dto.address_id else None
        return Supplier(
            name = dto.name,
            address_id = address_id,
            phone_number = dto.phone_number
        )
    
    @staticmethod
    def to_dto(supplier):
        return SupplierDTO(
            name = supplier.name,
            phone_number = supplier.phone_number,
            address_id=str(supplier.address_id) if supplier.address_id else None,
            id=str(supplier.id) if supplier.id else None
        )