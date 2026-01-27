from datetime import datetime


class User:
    def __init__(self, user_id, full_name, email, phone, password, created_at=None):
        self.user_id = user_id
        self.full_name = full_name
        self.email = email
        self.phone = phone
        self.password = password
        self.created_at = created_at or datetime.now().isoformat()

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "full_name": self.full_name,
            "email": self.email,
            "phone": self.phone,
            "password": self.password,
            "created_at": self.created_at
        }
