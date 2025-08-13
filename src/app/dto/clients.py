from datetime import datetime

class ClientDTO:
    def __init__(self, client_name, client_surname, birthday, gender, address_id=None, id=None):
        self.id = id if id else None  # Если ID не передано, будет None (для новых клиентов)
        self.client_name = client_name
        self.client_surname = client_surname
        self.birthday = birthday
        self.gender = gender
        self.registration_date = datetime.now().strftime("%Y-%m-%d")  # Устанавливаем текущую дату как дату регистрации
        self.address_id = address_id

    def to_dict(self):
        return {
            "id": self.id,
            "client_name": self.client_name,
            "client_surname": self.client_surname,
            "birthday": self.birthday,
            "gender": self.gender,
            "registration_date": self.registration_date,
            "address_id": self.address_id
        }


