class ContactGroup:
    def __init__(self, contact_id, group_id):
        self.contact_id = contact_id
        self.group_id = group_id

    def to_dict(self):
        return {
            "contact_id": self.contact_id,
            "group_id": self.group_id
        }
