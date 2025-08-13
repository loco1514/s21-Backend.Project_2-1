class ImageDTO:
    def __init__(self, image, id=None):
        self.id = id if id else None
        self.image = image
    
    def to_dict(self):
        return {
            'id': self.id,
            'image': self.image
        }