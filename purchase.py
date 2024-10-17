class purchase:
    def __init__(self, id: int = 0, date: str = "", total: float = 0.0, user_id: int = 0) -> None:
        self.id = id
        self.date = date
        self.total = total
        self.user_id = user_id
    
    def get_id(self) -> int:
        return self.id
    
    def get_date(self) -> str:
        return self.date
    
    def get_total(self) -> float:
        return self.total
    
    def get_user_id(self) -> int:
        return self.user_id
