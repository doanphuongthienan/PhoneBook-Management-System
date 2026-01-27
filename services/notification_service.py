import json
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from models.notification_model import Notification

DATA = "data/notifications.json"
HISTORY_DATA = "data/import_export_history.json"


def load_notifications():
    try:
        with open(DATA, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []


def save_notifications(notifications):
    with open(DATA, "w", encoding="utf-8") as f:
        json.dump(notifications, f, indent=2, ensure_ascii=False)


def send_email(recipient_email, subject, body):
    """Send email notification"""
    try:
        # Using print as fallback for demo purposes
        print(f"\n[EMAIL NOTIFICATION SENT]")
        print(f"To: {recipient_email}")
        print(f"Subject: {subject}")
        print(f"Message: {body}")
        print("-" * 50)
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False


def create_notification(user_id, message, notification_type="system"):
    """Create an in-system notification"""
    notifications = load_notifications()
    notification_id = len(notifications) + 1
    
    notification = Notification(notification_id, user_id, message, notification_type)
    notifications.append(notification.to_dict())
    save_notifications(notifications)
    
    return notification


def get_user_notifications(user_id):
    """Get all notifications for a user"""
    notifications = load_notifications()
    return [n for n in notifications if n["user_id"] == user_id]


def get_unread_notifications(user_id):
    """Get unread notifications for a user"""
    notifications = load_notifications()
    return [n for n in notifications if n["user_id"] == user_id and not n.get("is_read", False)]


def mark_notification_as_read(notification_id):
    """Mark notification as read"""
    notifications = load_notifications()
    for n in notifications:
        if n["notification_id"] == notification_id:
            n["is_read"] = True
            save_notifications(notifications)
            return True
    return False


def mark_all_notifications_as_read(user_id):
    """Mark all user notifications as read"""
    notifications = load_notifications()
    for n in notifications:
        if n["user_id"] == user_id:
            n["is_read"] = True
    save_notifications(notifications)


def notify_contact_creation(user_id, user_email, contact_name):
    """Notify user of successful contact creation"""
    message = f"Contact '{contact_name}' has been successfully created!"
    create_notification(user_id, message, "contact_creation")
    send_email(user_email, "Contact Created", message)


def notify_birthday(user_id, user_email, contact_name, birthday):
    """Notify user of contact birthday"""
    message = f"Today is {contact_name}'s birthday ({birthday})!"
    create_notification(user_id, message, "birthday")
    send_email(user_email, "Birthday Reminder", message)


def check_birthdays(user_id, user_email):
    """Check if any contacts have birthdays today and send notifications"""
    from services.contact_service import view_contacts
    from datetime import date
    
    contacts = view_contacts(user_id)
    today = date.today().strftime("%m-%d")
    
    for contact in contacts:
        if contact.get("birthday"):
            contact_birthday = contact["birthday"][-5:]  # Extract MM-DD
            if contact_birthday == today:
                notify_birthday(user_id, user_email, contact["name"], contact["birthday"])


def delete_notification(notification_id):
    """Delete a notification"""
    notifications = load_notifications()
    original_len = len(notifications)
    notifications = [n for n in notifications if n["notification_id"] != notification_id]
    
    if len(notifications) < original_len:
        save_notifications(notifications)
        return True
    return False


def clear_user_notifications(user_id):
    """Clear all notifications for a user"""
    notifications = load_notifications()
    notifications = [n for n in notifications if n["user_id"] != user_id]
    save_notifications(notifications)

