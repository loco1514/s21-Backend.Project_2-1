class SupplierDTO:
    def __init__(self, name, address_id, phone_number, id=None):
        self.id = id if id else None
        self.name = name
        self.address_id = address_id
        self.phone_number = phone_number

    def to_dict(self):
        return{
            'id': self.id,
            'name': self.name,
            'address_id': self.address_id,
            'phone_number': self.phone_number
        }