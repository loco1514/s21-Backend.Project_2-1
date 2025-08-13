from app.dto.product import ProductDTO
from app.models.product import Product

class ProductMapper:
    @staticmethod
    def to_entity(dto):
        return Product(
            name=dto.name,
            category=dto.category,
            price=dto.price,
            available_stock=dto.available_stock,
            supplier_id=dto.supplier_id,
            image_id=dto.image_id
        )

    @staticmethod
    def to_dto(entity):
        return ProductDTO(
            id=str(entity.id),
            name=entity.name,
            category=entity.category,
            price=entity.price,
            available_stock=entity.available_stock,
            supplier_id=str(entity.supplier_id),
            image_id=str(entity.image_id) if entity.image_id else None
        )