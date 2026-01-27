from datetime import datetime


class Contact:
    def __init__(self, contact_id, name, phone, email, owner_id, address="", notes="", 
                 birthday=None, groups=None, created_at=None, updated_at=None):
        self.contact_id = contact_id
        self.name = name
        self.phone = phone
        self.email = email
        self.owner_id = owner_id
        self.address = address
        self.notes = notes
        self.birthday = birthday
        self.groups = groups or []
        self.created_at = created_at or datetime.now().isoformat()
        self.updated_at = updated_at or datetime.now().isoformat()

    def to_dict(self):
        return {
            "contact_id": self.contact_id,
            "name": self.name,
            "phone": self.phone,
            "email": self.email,
            "owner_id": self.owner_id,
            "address": self.address,
            "notes": self.notes,
            "birthday": self.birthday,
            "groups": self.groups,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
