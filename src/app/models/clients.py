# app/models/clients.py
from sqlalchemy import Column, String, Date, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from app import db
import uuid
from datetime import datetime

class Client(db.Model):
    __tablename__ = 'client'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    client_name = Column(String(100), nullable=False)
    client_surname = Column(String(100), nullable=False)
    birthday = Column(Date)
    gender = Column(String(10))
    registration_date = Column(DateTime, default=datetime.utcnow)
    
    # Здесь указывается внешний ключ, который ссылается на таблицу Address
    address_id = Column(UUID(as_uuid=True), ForeignKey('address.id'), nullable=True)
    
    # Связь с моделью Address
    address = db.relationship('Address', backref='clients', lazy=True)

    def __init__(self, client_name, client_surname, birthday, gender, address_id):
        self.client_name = client_name
        self.client_surname = client_surname
        self.birthday = birthday
        self.gender = gender
        self.address_id = address_id

    def to_dict(self):
        return {
            'id': self.id,
            'client_name': self.client_name,
            'client_surname': self.client_surname,
            'birthday': self.birthday,
            'gender': self.gender,
            'registration_date': self.registration_date,
            'address_id': self.address_id
        }
