from datetime import datetime


class Group:
    def __init__(self, group_id, name, owner_id, created_at=None):
        self.group_id = group_id
        self.name = name
        self.owner_id = owner_id
        self.created_at = created_at or datetime.now().isoformat()

    def to_dict(self):
        return {
            "group_id": self.group_id,
            "name": self.name,
            "owner_id": self.owner_id,
            "created_at": self.created_at
        }
