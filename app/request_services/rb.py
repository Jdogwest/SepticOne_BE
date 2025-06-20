class RBRequestService:
    def __init__(self, id: int | None = None,
                 service_id: int | None = None,
                 amount: int | None = None):
        self.id = id
        self.service_id = service_id
        self.amount = amount

        
    def to_dict(self) -> dict:
        data = {'id': self.id, 'service_id': self.service_id, 'amount': self.amount}
        filtered_data = {key: value for key, value in data.items() if value is not None}
        return filtered_data