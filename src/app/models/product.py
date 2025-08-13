from sqlalchemy import Column, String, Numeric, Integer, ForeignKey, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
from app.database import db
import uuid

class Product(db.Model):
    __tablename__ = 'product'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(200), nullable=False)
    category = Column(String(200), nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    available_stock = Column(Integer, nullable=False)
    last_update_date = Column(TIMESTAMP, nullable=False, server_default=db.func.now(), onupdate=db.func.now())
    supplier_id = Column(UUID(as_uuid=True), ForeignKey('supplier.id'), nullable=False)
    image_id = Column(UUID(as_uuid=True), ForeignKey('images.id'), nullable=True)

    def __init__(self, name, category, price, available_stock, supplier_id, image_id=None):
        self.name = name
        self.category = category
        self.price = price
        self.available_stock = available_stock
        self.supplier_id = supplier_id
        self.image_id = image_id

    def to_dict(self):
        return {
            "id": str(self.id),
            "name": self.name,
            "category": self.category,
            "price": float(self.price),
            "available_stock": self.available_stock,
            "last_update_date": self.last_update_date.isoformat(),
            "supplier_id": str(self.supplier_id),
            "image_id": str(self.image_id) if self.image_id else None
        }