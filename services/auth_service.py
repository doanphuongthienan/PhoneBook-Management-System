class AuthService:

    def register(self, username, password, email) -> bool:
        if not hasattr(self, "users"):
            self.users = {}
            self.current_user = None

        if username in self.users:
            return False

        self.users[username] = {"password": password, "email": email}
        return True
    
    def login(self, username, password) -> bool:
        if not hasattr(self, "users"):
            return False

        if username in self.users and self.users[username]["password"] == password:
            self.current_user = username
            return True
        return False

    def logout(self) -> None:
        if hasattr(self, "current_user"):
            self.current_user = None

    def forgot_password(self, email) -> bool:
        if not hasattr(self, "users"):
            return False

        for user in self.users.values():
            if user["email"] == email:
                return True
        return False