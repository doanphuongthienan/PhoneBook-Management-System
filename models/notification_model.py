from datetime import datetime


class Notification:
    def __init__(self, notification_id, user_id, message, notification_type, created_at=None):
        self.notification_id = notification_id
        self.user_id = user_id
        self.message = message
        self.notification_type = notification_type  # birthday, contact_creation, system
        self.created_at = created_at or datetime.now().isoformat()
        self.is_read = False

    def to_dict(self):
        return {
            "notification_id": self.notification_id,
            "user_id": self.user_id,
            "message": self.message,
            "notification_type": self.notification_type,
            "created_at": self.created_at,
            "is_read": self.is_read
        }

