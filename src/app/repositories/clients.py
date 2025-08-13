# app/repositories/clients.py

from sqlalchemy import UUID
from app.database import db
from app.models.address import Address  # Импортируем модель Address, она не вызывает циклического импорта
from app.models.clients import Client

class ClientRepository:
    @staticmethod
    def get_all(limit=None, offset=None):
        query = db.session.query(Client)  # Пример с использованием SQLAlchemy
        
        if limit is not None:
            query = query.limit(limit)
        
        if offset is not None:
            query = query.offset(offset)
        
        return query.all()

    @staticmethod
    def get_by_name_and_surname(client_name, client_surname):
        # Отложенный импорт внутри метода
          
        return Client.query.filter_by(client_name=client_name, client_surname=client_surname).first()

    @staticmethod
    def create(client):
        try:
            db.session.add(client)  # Добавляем нового клиента в сессию
            db.session.commit()  # Сохраняем изменения в базе данных
            return client  # Возвращаем сохраненного клиента
        except Exception as e:
            db.session.rollback()  # Откатываем изменения в случае ошибки
            raise e

    @staticmethod
    def update(client, new_address_id):
        # Отложенный импорт внутри метода
          
        address = Address.query.get(new_address_id)
        if not address:
            raise ValueError("Address not found")
        client.address_id = new_address_id
        db.session.commit()
        return client
    
    @staticmethod
    def get_by_id(client_id: UUID):
          
        # Используйте ваш ORM (например, SQLAlchemy) для получения клиента по ID
        return Client.query.filter_by(id=client_id).first()

    @staticmethod
    def delete(client):
        # Отложенный импорт внутри метода
          
        db.session.delete(client)
        db.session.commit()
