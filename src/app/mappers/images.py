from app.models.images import Images
from app.dto.images import ImageDTO

class ImageMappers:
    @staticmethod
    def to_entity(dto):
        return Images(
            image=dto.image  # Убедитесь, что dto.image — это байты
        )

    @staticmethod
    def to_dto(images):
        return ImageDTO(
            id=images.id,
            image=images.image  # Это уже байты, которые можно использовать для дальнейших операций
        )
