from sqlalchemy import Column, LargeBinary
from sqlalchemy.dialects.postgresql import UUID
from app import db
import uuid

class Images(db.Model):
    __tablename__ = 'images'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    image = Column(LargeBinary, nullable=False)

    def __init__(self, image):
        self.image = image

    def to_dict(self):
        return {
            'id': self.id,
            'image': self.image
        }
