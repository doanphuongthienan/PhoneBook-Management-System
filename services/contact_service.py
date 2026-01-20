class ContactService:

    # Guest + Registered User
    def search_contacts(self, keyword):
        pass

    def view_contact(self, contact_id):
        pass

    # Registered User
    def add_contact(self, contact_data) -> bool:
        pass

    def update_contact(self, contact_id, new_data) -> bool:
        pass

    def delete_contact(self, contact_id) -> bool:
        if self.confirm_deletion():
            pass

    def confirm_deletion(self) -> bool:
        pass
