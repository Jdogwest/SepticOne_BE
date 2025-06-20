from datetime import datetime


class RBCallRequest:
    def __init__(self, id: int | None = None,
                 created_at: datetime | None = None,
                 fio: str | None = None,
                 phone_number: str | None = None,
                 comment: str | None = None,
                 status: str | None = None,):
        self.id = id
        self.created_at = created_at
        self.fio = fio
        self.phone_number = phone_number
        self.comment = comment
        self.status = status

        
    def to_dict(self) -> dict:
        data = {'id': self.id, 'created_at': self.created_at, 'fio': self.fio, 'phone_number': self.phone_number, 'comment': self.comment, 'status': self.status}
        filtered_data = {key: value for key, value in data.items() if value is not None}
        return filtered_data