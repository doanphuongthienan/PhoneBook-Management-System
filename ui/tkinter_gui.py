import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog
import tkinter.font as tkFont
from datetime import datetime
import json

# PIL is optional - try to import but don't require it
try:
    from PIL import Image, ImageTk
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

from services.auth_service import register, login, get_user_by_email, reset_password
from services.user_service import get_user_by_id, update_user_profile
from services.contact_service import (
    add_contact, view_contacts, get_contact_by_id, search_contacts,
    sort_contacts, edit_contact, delete_contact, get_contacts_by_group
)
from services.group_service import (
    add_group, get_user_groups, get_group_by_name, delete_group,
    add_contact_to_group, remove_contact_from_group
)
from services.notification_service import (
    get_user_notifications, get_unread_notifications, mark_notification_as_read,
    mark_all_notifications_as_read, clear_user_notifications, check_birthdays
)
from services.import_export_service import (
    export_contacts, export_contacts_by_group, import_contacts, get_user_history, add_history_entry
)

# Color Scheme
COLORS = {
    'primary': '#2E86AB',      # Blue
    'secondary': '#A23B72',    # Purple
    'accent': '#F18F01',       # Orange
    'success': '#06A77D',      # Green
    'danger': '#C1121F',       # Red
    'dark': '#1A1A1A',         # Dark
    'light': '#F5F5F5',        # Light
    'text': '#333333',         # Text color
    'bg': '#FAFAFA',           # Background
    'border': '#E0E0E0',       # Border
}


class PhoneBookApp(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("Phone Book Management System")
        self.geometry("1200x700")
        self.minsize(800, 600)
        
        # Configure style
        self.configure(bg=COLORS['bg'])
        
        # Current user
        self.current_user = None
        self.current_frame = None
        
        # Create main container
        self.container = tk.Frame(self, bg=COLORS['bg'])
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        
        # Show login frame
        self.show_frame(LoginFrame)
    
    def show_frame(self, cont):
        if self.current_frame:
            self.current_frame.destroy()
        
        self.current_frame = frame = cont(self.container, self)
        frame.grid(row=0, column=0, sticky="nsew")
        frame.tkraise()


class BaseFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=COLORS['bg'])
        self.controller = controller
    
    def create_header(self, title):
        header = tk.Frame(self, bg=COLORS['primary'], height=60)
        header.pack(fill="x")
        
        title_label = tk.Label(
            header,
            text=title,
            font=("Arial", 24, "bold"),
            fg="white",
            bg=COLORS['primary']
        )
        title_label.pack(pady=10)
    
    def create_button(self, parent, text, command, bg=COLORS['primary'], fg="white", width=15):
        btn = tk.Button(
            parent,
            text=text,
            command=command,
            bg=bg,
            fg=fg,
            font=("Arial", 11, "bold"),
            padx=15,
            pady=10,
            relief="flat",
            cursor="hand2",
            width=width
        )
        btn.pack(pady=5)
        return btn
    
    def create_entry(self, parent, label_text, show=None):
        label = tk.Label(parent, text=label_text, font=("Arial", 10), bg=COLORS['bg'], fg=COLORS['text'])
        label.pack(anchor="w", pady=(10, 2))
        
        entry = tk.Entry(
            parent,
            font=("Arial", 11),
            show=show,
            relief="solid",
            borderwidth=1,
            width=30
        )
        entry.pack(pady=(0, 10), ipady=8)
        return entry
    
    def center_window(self):
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.controller.geometry(f"{width}x{height}+{x}+{y}")


