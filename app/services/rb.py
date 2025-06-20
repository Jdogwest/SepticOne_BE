import decimal


class RBService:
    def __init__(self,
                 service_id: int | None = None,
                 name: str | None = None,
                 price: decimal.Decimal | None = None,
                 description: str | None = None,
                 time_to_complete: float | None = None):
        self.id = service_id
        self.name = name
        self.price = price
        self.description = description
        self.time_to_complete = time_to_complete

        
    def to_dict(self) -> dict:
        data = {'id': self.id, 'name': self.name, 'price': self.price, 'description': self.description, 'time_to_complete': self.time_to_complete}
        filtered_data = {key: value for key, value in data.items() if value is not None}
        return filtered_data