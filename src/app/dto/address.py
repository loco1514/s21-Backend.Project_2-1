class AddressDTO:
    def __init__(self, id, country, city,street):
        self.id = id
        self.country = country
        self.city = city
        self.street = street

    def to_dict(self):
        return{
            "id": self.id,
            "country": self.country,
            "city": self.city,
            "street": self.street
        }
    