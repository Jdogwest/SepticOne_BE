class RBSeptic:
    def __init__(self, septic_id: int | None = None,
                 city : str | None = None,
                 street: str | None = None,
                 house: str | None = None,
                 volume: str | None = None,
                 model: str | None = None,
                 owner: int | None = None):
        self.id = septic_id
        self.city = city
        self.street = street
        self.house = house
        self.volume = volume
        self.model = model
        self.owner = owner

        
    def to_dict(self) -> dict:
        data = {'id': self.id, 'city': self.city, 'street': self.street, 'house': self.house, 'volume': self.volume, 'model': self.model, 'owner': self.owner}
        filtered_data = {key: value for key, value in data.items() if value is not None}
        return filtered_data