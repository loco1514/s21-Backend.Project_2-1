from app.database import db
from app.models.images import Images
from sqlalchemy.exc import IntegrityError
from app.models.product import Product

class ImageRepository:
    @staticmethod
    def add_image(image_data):
        try:
            # Убедитесь, что image_data — это байты, а не объект Images
            if isinstance(image_data, Images):
                raise TypeError("Expected binary data, got Images object")
            
            image = Images(image=image_data)  # Создаем новый объект Images
            db.session.add(image)
            db.session.commit()
            return image
        except IntegrityError as e:
            db.session.rollback()
            raise e
    
    @staticmethod
    def get_image_by_product_id(product_id):
        """
        Получить изображение по идентификатору продукта.
        """
        # Находим продукт по ID
        product = Product.query.filter_by(id=product_id).first()
        if not product or not product.image_id:
            return None  # Продукт не найден или не связан с изображением

        # Находим изображение по image_id
        return Images.query.filter_by(id=product.image_id).first()


    @staticmethod
    def get_by_id(image_id):
        return Images.query.filter_by(id=image_id).first()

    @staticmethod
    def delete(image):
        db.session.delete(image)
        db.session.commit()

    @staticmethod
    def update(image_id, new_image_data):
        image = Images.query.get(image_id)
        if image:
            image.image = new_image_data
            db.session.commit()
            return image
        return None
