class RBUser:
    def __init__(self,
                 id: int | None = None,
                 name: str | None = None,
                 surname: str | None = None,
                 patronymic: str | None = None,
                 phone_number: str | None = None,
                 email: str | None = None):
        self.id = id
        self.name = name
        self.surname = surname
        self.patronymic = patronymic
        self.phone_number = phone_number
        self.email = email

        
    def to_dict(self) -> dict:
        data = {'id': self.id, 'name': self.name, 'surname': self.surname, 'patronymic': self.patronymic, 'phone_number': self.phone_number, 'email': self.email}
        filtered_data = {key: value for key, value in data.items() if value is not None}
        return filtered_data