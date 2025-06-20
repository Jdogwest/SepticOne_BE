class RBWorkmanBrigadier:
    def __init__(self,
                 workman_id: int | None = None,
                 brigadier_id: str | None = None):
        self.workman_id = workman_id
        self.brigadier_id = brigadier_id

        
    def to_dict(self) -> dict:
        data = {'workman_id': self.workman_id, 'brigadier_id': self.brigadier_id}
        filtered_data = {key: value for key, value in data.items() if value is not None}
        return filtered_data