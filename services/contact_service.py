class ContactService:
    def __init__(self):
        self.contacts = []

    # Guest + Registered User
    def search_contacts(self, keyword):
        result = []
        for contact in self.contacts:
            if keyword.lower() in contact["name"].lower():
                result.append(contact)
        return result

    def view_contact(self, contact_id):
        for contact in self.contacts:
            if contact["id"] == contact_id:
                return contact
        return None

    # Registered User
    def add_contact(self, contact_data) -> bool:
        self.contacts.append(contact_data)
        return True

    def update_contact(self, contact_id, new_data) -> bool:
        for contact in self.contacts:
            if contact["id"] == contact_id:
                contact.update(new_data)
                return True
        return False

    def delete_contact(self, contact_id) -> bool:
        if not self.contacts:
            return False

        if not self.confirm_deletion():
            return False

        for contact in self.contacts:
            if contact["id"] == contact_id:
                self.contacts.remove(contact)
                return True
        return False

    def confirm_deletion(self) -> bool:
        # giả lập xác nhận xóa
        return True