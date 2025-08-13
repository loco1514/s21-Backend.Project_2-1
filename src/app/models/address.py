from sqlalchemy import Column, String, UUID
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app import db

class Address(db.Model):
    __tablename__ = 'address'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    street = Column(String(255), nullable=False)
    city = Column(String(100), nullable=False)
    country = Column(String(100), nullable=False)