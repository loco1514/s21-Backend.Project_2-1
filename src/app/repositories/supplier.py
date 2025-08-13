from sqlalchemy import UUID
from app.database import db
from app.models.supplier import Supplier
from app.models.address import Address  # Импортируем модель Address, она не вызывает циклического импорта

class SupplierRepository:
    @staticmethod
    def get_all():
        return Supplier.query.all()
    
    @staticmethod
    def get_by_id(supplier_id):
        return Supplier.query.filter_by(id=supplier_id).first()  # Используем .first()

    
    @staticmethod
    def create(supplier):
        try:
            db.session.add(supplier)  # Добавляем нового клиента в сессию
            db.session.commit()  # Сохраняем изменения в базе данных
            return supplier  # Возвращаем сохраненного клиента
        except Exception as e:
            db.session.rollback()  # Откатываем изменения в случае ошибки
            raise e

    @staticmethod
    def delete(supplier):
        db.session.delete(supplier)
        db.session.commit()
    
    @staticmethod
    def update(supplier, new_address_id):
        # Отложенный импорт внутри метода 
        address = Address.query.get(new_address_id)
        if not address:
            raise ValueError("Address not found")
        supplier.address_id = new_address_id
        db.session.commit()
        return supplier