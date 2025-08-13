class ProductDTO:
    def __init__(self, name, category, price, available_stock, supplier_id, image_id=None, id=None):
        self.id = id
        self.name = name
        self.category = category
        self.price = price
        self.available_stock = available_stock
        self.supplier_id = supplier_id
        self.image_id = image_id

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category,
            "price": self.price,
            "available_stock": self.available_stock,
            "supplier_id": self.supplier_id,
            "image_id": self.image_id}