from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from app import db
import uuid

class Supplier(db.Model):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(200), nullable=False)
    phone_number = Column(String(45), nullable=False)

    # Здесь указывается внешний ключ, который ссылается на таблицу Address
    address_id = Column(UUID(as_uuid=True), ForeignKey('address.id'), nullable=True)
    
    # Связь с моделью Address
    address = db.relationship('Address', backref='supplier', lazy=True)

    def __init__(self, name, address_id, phone_number):
        self.name = name
        self.address_id = address_id
        self.phone_number = phone_number

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,            
            'address_id': self.address_id,
            'phone_number': self.phone_number
            }