class LoginFrame(BaseFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        
        # Main container
        main_container = tk.Frame(self, bg=COLORS['bg'])
        main_container.pack(fill="both", expand=True, padx=40, pady=40)
        
        # Title
        title = tk.Label(
            main_container,
            text="Phone Book Management",
            font=("Arial", 28, "bold"),
            bg=COLORS['bg'],
            fg=COLORS['primary']
        )
        title.pack(pady=20)
        
        subtitle = tk.Label(
            main_container,
            text="Login to your account",
            font=("Arial", 12),
            bg=COLORS['bg'],
            fg=COLORS['text']
        )
        subtitle.pack(pady=(0, 30))
        
        # Input frame
        input_frame = tk.Frame(main_container, bg=COLORS['bg'])
        input_frame.pack(pady=20)
        
        self.email_entry = self.create_entry(input_frame, "Email Address:")
        self.password_entry = self.create_entry(input_frame, "Password:", show="*")
        
        # Button frame
        button_frame = tk.Frame(main_container, bg=COLORS['bg'])
        button_frame.pack(pady=20)
        
        self.create_button(button_frame, "LOGIN", self.login, width=20)
        self.create_button(button_frame, "REGISTER", self.show_register, bg=COLORS['secondary'], width=20)
        self.create_button(button_frame, "FORGOT PASSWORD", self.show_forgot_password, bg=COLORS['accent'], width=20)
        self.create_button(button_frame, "BROWSE AS GUEST", self.show_guest_view, bg=COLORS['success'], width=20)
    
    def login(self):
        email = self.email_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not email or not password:
            messagebox.showerror("Error", "Please fill in all fields")
            return
        
        success, user = login(email, password)
        if success:
            self.controller.current_user = user
            check_birthdays(user.get('user_id'), user.get('email'))
            self.controller.show_frame(DashboardFrame)
        else:
            messagebox.showerror("Login Failed", "Invalid email or password")
    
    def show_register(self):
        self.controller.show_frame(RegisterFrame)
    
    def show_forgot_password(self):
        self.controller.show_frame(ForgotPasswordFrame)
    
    def show_guest_view(self):
        self.controller.show_frame(GuestContactViewFrame)


class RegisterFrame(BaseFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        
        main_container = tk.Frame(self, bg=COLORS['bg'])
        main_container.pack(fill="both", expand=True, padx=40, pady=40)
        
        title = tk.Label(
            main_container,
            text="Create New Account",
            font=("Arial", 28, "bold"),
            bg=COLORS['bg'],
            fg=COLORS['primary']
        )
        title.pack(pady=20)
        
        input_frame = tk.Frame(main_container, bg=COLORS['bg'])
        input_frame.pack(pady=20)
        
        self.name_entry = self.create_entry(input_frame, "Full Name:")
        self.email_entry = self.create_entry(input_frame, "Email Address:")
        self.phone_entry = self.create_entry(input_frame, "Phone Number:")
        self.password_entry = self.create_entry(input_frame, "Password:", show="*")
        self.confirm_entry = self.create_entry(input_frame, "Confirm Password:", show="*")
        
        button_frame = tk.Frame(main_container, bg=COLORS['bg'])
        button_frame.pack(pady=20)
        
        self.create_button(button_frame, "REGISTER", self.register, width=20)
        self.create_button(button_frame, "BACK TO LOGIN", self.back_to_login, bg=COLORS['text'], width=20)
    
    def register(self):
        name = self.name_entry.get().strip()
        email = self.email_entry.get().strip()
        phone = self.phone_entry.get().strip()
        password = self.password_entry.get().strip()
        confirm = self.confirm_entry.get().strip()
        
        if not all([name, email, phone, password, confirm]):
            messagebox.showerror("Error", "Please fill in all fields")
            return
        
        if password != confirm:
            messagebox.showerror("Error", "Passwords do not match")
            return
        
        success, msg = register(name, email, phone, password)
        if success:
            messagebox.showinfo("Success", msg)
            self.controller.show_frame(LoginFrame)
        else:
            messagebox.showerror("Registration Failed", msg)
    
    def back_to_login(self):
        self.controller.show_frame(LoginFrame)


class ForgotPasswordFrame(BaseFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        
        main_container = tk.Frame(self, bg=COLORS['bg'])
        main_container.pack(fill="both", expand=True, padx=40, pady=40)
        
        title = tk.Label(
            main_container,
            text="Reset Password",
            font=("Arial", 28, "bold"),
            bg=COLORS['bg'],
            fg=COLORS['primary']
        )
        title.pack(pady=20)
        
        input_frame = tk.Frame(main_container, bg=COLORS['bg'])
        input_frame.pack(pady=20)
        
        self.email_entry = self.create_entry(input_frame, "Email Address:")
        self.password_entry = self.create_entry(input_frame, "New Password:", show="*")
        self.confirm_entry = self.create_entry(input_frame, "Confirm Password:", show="*")
        
        button_frame = tk.Frame(main_container, bg=COLORS['bg'])
        button_frame.pack(pady=20)
        
        self.create_button(button_frame, "RESET PASSWORD", self.reset_password_action, width=20)
        self.create_button(button_frame, "BACK TO LOGIN", self.back_to_login, bg=COLORS['text'], width=20)
    
    def reset_password_action(self):
        email = self.email_entry.get().strip()
        password = self.password_entry.get().strip()
        confirm = self.confirm_entry.get().strip()
        
        if not all([email, password, confirm]):
            messagebox.showerror("Error", "Please fill in all fields")
            return
        
        if password != confirm:
            messagebox.showerror("Error", "Passwords do not match")
            return
        
        success, msg = reset_password(email, password)
        if success:
            messagebox.showinfo("Success", msg)
            self.controller.show_frame(LoginFrame)
        else:
            messagebox.showerror("Error", msg)
    
    def back_to_login(self):
        self.controller.show_frame(LoginFrame)


class GuestContactViewFrame(BaseFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        
        self.all_contacts = []  # Store all contacts
        self.current_displayed_contacts = []  # Store currently displayed contacts
        self.selected_index = None
        
        # Header
        header_frame = tk.Frame(self, bg=COLORS['primary'], height=50)
        header_frame.pack(fill="x")
        
        title_label = tk.Label(
            header_frame,
            text="Browse Contacts (Guest Mode)",
            font=("Arial", 20, "bold"),
            fg="white",
            bg=COLORS['primary']
        )
        title_label.pack(pady=10)
        
        # Main content
        content_frame = tk.Frame(self, bg=COLORS['bg'])
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        info_label = tk.Label(
            content_frame,
            text="Guest mode allows you to view and search contacts.\nRegister or Login to add/edit/delete contacts.",
            font=("Arial", 12),
            bg=COLORS['bg'],
            fg=COLORS['text'],
            justify="center"
        )
        info_label.pack(pady=10)
        
        # Search frame
        search_frame = tk.Frame(content_frame, bg=COLORS['bg'])
        search_frame.pack(fill="x", pady=10)
        
        tk.Label(search_frame, text="Search:", font=("Arial", 10), bg=COLORS['bg']).pack(side="left", padx=5)
        self.search_var = tk.StringVar()
        search_entry = tk.Entry(search_frame, textvariable=self.search_var, width=30)
        search_entry.pack(side="left", padx=5)
        search_entry.bind('<Return>', lambda e: self.do_search())
        
        self.create_button(search_frame, "Search", self.do_search, width=10)
        self.create_button(search_frame, "View All", self.load_all_contacts, width=10)
        
        # Results frame with scrollbar
        results_frame = tk.Frame(content_frame, bg=COLORS['bg'])
        results_frame.pack(fill="both", expand=True, pady=10)
        
        scrollbar = ttk.Scrollbar(results_frame)
        scrollbar.pack(side="right", fill="y")
        
        self.contacts_listbox = tk.Listbox(
            results_frame,
            yscrollcommand=scrollbar.set,
            font=("Arial", 10),
            height=15
        )
        self.contacts_listbox.pack(fill="both", expand=True)
        self.contacts_listbox.bind('<<ListboxSelect>>', self.on_contact_select)
        scrollbar.config(command=self.contacts_listbox.yview)
        
        # Button frame
        button_frame = tk.Frame(content_frame, bg=COLORS['bg'])
        button_frame.pack(pady=10)
        
        self.create_button(button_frame, "View Details", self.view_contact_details, width=15)
        self.create_button(button_frame, "BACK TO LOGIN", self.back_to_login, width=15)
        
        # Load all contacts initially
        self.load_all_contacts()
    
    def get_all_contacts_from_file(self):
        """Load all contacts directly from JSON file"""
        try:
            with open("data/contacts.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading contacts: {e}")
            return []
    
    def load_all_contacts(self):
        """Load and display all contacts"""
        self.contacts_listbox.delete(0, tk.END)
        self.search_var.set("")
        
        try:
            self.all_contacts = self.get_all_contacts_from_file()
            self.current_displayed_contacts = self.all_contacts
            
            if not self.all_contacts:
                self.contacts_listbox.insert(tk.END, "No contacts found.")
            else:
                for contact in self.all_contacts:
                    # Map different field names that might exist
                    name = contact.get('full_name') or contact.get('name', 'Unknown')
                    phone = contact.get('phone_number') or contact.get('phone', 'No phone')
                    display_text = f"{name} - {phone}"
                    self.contacts_listbox.insert(tk.END, display_text)
                    self.contacts_listbox.itemconfig(tk.END, {'bg': COLORS['light']})
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load contacts: {str(e)}")
            self.contacts_listbox.insert(tk.END, f"Error: {str(e)}")
    
    def do_search(self):
        """Search contacts by name or phone"""
        search_term = self.search_var.get().strip().lower()
        if not search_term:
            messagebox.showwarning("Warning", "Please enter a search term.")
            return
        
        self.contacts_listbox.delete(0, tk.END)
        
        try:
            # Search through all contacts (not just user's)
            all_contacts = self.get_all_contacts_from_file()
            results = []
            
            for contact in all_contacts:
                name = contact.get('full_name') or contact.get('name', '')
                phone = contact.get('phone_number') or contact.get('phone', '')
                email = contact.get('email', '')
                
                if (search_term in name.lower() or 
                    search_term in phone.lower() or 
                    search_term in email.lower()):
                    results.append(contact)
            
            self.current_displayed_contacts = results
            
            if not results:
                self.contacts_listbox.insert(tk.END, "No contacts found.")
            else:
                for contact in results:
                    name = contact.get('full_name') or contact.get('name', 'Unknown')
                    phone = contact.get('phone_number') or contact.get('phone', 'No phone')
                    display_text = f"{name} - {phone}"
                    self.contacts_listbox.insert(tk.END, display_text)
                    self.contacts_listbox.itemconfig(tk.END, {'bg': COLORS['light']})
        except Exception as e:
            messagebox.showerror("Error", f"Search failed: {str(e)}")
            self.contacts_listbox.insert(tk.END, f"Error: {str(e)}")
    
    def on_contact_select(self, event):
        """Handle contact selection"""
        selection = self.contacts_listbox.curselection()
        if selection:
            self.selected_index = selection[0]
        else:
            self.selected_index = None
    
    def view_contact_details(self):
        """View selected contact details"""
        if self.selected_index is None:
            messagebox.showwarning("Warning", "Please select a contact.")
            return
        
        selection_text = self.contacts_listbox.get(self.selected_index)
        if selection_text == "No contacts found." or "Error:" in selection_text:
            messagebox.showinfo("Info", "No valid contact to view.")
            return
        
        try:
            if self.selected_index < len(self.current_displayed_contacts):
                contact = self.current_displayed_contacts[self.selected_index]
                
                # Map different field names
                name = contact.get('full_name') or contact.get('name', 'N/A')
                email = contact.get('email', 'N/A')
                phone = contact.get('phone_number') or contact.get('phone', 'N/A')
                address = contact.get('address', 'N/A')
                dob = contact.get('date_of_birth') or contact.get('birthday', 'N/A')
                
                details = f"""
Contact Details:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Name: {name}
Email: {email}
Phone: {phone}
Address: {address}
Date of Birth: {dob}
                """
                messagebox.showinfo("Contact Details", details)
            else:
                messagebox.showwarning("Error", "Contact not found.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to view details: {str(e)}")
    
    def back_to_login(self):
        """Go back to login frame"""
        self.controller.show_frame(LoginFrame)



class DashboardFrame(BaseFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        
        # Header
        header_frame = tk.Frame(self, bg=COLORS['primary'], height=60)
        header_frame.pack(fill="x")
        
        user_name = controller.current_user.get('full_name', 'User')
        title_label = tk.Label(
            header_frame,
            text=f"Welcome, {user_name}",
            font=("Arial", 20, "bold"),
            fg="white",
            bg=COLORS['primary']
        )
        title_label.pack(pady=10)
        
        # Main content
        content_frame = tk.Frame(self, bg=COLORS['bg'])
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Create grid of buttons
        button_grid = tk.Frame(content_frame, bg=COLORS['bg'])
        button_grid.pack(fill="both", expand=True)
        
        # Row 1
        row1 = tk.Frame(button_grid, bg=COLORS['bg'])
        row1.pack(fill="x", pady=10)
        
        self.create_dashboard_button(
            row1, "Contacts", "Manage your contacts",
            lambda: controller.show_frame(ContactManagementFrame), COLORS['primary']
        )
        
        self.create_dashboard_button(
            row1, "Groups", "Organize contacts into groups",
            lambda: controller.show_frame(GroupManagementFrame), COLORS['secondary']
        )
        
        # Row 2
        row2 = tk.Frame(button_grid, bg=COLORS['bg'])
        row2.pack(fill="x", pady=10)
        
        self.create_dashboard_button(
            row2, "Import/Export", "Import or export contacts",
            lambda: controller.show_frame(ImportExportFrame), COLORS['accent']
        )
        
        self.create_dashboard_button(
            row2, "Notifications", "View your notifications",
            lambda: controller.show_frame(NotificationFrame), COLORS['success']
        )
        
        # Row 3
        row3 = tk.Frame(button_grid, bg=COLORS['bg'])
        row3.pack(fill="x", pady=10)
        
        self.create_dashboard_button(
            row3, "Profile", "Update your profile",
            lambda: controller.show_frame(ProfileFrame), COLORS['text']
        )
        
        self.create_dashboard_button(
            row3, "Logout", "Exit the application",
            self.logout, COLORS['danger']
        )
    
    def create_dashboard_button(self, parent, title, desc, command, color):
        btn_frame = tk.Frame(parent, bg=color, relief="flat", padx=20, pady=20)
        btn_frame.pack(side="left", padx=10, fill="both", expand=True)
        
        btn = tk.Button(
            btn_frame,
            text=title,
            font=("Arial", 14, "bold"),
            bg=color,
            fg="white",
            relief="flat",
            cursor="hand2",
            command=command,
            padx=10,
            pady=10,
            wraplength=100
        )
        btn.pack(fill="both", expand=True)
        
        desc_label = tk.Label(
            btn_frame,
            text=desc,
            font=("Arial", 9),
            bg=color,
            fg="white",
            wraplength=100
        )
        desc_label.pack()
    
    def logout(self):
        self.controller.current_user = None
        self.controller.show_frame(LoginFrame)


class ContactManagementFrame(BaseFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        
        # Header
        self.create_header("Contact Management")
        
        # Main content
        content_frame = tk.Frame(self, bg=COLORS['bg'])
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Buttons
        button_frame = tk.Frame(content_frame, bg=COLORS['bg'])
        button_frame.pack(side="left", fill="y", padx=10)
        
        self.create_button(button_frame, "Add Contact", self.add_contact)
        self.create_button(button_frame, "View All", self.view_all)
        self.create_button(button_frame, "Search", self.search_contact)
        self.create_button(button_frame, "Edit", self.edit_contact)
        self.create_button(button_frame, "Delete", self.delete_contact)
        self.create_button(button_frame, "Back", self.back_to_dashboard, bg=COLORS['text'])
        
        # Content area
        self.content_area = tk.Frame(content_frame, bg="white", relief="solid", borderwidth=1)
        self.content_area.pack(side="right", fill="both", expand=True, padx=10)
        
        self.display_info("Select an option from the left menu")
    
    def display_info(self, text):
        for widget in self.content_area.winfo_children():
            widget.destroy()
        
        label = tk.Label(
            self.content_area,
            text=text,
            font=("Arial", 12),
            fg=COLORS['text'],
            bg="white",
            wraplength=400,
            justify="left"
        )
        label.pack(padx=20, pady=20)
    
    def add_contact(self):
        self.controller.show_frame(AddContactFrame)
    
    def view_all(self):
        user_id = self.controller.current_user.get('user_id')
        contacts = view_contacts(user_id)
        
        if not contacts:
            self.display_info("No contacts found")
            return
        
        self.display_contacts(contacts)
    
    def search_contact(self):
        self.controller.show_frame(SearchContactFrame)
    
    def edit_contact(self):
        self.controller.show_frame(EditContactFrame)
    
    def delete_contact(self):
        self.controller.show_frame(DeleteContactFrame)
    
    def display_contacts(self, contacts):
        for widget in self.content_area.winfo_children():
            widget.destroy()
        
        # Create treeview
        tree_frame = tk.Frame(self.content_area, bg="white")
        tree_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        tree = ttk.Treeview(
            tree_frame,
            columns=("ID", "Name", "Phone", "Email", "Groups"),
            height=15,
            show="headings"
        )
        
        tree.column("ID", width=30)
        tree.column("Name", width=100)
        tree.column("Phone", width=100)
        tree.column("Email", width=150)
        tree.column("Groups", width=100)
        
        tree.heading("ID", text="ID")
        tree.heading("Name", text="Name")
        tree.heading("Phone", text="Phone")
        tree.heading("Email", text="Email")
        tree.heading("Groups", text="Groups")
        
        for contact in contacts:
            tree.insert("", "end", values=(
                contact.get('contact_id'),
                contact.get('name', 'N/A'),
                contact.get('phone', 'N/A'),
                contact.get('email', 'N/A'),
                ", ".join(contact.get('groups', []))
            ))
        
        tree.pack(fill="both", expand=True)
    
    def back_to_dashboard(self):
        self.controller.show_frame(DashboardFrame)


class AddContactFrame(BaseFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        
        self.create_header("Add New Contact")
        
        content_frame = tk.Frame(self, bg=COLORS['bg'])
        content_frame.pack(fill="both", expand=True, padx=40, pady=20)
        
        # Input frame
        input_frame = tk.Frame(content_frame, bg=COLORS['bg'])
        input_frame.pack(fill="x", expand=False, pady=(0, 10))
        
        self.name_entry = self.create_entry(input_frame, "Contact Name:")
        self.phone_entry = self.create_entry(input_frame, "Phone Number:")
        self.email_entry = self.create_entry(input_frame, "Email Address:")
        self.address_entry = self.create_entry(input_frame, "Address (optional):")
        self.birthday_entry = self.create_entry(input_frame, "Birthday (YYYY-MM-DD):")
        self.notes_entry = self.create_entry(input_frame, "Notes (optional):")
        
        # Button frame
        button_frame = tk.Frame(input_frame, bg=COLORS['bg'])
        button_frame.pack(fill="x", expand=False, pady=20)
        
        add_btn = tk.Button(
            button_frame,
            text="ADD CONTACT",
            command=self.add_contact,
            bg=COLORS['primary'],
            fg="white",
            font=("Arial", 11, "bold"),
            padx=15,
            pady=10,
            relief="flat",
            cursor="hand2",
            width=20
        )
        add_btn.pack(side="left", padx=5)
        
        back_btn = tk.Button(
            button_frame,
            text="BACK",
            command=lambda: self.controller.show_frame(ContactManagementFrame),
            bg=COLORS['text'],
            fg="white",
            font=("Arial", 11, "bold"),
            padx=15,
            pady=10,
            relief="flat",
            cursor="hand2",
            width=20
        )
        back_btn.pack(side="left", padx=5)
    
    def add_contact(self):
        name = self.name_entry.get().strip()
        phone = self.phone_entry.get().strip()
        email = self.email_entry.get().strip()
        address = self.address_entry.get().strip()
        birthday = self.birthday_entry.get().strip()
        notes = self.notes_entry.get().strip()
        
        if not all([name, phone, email]):
            messagebox.showerror("Error", "Please fill in required fields")
            return
        
        user_id = self.controller.current_user.get('user_id')
        
        try:
            contact = add_contact(name, phone, email, user_id, address, notes, birthday)
            messagebox.showinfo("Success", f"Contact '{name}' added successfully!")
            self.controller.show_frame(ContactManagementFrame)
        except Exception as e:
            messagebox.showerror("Error", str(e))


class SearchContactFrame(BaseFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        
        self.create_header("Search Contacts")
        
        content_frame = tk.Frame(self, bg=COLORS['bg'])
        content_frame.pack(fill="both", expand=True, padx=40, pady=20)
        
        # Input frame to hold all search inputs and buttons
        input_frame = tk.Frame(content_frame, bg=COLORS['bg'])
        input_frame.pack(fill="x", expand=False, pady=(0, 10))
        
        # Search type
        tk.Label(input_frame, text="Search Type:", font=("Arial", 11), bg=COLORS['bg']).pack(anchor="w", pady=(10, 5))
        
        search_frame = tk.Frame(input_frame, bg=COLORS['bg'])
        search_frame.pack(anchor="w", pady=10)
        
        self.search_type = tk.StringVar(value="all")
        
        for type_val, label in [("all", "All Fields"), ("name", "Name"), ("phone", "Phone"), ("email", "Email"), ("group", "Group")]:
            tk.Radiobutton(
                search_frame,
                text=label,
                variable=self.search_type,
                value=type_val,
                font=("Arial", 10),
                bg=COLORS['bg']
            ).pack(side="left", padx=10)
        
        # Keyword
        self.keyword_entry = self.create_entry(input_frame, "Search Keyword:")
        
        # Button frame
        button_frame = tk.Frame(input_frame, bg=COLORS['bg'])
        button_frame.pack(fill="x", expand=False, pady=20)
        
        search_btn = tk.Button(
            button_frame,
            text="SEARCH",
            command=self.search,
            bg=COLORS['primary'],
            fg="white",
            font=("Arial", 11, "bold"),
            padx=15,
            pady=10,
            relief="flat",
            cursor="hand2",
            width=20
        )
        search_btn.pack(side="left", padx=5)
        
        back_btn = tk.Button(
            button_frame,
            text="BACK",
            command=lambda: self.controller.show_frame(ContactManagementFrame),
            bg=COLORS['text'],
            fg="white",
            font=("Arial", 11, "bold"),
            padx=15,
            pady=10,
            relief="flat",
            cursor="hand2",
            width=20
        )
        back_btn.pack(side="left", padx=5)
        
        # Results area
        self.results_frame = tk.Frame(self, bg="white", relief="solid", borderwidth=1)
        self.results_frame.pack(fill="both", expand=True, padx=20, pady=20)
    
    def search(self):
        keyword = self.keyword_entry.get().strip()
        search_type = self.search_type.get()
        user_id = self.controller.current_user.get('user_id')
        
        if not keyword:
            messagebox.showerror("Error", "Please enter a search keyword")
            return
        
        results = search_contacts(user_id, keyword, search_type)
        self.display_results(results)
    
    def display_results(self, contacts):
        for widget in self.results_frame.winfo_children():
            widget.destroy()
        
        if not contacts:
            label = tk.Label(
                self.results_frame,
                text="No contacts found",
                font=("Arial", 12),
                bg="white"
            )
            label.pack(pady=20)
            return
        
        tree_frame = tk.Frame(self.results_frame, bg="white")
        tree_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        tree = ttk.Treeview(
            tree_frame,
            columns=("ID", "Name", "Phone", "Email"),
            height=10,
            show="headings"
        )
        
        tree.column("ID", width=30)
        tree.column("Name", width=150)
        tree.column("Phone", width=120)
        tree.column("Email", width=150)
        
        tree.heading("ID", text="ID")
        tree.heading("Name", text="Name")
        tree.heading("Phone", text="Phone")
        tree.heading("Email", text="Email")
        
        for contact in contacts:
            tree.insert("", "end", values=(
                contact.get('contact_id'),
                contact.get('name'),
                contact.get('phone'),
                contact.get('email')
            ))
        
        tree.pack(fill="both", expand=True)


class EditContactFrame(BaseFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        
        self.create_header("Edit Contact")
        
        content_frame = tk.Frame(self, bg=COLORS['bg'])
        content_frame.pack(fill="both", expand=True, padx=40, pady=20)
        
        # Input frame for all fields
        input_frame = tk.Frame(content_frame, bg=COLORS['bg'])
        input_frame.pack(fill="x", expand=False, pady=(0, 10))
        
        # Select contact
        tk.Label(input_frame, text="Contact ID to Edit:", font=("Arial", 11), bg=COLORS['bg']).pack(anchor="w", pady=(10, 5))
        self.id_entry = self.create_entry(input_frame, "")
        
        # Contact details
        self.name_entry = self.create_entry(input_frame, "Contact Name:")
        self.phone_entry = self.create_entry(input_frame, "Phone Number:")
        self.email_entry = self.create_entry(input_frame, "Email Address:")
        self.address_entry = self.create_entry(input_frame, "Address:")
        self.birthday_entry = self.create_entry(input_frame, "Birthday:")
        self.notes_entry = self.create_entry(input_frame, "Notes:")
        
        # Button frame
        button_frame = tk.Frame(input_frame, bg=COLORS['bg'])
        button_frame.pack(fill="x", expand=False, pady=20)
        
        save_btn = tk.Button(
            button_frame,
            text="SAVE CHANGES",
            command=self.save_changes,
            bg=COLORS['primary'],
            fg="white",
            font=("Arial", 11, "bold"),
            padx=15,
            pady=10,
            relief="flat",
            cursor="hand2",
            width=20
        )
        save_btn.pack(side="left", padx=5)
        
        back_btn = tk.Button(
            button_frame,
            text="BACK",
            command=lambda: self.controller.show_frame(ContactManagementFrame),
            bg=COLORS['text'],
            fg="white",
            font=("Arial", 11, "bold"),
            padx=15,
            pady=10,
            relief="flat",
            cursor="hand2",
            width=20
        )
        back_btn.pack(side="left", padx=5)
    
    def save_changes(self):
        try:
            contact_id = int(self.id_entry.get())
        except:
            messagebox.showerror("Error", "Please enter a valid contact ID")
            return
        
        user_id = self.controller.current_user.get('user_id')
        name = self.name_entry.get().strip() or None
        phone = self.phone_entry.get().strip() or None
        email = self.email_entry.get().strip() or None
        address = self.address_entry.get().strip() or None
        birthday = self.birthday_entry.get().strip() or None
        notes = self.notes_entry.get().strip() or None
        
        success, msg = edit_contact(
            contact_id, user_id,
            name=name, phone=phone, email=email,
            address=address, birthday=birthday, notes=notes
        )
        
        if success:
            messagebox.showinfo("Success", msg)
            self.controller.show_frame(ContactManagementFrame)
        else:
            messagebox.showerror("Error", msg)


class DeleteContactFrame(BaseFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        
        self.create_header("Delete Contact")
        
        content_frame = tk.Frame(self, bg=COLORS['bg'])
        content_frame.pack(fill="both", expand=True, padx=40, pady=20)
        
        input_frame = tk.Frame(content_frame, bg=COLORS['bg'])
        input_frame.pack(fill="x", expand=False, pady=(0, 10))
        
        warning = tk.Label(
            input_frame,
            text="Warning: This action cannot be undone!",
            font=("Arial", 12, "bold"),
            bg=COLORS['bg'],
            fg=COLORS['danger']
        )
        warning.pack(pady=20)
        
        self.id_entry = self.create_entry(input_frame, "Contact ID to Delete:")
        
        # Button frame
        button_frame = tk.Frame(input_frame, bg=COLORS['bg'])
        button_frame.pack(fill="x", expand=False, pady=20)
        
        delete_btn = tk.Button(
            button_frame,
            text="DELETE",
            command=self.delete_contact,
            bg=COLORS['danger'],
            fg="white",
            font=("Arial", 11, "bold"),
            padx=15,
            pady=10,
            relief="flat",
            cursor="hand2",
            width=20
        )
        delete_btn.pack(side="left", padx=5)
        
        back_btn = tk.Button(
            button_frame,
            text="BACK",
            command=lambda: self.controller.show_frame(ContactManagementFrame),
            bg=COLORS['text'],
            fg="white",
            font=("Arial", 11, "bold"),
            padx=15,
            pady=10,
            relief="flat",
            cursor="hand2",
            width=20
        )
        back_btn.pack(side="left", padx=5)
    
    def delete_contact(self):
        try:
            contact_id = int(self.id_entry.get())
        except:
            messagebox.showerror("Error", "Please enter a valid contact ID")
            return
        
        if not messagebox.askyesno("Confirm", "Are you sure you want to delete this contact?"):
            return
        
        user_id = self.controller.current_user.get('user_id')
        success, msg = delete_contact(contact_id, user_id)
        
        if success:
            messagebox.showinfo("Success", msg)
            self.controller.show_frame(ContactManagementFrame)
        else:
            messagebox.showerror("Error", msg)


class GroupManagementFrame(BaseFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        
        self.create_header("Group Management")
        
        content_frame = tk.Frame(self, bg=COLORS['bg'])
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Buttons
        button_frame = tk.Frame(content_frame, bg=COLORS['bg'])
        button_frame.pack(side="left", fill="y", padx=10)
        
        self.create_button(button_frame, "Create Group", self.create_group)
        self.create_button(button_frame, "View Groups", self.view_groups)
        self.create_button(button_frame, "Add to Group", self.add_to_group)
        self.create_button(button_frame, "Remove from Group", self.remove_from_group)
        self.create_button(button_frame, "Delete Group", self.delete_group)
        self.create_button(button_frame, "Back", self.back_to_dashboard, bg=COLORS['text'])
        
        # Content area
        self.content_area = tk.Frame(content_frame, bg="white", relief="solid", borderwidth=1)
        self.content_area.pack(side="right", fill="both", expand=True, padx=10)
    
    def create_group(self):
        self.controller.show_frame(CreateGroupFrame)
    
    def view_groups(self):
        user_id = self.controller.current_user.get('user_id')
        groups = get_user_groups(user_id)
        
        for widget in self.content_area.winfo_children():
            widget.destroy()
        
        if not groups:
            label = tk.Label(self.content_area, text="No groups found", bg="white", font=("Arial", 12))
            label.pack(pady=20)
            return
        
        text = "Your Groups:\n\n"
        for g in groups:
            contacts = get_contacts_by_group(user_id, g.get('name'))
            text += f"• {g.get('name')} ({len(contacts)} contacts)\n"
        
        label = tk.Label(self.content_area, text=text, bg="white", font=("Arial", 11), justify="left")
        label.pack(padx=20, pady=20)
    
    def add_to_group(self):
        self.controller.show_frame(AddToGroupFrame)
    
    def remove_from_group(self):
        self.controller.show_frame(RemoveFromGroupFrame)
    
    def delete_group(self):
        self.controller.show_frame(DeleteGroupFrame)
    
    def back_to_dashboard(self):
        self.controller.show_frame(DashboardFrame)


class CreateGroupFrame(BaseFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        
        self.create_header("Create New Group")
        
        content_frame = tk.Frame(self, bg=COLORS['bg'])
        content_frame.pack(fill="both", expand=True, padx=40, pady=20)
        
        # Input frame
        input_frame = tk.Frame(content_frame, bg=COLORS['bg'])
        input_frame.pack(fill="x", expand=False, pady=(0, 10))
        
        self.name_entry = self.create_entry(input_frame, "Group Name:")
        
        # Button frame
        button_frame = tk.Frame(input_frame, bg=COLORS['bg'])
        button_frame.pack(fill="x", expand=False, pady=20)
        
        create_btn = tk.Button(
            button_frame,
            text="CREATE",
            command=self.create_group,
            bg=COLORS['primary'],
            fg="white",
            font=("Arial", 11, "bold"),
            padx=15,
            pady=10,
            relief="flat",
            cursor="hand2",
            width=20
        )
        create_btn.pack(side="left", padx=5)
        
        back_btn = tk.Button(
            button_frame,
            text="BACK",
            command=lambda: self.controller.show_frame(GroupManagementFrame),
            bg=COLORS['text'],
            fg="white",
            font=("Arial", 11, "bold"),
            padx=15,
            pady=10,
            relief="flat",
            cursor="hand2",
            width=20
        )
        back_btn.pack(side="left", padx=5)
    
    def create_group(self):
        name = self.name_entry.get().strip()
        
        if not name:
            messagebox.showerror("Error", "Please enter a group name")
            return
        
        user_id = self.controller.current_user.get('user_id')
        
        try:
            add_group(name, user_id)
            messagebox.showinfo("Success", f"Group '{name}' created successfully!")
            self.controller.show_frame(GroupManagementFrame)
        except Exception as e:
            messagebox.showerror("Error", str(e))


class AddToGroupFrame(BaseFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        
        self.create_header("Add Contact to Group")
        
        content_frame = tk.Frame(self, bg=COLORS['bg'])
        content_frame.pack(fill="both", expand=True, padx=40, pady=20)
        
        # Input frame
        input_frame = tk.Frame(content_frame, bg=COLORS['bg'])
        input_frame.pack(fill="x", expand=False, pady=(0, 10))
        
        self.contact_id_entry = self.create_entry(input_frame, "Contact ID:")
        self.group_name_entry = self.create_entry(input_frame, "Group Name:")
        
        # Button frame
        button_frame = tk.Frame(input_frame, bg=COLORS['bg'])
        button_frame.pack(fill="x", expand=False, pady=20)
        
        add_btn = tk.Button(
            button_frame,
            text="ADD",
            command=self.add_to_group,
            bg=COLORS['primary'],
            fg="white",
            font=("Arial", 11, "bold"),
            padx=15,
            pady=10,
            relief="flat",
            cursor="hand2",
            width=20
        )
        add_btn.pack(side="left", padx=5)
        
        back_btn = tk.Button(
            button_frame,
            text="BACK",
            command=lambda: self.controller.show_frame(GroupManagementFrame),
            bg=COLORS['text'],
            fg="white",
            font=("Arial", 11, "bold"),
            padx=15,
            pady=10,
            relief="flat",
            cursor="hand2",
            width=20
        )
        back_btn.pack(side="left", padx=5)
    
    def add_to_group(self):
        try:
            contact_id = int(self.contact_id_entry.get())
        except:
            messagebox.showerror("Error", "Please enter a valid contact ID")
            return
        
        group_name = self.group_name_entry.get().strip()
        user_id = self.controller.current_user.get('user_id')
        
        success, msg = add_contact_to_group(contact_id, group_name, user_id)
        
        if success:
            messagebox.showinfo("Success", msg)
            self.controller.show_frame(GroupManagementFrame)
        else:
            messagebox.showerror("Error", msg)


class RemoveFromGroupFrame(BaseFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        
        self.create_header("Remove Contact from Group")
        
        content_frame = tk.Frame(self, bg=COLORS['bg'])
        content_frame.pack(fill="both", expand=True, padx=40, pady=20)
        
        # Input frame
        input_frame = tk.Frame(content_frame, bg=COLORS['bg'])
        input_frame.pack(fill="x", expand=False, pady=(0, 10))
        
        self.contact_id_entry = self.create_entry(input_frame, "Contact ID:")
        self.group_name_entry = self.create_entry(input_frame, "Group Name:")
        
        # Button frame
        button_frame = tk.Frame(input_frame, bg=COLORS['bg'])
        button_frame.pack(fill="x", expand=False, pady=20)
        
        remove_btn = tk.Button(
            button_frame,
            text="REMOVE",
            command=self.remove_from_group,
            bg=COLORS['primary'],
            fg="white",
            font=("Arial", 11, "bold"),
            padx=15,
            pady=10,
            relief="flat",
            cursor="hand2",
            width=20
        )
        remove_btn.pack(side="left", padx=5)
        
        back_btn = tk.Button(
            button_frame,
            text="BACK",
            command=lambda: self.controller.show_frame(GroupManagementFrame),
            bg=COLORS['text'],
            fg="white",
            font=("Arial", 11, "bold"),
            padx=15,
            pady=10,
            relief="flat",
            cursor="hand2",
            width=20
        )
        back_btn.pack(side="left", padx=5)
    
    def remove_from_group(self):
        try:
            contact_id = int(self.contact_id_entry.get())
        except:
            messagebox.showerror("Error", "Please enter a valid contact ID")
            return
        
        group_name = self.group_name_entry.get().strip()
        user_id = self.controller.current_user.get('user_id')
        
        success, msg = remove_contact_from_group(contact_id, group_name, user_id)
        
        if success:
            messagebox.showinfo("Success", msg)
            self.controller.show_frame(GroupManagementFrame)
        else:
            messagebox.showerror("Error", msg)


class DeleteGroupFrame(BaseFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        
        self.create_header("Delete Group")
        
        content_frame = tk.Frame(self, bg=COLORS['bg'])
        content_frame.pack(fill="both", expand=True, padx=40, pady=20)
        
        # Input frame
        input_frame = tk.Frame(content_frame, bg=COLORS['bg'])
        input_frame.pack(fill="x", expand=False, pady=(0, 10))
        
        warning = tk.Label(
            input_frame,
            text="Warning: This will delete the group but not the contacts!",
            font=("Arial", 12),
            bg=COLORS['bg'],
            fg=COLORS['danger']
        )
        warning.pack(pady=20)
        
        self.group_name_entry = self.create_entry(input_frame, "Group Name:")
        
        # Button frame
        button_frame = tk.Frame(input_frame, bg=COLORS['bg'])
        button_frame.pack(fill="x", expand=False, pady=20)
        
        delete_btn = tk.Button(
            button_frame,
            text="DELETE",
            command=self.delete_group,
            bg=COLORS['danger'],
            fg="white",
            font=("Arial", 11, "bold"),
            padx=15,
            pady=10,
            relief="flat",
            cursor="hand2",
            width=20
        )
        delete_btn.pack(side="left", padx=5)
        
        back_btn = tk.Button(
            button_frame,
            text="BACK",
            command=lambda: self.controller.show_frame(GroupManagementFrame),
            bg=COLORS['text'],
            fg="white",
            font=("Arial", 11, "bold"),
            padx=15,
            pady=10,
            relief="flat",
            cursor="hand2",
            width=20
        )
        back_btn.pack(side="left", padx=5)
    
    def delete_group(self):
        group_name = self.group_name_entry.get().strip()
        user_id = self.controller.current_user.get('user_id')
        
        if not messagebox.askyesno("Confirm", f"Delete group '{group_name}'?"):
            return
        
        group = get_group_by_name(group_name, user_id)
        if group:
            success, msg = delete_group(group.get('group_id'), user_id)
            if success:
                messagebox.showinfo("Success", msg)
                self.controller.show_frame(GroupManagementFrame)
            else:
                messagebox.showerror("Error", msg)
        else:
            messagebox.showerror("Error", "Group not found")


class ImportExportFrame(BaseFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        
        self.create_header("Import/Export Contacts")
        
        content_frame = tk.Frame(self, bg=COLORS['bg'])
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Buttons
        button_frame = tk.Frame(content_frame, bg=COLORS['bg'])
        button_frame.pack(side="left", fill="y", padx=10)
        
        self.create_button(button_frame, "Export All", self.export_all)
        self.create_button(button_frame, "Export by Group", self.export_group)
        self.create_button(button_frame, "Import", self.import_contacts)
        self.create_button(button_frame, "View History", self.view_history)
        self.create_button(button_frame, "Back", self.back_to_dashboard, bg=COLORS['text'])
        
        # Content area
        self.content_area = tk.Frame(content_frame, bg="white", relief="solid", borderwidth=1)
        self.content_area.pack(side="right", fill="both", expand=True, padx=10)
    
    def export_all(self):
        user_id = self.controller.current_user.get('user_id')
        contacts = view_contacts(user_id)
        
        if not contacts:
            messagebox.showerror("Error", "No contacts to export")
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filename:
            success, msg = export_contacts(contacts, filename)
            if success:
                messagebox.showinfo("Success", msg)
                add_history_entry(user_id, "export", filename, len(contacts), "success")
            else:
                messagebox.showerror("Error", msg)
    
    def export_group(self):
        user_id = self.controller.current_user.get('user_id')
        groups = get_user_groups(user_id)
        
        if not groups:
            messagebox.showerror("Error", "No groups available")
            return
        
        group_name = simpledialog.askstring("Export Group", "Enter group name:")
        
        if group_name:
            filename = filedialog.asksaveasfilename(
                defaultextension=".json",
                filetypes=[("JSON files", "*.json")]
            )
            
            if filename:
                success, msg = export_contacts_by_group(user_id, group_name, filename)
                if success:
                    messagebox.showinfo("Success", msg)
                else:
                    messagebox.showerror("Error", msg)
    
    def import_contacts(self):
        filename = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filename:
            user_id = self.controller.current_user.get('user_id')
            success, result = import_contacts(user_id, filename)
            
            if success:
                summary, details = result
                messagebox.showinfo("Import Results", summary)
                add_history_entry(user_id, "import", filename, details.get("success", 0), "success")
            else:
                messagebox.showerror("Import Failed", result)
    
    def view_history(self):
        user_id = self.controller.current_user.get('user_id')
        history = get_user_history(user_id)
        
        for widget in self.content_area.winfo_children():
            widget.destroy()
        
        if not history:
            label = tk.Label(self.content_area, text="No history found", bg="white", font=("Arial", 12))
            label.pack(pady=20)
            return
        
        tree_frame = tk.Frame(self.content_area, bg="white")
        tree_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        tree = ttk.Treeview(
            tree_frame,
            columns=("Date", "Action", "File", "Count", "Status"),
            height=10,
            show="headings"
        )
        
        tree.column("Date", width=100)
        tree.column("Action", width=80)
        tree.column("File", width=150)
        tree.column("Count", width=60)
        tree.column("Status", width=80)
        
        for col in ["Date", "Action", "File", "Count", "Status"]:
            tree.heading(col, text=col)
        
        for h in history:
            tree.insert("", "end", values=(
                h.get("timestamp", "").split("T")[0],
                h.get("action", "").upper(),
                h.get("file_name", ""),
                h.get("count", ""),
                h.get("status", "").upper()
            ))
        
        tree.pack(fill="both", expand=True)
    
    def back_to_dashboard(self):
        self.controller.show_frame(DashboardFrame)


class NotificationFrame(BaseFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        
        self.create_header("Notifications")
        
        content_frame = tk.Frame(self, bg=COLORS['bg'])
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Buttons
        button_frame = tk.Frame(content_frame, bg=COLORS['bg'])
        button_frame.pack(side="left", fill="y", padx=10)
        
        self.create_button(button_frame, "All Notifications", self.view_all)
        self.create_button(button_frame, "Unread", self.view_unread)
        self.create_button(button_frame, "Mark as Read", self.mark_as_read)
        self.create_button(button_frame, "Clear All", self.clear_all)
        self.create_button(button_frame, "Back", self.back_to_dashboard, bg=COLORS['text'])
        
        # Content area
        self.content_area = tk.Frame(content_frame, bg="white", relief="solid", borderwidth=1)
        self.content_area.pack(side="right", fill="both", expand=True, padx=10)
    
    def view_all(self):
        user_id = self.controller.current_user.get('user_id')
        notifications = get_user_notifications(user_id)
        self.display_notifications(notifications)
    
    def view_unread(self):
        user_id = self.controller.current_user.get('user_id')
        notifications = get_unread_notifications(user_id)
        self.display_notifications(notifications)
    
    def display_notifications(self, notifications):
        for widget in self.content_area.winfo_children():
            widget.destroy()
        
        if not notifications:
            label = tk.Label(self.content_area, text="No notifications", bg="white", font=("Arial", 12))
            label.pack(pady=20)
            return
        
        text_frame = tk.Frame(self.content_area, bg="white")
        text_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        text_widget = tk.Text(text_frame, font=("Arial", 10), wrap="word", height=15)
        text_widget.pack(fill="both", expand=True)
        
        for notif in notifications:
            status = "[UNREAD]" if not notif.get("is_read") else "[READ]"
            text_widget.insert("end", f"{status} {notif.get('notification_type', 'system').upper()}\n")
            text_widget.insert("end", f"Message: {notif.get('message')}\n")
            text_widget.insert("end", f"Date: {notif.get('created_at', '').split('T')[0]}\n\n")
        
        text_widget.config(state="disabled")
    
    def mark_as_read(self):
        user_id = self.controller.current_user.get('user_id')
        mark_all_notifications_as_read(user_id)
        messagebox.showinfo("Success", "All notifications marked as read")
        self.view_all()
    
    def clear_all(self):
        if not messagebox.askyesno("Confirm", "Clear all notifications?"):
            return
        
        user_id = self.controller.current_user.get('user_id')
        clear_user_notifications(user_id)
        messagebox.showinfo("Success", "All notifications cleared")
        self.view_all()
    
    def back_to_dashboard(self):
        self.controller.show_frame(DashboardFrame)


class ProfileFrame(BaseFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        
        self.create_header("Profile Management")
        
        content_frame = tk.Frame(self, bg=COLORS['bg'])
        content_frame.pack(fill="both", expand=True, padx=40, pady=20)
        
        # Display current info
        user = controller.current_user
        info_text = f"Current Information:\n\n"
        info_text += f"Full Name: {user.get('full_name')}\n"
        info_text += f"Email: {user.get('email')}\n"
        info_text += f"Phone: {user.get('phone')}\n"
        
        info_label = tk.Label(
            content_frame,
            text=info_text,
            font=("Arial", 11),
            bg=COLORS['bg'],
            justify="left",
            fg=COLORS['text']
        )
        info_label.pack(pady=20, anchor="w")
        
        separator = tk.Frame(content_frame, bg=COLORS['border'], height=1)
        separator.pack(fill="x", pady=20)
        
        # Update fields
        self.name_entry = self.create_entry(content_frame, "New Full Name:")
        self.email_entry = self.create_entry(content_frame, "New Email:")
        self.phone_entry = self.create_entry(content_frame, "New Phone:")
        
        # Button frame
        button_frame = tk.Frame(content_frame, bg=COLORS['bg'])
        button_frame.pack(pady=20)
        
        self.create_button(button_frame, "SAVE CHANGES", self.save_changes, width=20)
        self.create_button(button_frame, "BACK", self.back_to_dashboard, bg=COLORS['text'], width=20)
    
    def save_changes(self):
        user_id = self.controller.current_user.get('user_id')
        name = self.name_entry.get().strip() or None
        email = self.email_entry.get().strip() or None
        phone = self.phone_entry.get().strip() or None
        
        if name:
            success, msg = update_user_profile(user_id, full_name=name)
            if success:
                self.controller.current_user['full_name'] = name
        
        if email:
            success, msg = update_user_profile(user_id, email=email)
            if success:
                self.controller.current_user['email'] = email
        
        if phone:
            success, msg = update_user_profile(user_id, phone=phone)
            if success:
                self.controller.current_user['phone'] = phone
        
        messagebox.showinfo("Success", "Profile updated successfully!")
        self.controller.show_frame(DashboardFrame)
    
    def back_to_dashboard(self):
        self.controller.show_frame(DashboardFrame)


if __name__ == "__main__":
    from tkinter import simpledialog
    app = PhoneBookApp()
    app.mainloop()
