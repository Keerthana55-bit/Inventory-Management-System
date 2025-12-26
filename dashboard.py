from tkinter import *
from PIL import Image, ImageTk
from tkinter import messagebox
from tkinter import ttk
import time
import sqlite3
import os
from employee import employeeClass
from supplier import supplierClass
from category import categoryClass
from product import productClass
from sales import salesClass
from billing import billClass

class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1000x600+200+100")
        self.root.title("IMS - Login System")
        self.root.resizable(True, True)
        self.root.config(bg="#0a0e27")
        
        # Create users table if not exists
        self.create_users_table()
        
        # Left side - Branding
        left_frame = Frame(self.root, bg="#1a1f3a", width=500)
        left_frame.pack(side=LEFT, fill=BOTH, expand=True)
        
        Label(left_frame, text="IMS", font=("Consolas", 48, "bold"), 
              bg="#1a1f3a", fg="#00d4ff").pack(pady=80)
        Label(left_frame, text="INVENTORY MANAGEMENT\nSYSTEM", 
              font=("Segoe UI", 20, "bold"), bg="#1a1f3a", fg="#ffffff").pack()
        Label(left_frame, text="Command Center Access", 
              font=("Segoe UI", 12), bg="#1a1f3a", fg="#7f8fa6").pack(pady=20)
        
        # Right side - Login Form
        right_frame = Frame(self.root, bg="#0a0e27", width=500)
        right_frame.pack(side=RIGHT, fill=BOTH, expand=True)
        
        # Login form container
        login_container = Frame(right_frame, bg="#0a0e27")
        login_container.place(relx=0.5, rely=0.5, anchor=CENTER)
        
        Label(login_container, text="LOGIN", font=("Consolas", 28, "bold"),
              bg="#0a0e27", fg="#00d4ff").pack(pady=20)
        
        # Username
        Label(login_container, text="USERNAME", font=("Segoe UI", 10, "bold"),
              bg="#0a0e27", fg="#7f8fa6").pack(anchor=W, pady=(20,5))
        self.txt_username = Entry(login_container, font=("Segoe UI", 12),
                                 bg="#1a1f3a", fg="#ffffff", 
                                 insertbackground="#00d4ff", bd=0,
                                 relief=FLAT, width=30)
        self.txt_username.pack(ipady=10, pady=5)
        Frame(login_container, bg="#00d4ff", height=2, width=300).pack()
        
        # Password
        Label(login_container, text="PASSWORD", font=("Segoe UI", 10, "bold"),
              bg="#0a0e27", fg="#7f8fa6").pack(anchor=W, pady=(20,5))
        self.txt_password = Entry(login_container, font=("Segoe UI", 12),
                                 bg="#1a1f3a", fg="#ffffff", 
                                 insertbackground="#00d4ff", bd=0,
                                 relief=FLAT, width=30, show="●")
        self.txt_password.pack(ipady=10, pady=5)
        Frame(login_container, bg="#00d4ff", height=2, width=300).pack()
        
        # Bind Enter key to login
        self.txt_password.bind('<Return>', lambda e: self.login())
        
        # Login Button
        btn_login = Button(login_container, text="LOGIN", 
                          font=("Segoe UI", 12, "bold"),
                          bg="#00d4ff", fg="#0a0e27", cursor="hand2", bd=0,
                          activebackground="#00a8cc", activeforeground="#ffffff",
                          command=self.login, width=30, pady=12)
        btn_login.pack(pady=30)
        
        # Register link
        register_frame = Frame(login_container, bg="#0a0e27")
        register_frame.pack(pady=5)
        
        Label(register_frame, text="Don't have an account?", 
              font=("Segoe UI", 9), bg="#0a0e27", fg="#7f8fa6").pack(side=LEFT)
        
        btn_register_link = Button(register_frame, text="Register Here", 
                                   font=("Segoe UI", 9, "bold"),
                                   bg="#0a0e27", fg="#00d4ff", cursor="hand2", 
                                   bd=0, activebackground="#0a0e27", 
                                   activeforeground="#00a8cc",
                                   command=self.open_register)
        btn_register_link.pack(side=LEFT, padx=5)
        
        # Footer info
        Label(login_container, text="Default: admin / admin123", 
              font=("Segoe UI", 9), bg="#0a0e27", fg="#535c68").pack(pady=10)
        
        # Focus on username
        self.txt_username.focus()
    
    def open_register(self):
        """Open registration window"""
        self.root.destroy()
        register_root = Tk()
        RegisterWindow(register_root)
        register_root.mainloop()
    
    def create_users_table(self):
        """Create users table and add default admin if not exists"""
        try:
            con = sqlite3.connect(database=r'ims.db')
            cur = con.cursor()
            
            # Create users table
            cur.execute("""CREATE TABLE IF NOT EXISTS users(
                        uid INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE,
                        password TEXT,
                        role TEXT
                        )""")
            
            # Check if admin exists
            cur.execute("SELECT * FROM users WHERE username=?", ('admin',))
            if cur.fetchone() is None:
                # Add default admin user
                cur.execute("INSERT INTO users(username, password, role) VALUES(?,?,?)",
                          ('admin', 'admin123', 'Admin'))
                con.commit()
            
            con.close()
        except Exception as ex:
            messagebox.showerror("Error", f"Error creating users table: {str(ex)}")
    
    def login(self):
        """Authenticate user and open dashboard"""
        if self.txt_username.get() == "" or self.txt_password.get() == "":
            messagebox.showerror("Error", "All fields are required", parent=self.root)
        else:
            try:
                con = sqlite3.connect(database=r'ims.db')
                cur = con.cursor()
                
                cur.execute("SELECT * FROM users WHERE username=? AND password=?",
                          (self.txt_username.get(), self.txt_password.get()))
                user = cur.fetchone()
                
                if user is None:
                    messagebox.showerror("Error", "Invalid Username or Password", 
                                       parent=self.root)
                else:
                    # Store logged in user info
                    self.username = user[1]
                    self.role = user[3]
                    
                    # Close login window and open dashboard
                    self.root.destroy()
                    dashboard_root = Tk()
                    IMS(dashboard_root, self.username, self.role)
                    dashboard_root.mainloop()
                
                con.close()
            except Exception as ex:
                messagebox.showerror("Error", f"Error: {str(ex)}", parent=self.root)


class RegisterWindow:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1000x700+200+50")
        self.root.title("IMS - Register New User")
        self.root.resizable(True, True)
        self.root.config(bg="#0a0e27")
        
        # Left side - Branding
        left_frame = Frame(self.root, bg="#1a1f3a", width=500)
        left_frame.pack(side=LEFT, fill=BOTH, expand=True)
        
        Label(left_frame, text="IMS", font=("Consolas", 48, "bold"), 
              bg="#1a1f3a", fg="#00d4ff").pack(pady=60)
        Label(left_frame, text="CREATE NEW ACCOUNT", 
              font=("Segoe UI", 20, "bold"), bg="#1a1f3a", fg="#ffffff").pack()
        Label(left_frame, text="Join the Command Center", 
              font=("Segoe UI", 12), bg="#1a1f3a", fg="#7f8fa6").pack(pady=20)
        
        # Info text
        info_text = """
        Register to access:
        
        • Employee Management
        • Supplier Management
        • Category Management
        • Product Management
        • Billing System
        • Sales Records
        """
        Label(left_frame, text=info_text, 
              font=("Segoe UI", 11), bg="#1a1f3a", fg="#ffffff",
              justify=LEFT).pack(pady=30, padx=40)
        
        # Right side - Registration Form
        right_frame = Frame(self.root, bg="#0a0e27", width=500)
        right_frame.pack(side=RIGHT, fill=BOTH, expand=True)
        
        # Registration form container
        register_container = Frame(right_frame, bg="#0a0e27")
        register_container.place(relx=0.5, rely=0.5, anchor=CENTER)
        
        Label(register_container, text="REGISTER", font=("Consolas", 28, "bold"),
              bg="#0a0e27", fg="#00d4ff").pack(pady=15)
        
        # Username
        Label(register_container, text="USERNAME", font=("Segoe UI", 10, "bold"),
              bg="#0a0e27", fg="#7f8fa6").pack(anchor=W, pady=(15,5))
        self.txt_username = Entry(register_container, font=("Segoe UI", 12),
                                 bg="#1a1f3a", fg="#ffffff", 
                                 insertbackground="#00d4ff", bd=0,
                                 relief=FLAT, width=30)
        self.txt_username.pack(ipady=10, pady=5)
        Frame(register_container, bg="#00d4ff", height=2, width=300).pack()
        
        # Password
        Label(register_container, text="PASSWORD", font=("Segoe UI", 10, "bold"),
              bg="#0a0e27", fg="#7f8fa6").pack(anchor=W, pady=(15,5))
        self.txt_password = Entry(register_container, font=("Segoe UI", 12),
                                 bg="#1a1f3a", fg="#ffffff", 
                                 insertbackground="#00d4ff", bd=0,
                                 relief=FLAT, width=30, show="●")
        self.txt_password.pack(ipady=10, pady=5)
        Frame(register_container, bg="#00d4ff", height=2, width=300).pack()
        
        # Confirm Password
        Label(register_container, text="CONFIRM PASSWORD", font=("Segoe UI", 10, "bold"),
              bg="#0a0e27", fg="#7f8fa6").pack(anchor=W, pady=(15,5))
        self.txt_confirm_password = Entry(register_container, font=("Segoe UI", 12),
                                         bg="#1a1f3a", fg="#ffffff", 
                                         insertbackground="#00d4ff", bd=0,
                                         relief=FLAT, width=30, show="●")
        self.txt_confirm_password.pack(ipady=10, pady=5)
        Frame(register_container, bg="#00d4ff", height=2, width=300).pack()
        
        # Role Selection
        Label(register_container, text="ROLE", font=("Segoe UI", 10, "bold"),
              bg="#0a0e27", fg="#7f8fa6").pack(anchor=W, pady=(15,5))
        
        self.cmb_role = ttk.Combobox(register_container, font=("Segoe UI", 12),
                                     state='readonly', width=28)
        self.cmb_role['values'] = ('Admin', 'Manager', 'Employee')
        self.cmb_role.current(2)
        self.cmb_role.pack(ipady=8, pady=5)
        Frame(register_container, bg="#00d4ff", height=2, width=300).pack()
        
        # Bind Enter key to register
        self.txt_confirm_password.bind('<Return>', lambda e: self.register())
        
        # Register Button
        btn_register = Button(register_container, text="REGISTER", 
                             font=("Segoe UI", 12, "bold"),
                             bg="#00d4ff", fg="#0a0e27", cursor="hand2", bd=0,
                             activebackground="#00a8cc", activeforeground="#ffffff",
                             command=self.register, width=30, pady=12)
        btn_register.pack(pady=25)
        
        # Back to Login link
        login_frame = Frame(register_container, bg="#0a0e27")
        login_frame.pack(pady=5)
        
        Label(login_frame, text="Already have an account?", 
              font=("Segoe UI", 9), bg="#0a0e27", fg="#7f8fa6").pack(side=LEFT)
        
        btn_login_link = Button(login_frame, text="Login Here", 
                                font=("Segoe UI", 9, "bold"),
                                bg="#0a0e27", fg="#00d4ff", cursor="hand2", 
                                bd=0, activebackground="#0a0e27", 
                                activeforeground="#00a8cc",
                                command=self.back_to_login)
        btn_login_link.pack(side=LEFT, padx=5)
        
        # Focus on username
        self.txt_username.focus()
    
    def register(self):
        """Register new user"""
        if (self.txt_username.get() == "" or self.txt_password.get() == "" 
            or self.txt_confirm_password.get() == ""):
            messagebox.showerror("Error", "All fields are required", parent=self.root)
        elif self.txt_password.get() != self.txt_confirm_password.get():
            messagebox.showerror("Error", "Password and Confirm Password must match", 
                               parent=self.root)
        elif len(self.txt_password.get()) < 6:
            messagebox.showerror("Error", "Password must be at least 6 characters", 
                               parent=self.root)
        else:
            try:
                con = sqlite3.connect(database=r'ims.db')
                cur = con.cursor()
                
                cur.execute("SELECT * FROM users WHERE username=?", 
                          (self.txt_username.get(),))
                if cur.fetchone() is not None:
                    messagebox.showerror("Error", 
                                       "Username already exists. Please choose another.", 
                                       parent=self.root)
                else:
                    cur.execute("INSERT INTO users(username, password, role) VALUES(?,?,?)",
                              (self.txt_username.get(), 
                               self.txt_password.get(), 
                               self.cmb_role.get()))
                    con.commit()
                    messagebox.showinfo("Success", 
                                      "Registration successful! Please login now.",
                                      parent=self.root)
                    self.back_to_login()
                
                con.close()
            except Exception as ex:
                messagebox.showerror("Error", f"Error: {str(ex)}", parent=self.root)
    
    def back_to_login(self):
        """Return to login window"""
        self.root.destroy()
        login_root = Tk()
        LoginWindow(login_root)
        login_root.mainloop()


class IMS:
    def __init__(self, root, username="User", role="Admin"):
        self.root = root
        self.username = username
        self.role = role
        self.root.geometry("1400x750+100+50")
        self.root.title("Inventory Management System | Command Center")
        self.root.resizable(True, True)
        self.root.config(bg="#0a0e27")
        
        #------------- TOP NAVIGATION BAR --------------
        top_nav = Frame(self.root, bg="#1a1f3a", height=60)
        top_nav.pack(side=TOP, fill=X)
        
        # Logo and title in top left
        try:
            self.icon_title = PhotoImage(file="Inventory-Management-System/images/logo1.png")
            Label(top_nav, text="IMS", image=self.icon_title, compound=LEFT,
                  font=("Consolas", 20, "bold"), bg="#1a1f3a", fg="#00d4ff").pack(side=LEFT, padx=20)
        except:
            Label(top_nav, text="IMS",
                  font=("Consolas", 20, "bold"), bg="#1a1f3a", fg="#00d4ff").pack(side=LEFT, padx=20)
        
        # Top menu buttons - horizontal
        menu_frame = Frame(top_nav, bg="#1a1f3a")
        menu_frame.pack(side=LEFT, padx=100)
        
        menu_style = {
            "font": ("Segoe UI", 11, "bold"),
            "bg": "#1a1f3a",
            "fg": "#ffffff",
            "bd": 0,
            "cursor": "hand2",
            "activebackground": "#00d4ff",
            "activeforeground": "#0a0e27",
            "relief": FLAT,
            "padx": 25,
            "pady": 10
        }
        
        btn_home = Button(menu_frame, text="HOME", **menu_style)
        btn_home.pack(side=LEFT, padx=5)
        btn_home.config(bg="#00d4ff", fg="#0a0e27")
        
        btn_reports = Button(menu_frame, text="REPORTS", command=self.reports, **menu_style)
        btn_reports.pack(side=LEFT, padx=5)
        
        btn_settings = Button(menu_frame, text="SETTINGS", command=self.settings, **menu_style)
        btn_settings.pack(side=LEFT, padx=5)
        
        btn_help = Button(menu_frame, text="HELP", command=self.help, **menu_style)
        btn_help.pack(side=LEFT, padx=5)
        
        # User info and logout button top right
        user_frame = Frame(top_nav, bg="#1a1f3a")
        user_frame.pack(side=RIGHT, padx=20)
        
        Label(user_frame, text=f"👤 {self.username} ({self.role})", 
              font=("Segoe UI", 10), bg="#1a1f3a", fg="#ffffff").pack(side=LEFT, padx=10)
        
        logout_btn = Button(user_frame, text="LOGOUT ►", font=("Segoe UI", 11, "bold"),
                           bg="#ff4757", fg="white", cursor="hand2", bd=0,
                           activebackground="#ee2f3c", activeforeground="white",
                           command=self.logout, padx=20, pady=10)
        logout_btn.pack(side=LEFT)
        
        # Accent line
        accent = Frame(self.root, bg="#00d4ff", height=3)
        accent.pack(side=TOP, fill=X)
        
        #------------- WELCOME BANNER WITH CLOCK --------------
        banner = Frame(self.root, bg="#0f1535", height=120)
        banner.pack(side=TOP, fill=X, pady=20, padx=30)
        
        welcome_text = Label(banner, text=f"WELCOME TO COMMAND CENTER, {self.username.upper()}",
                            font=("Consolas", 28, "bold"), bg="#0f1535", fg="#00d4ff")
        welcome_text.pack(pady=10)
        
        self.lbl_clock = Label(banner, text="System Online • Loading...",
                              font=("Segoe UI", 12), bg="#0f1535", fg="#7f8fa6")
        self.lbl_clock.pack()
        
        #------------- CENTRAL ACTION HUB --------------
        action_hub = Frame(self.root, bg="#0a0e27")
        action_hub.pack(expand=True, fill=BOTH, padx=50, pady=10)
        
        # Title for action hub
        Label(action_hub, text="» MODULE LAUNCHER",
              font=("Consolas", 16, "bold"), bg="#0a0e27", fg="#ffffff").pack(pady=15)
        
        # Hexagonal grid container
        hex_container = Frame(action_hub, bg="#0a0e27")
        hex_container.pack()
        
        # Row 1 - 3 buttons
        row1 = Frame(hex_container, bg="#0a0e27")
        row1.pack(pady=5)
        
        self.create_action_button(row1, "EMPLOYEE\nMANAGEMENT", "#e84393", self.employee)
        self.create_action_button(row1, "SUPPLIER\nMANAGEMENT", "#00b894", self.supplier)
        self.create_action_button(row1, "CATEGORY\nMANAGEMENT", "#fdcb6e", self.category)
        
        # Row 2 - 3 buttons
        row2 = Frame(hex_container, bg="#0a0e27")
        row2.pack(pady=5)
        
        self.create_action_button(row2, "PRODUCT\nMANAGEMENT", "#6c5ce7", self.product)
        self.create_action_button(row2, "BILLING\nSYSTEM", "#00d4ff", self.billing)
        self.create_action_button(row2, "SALES\nRECORDS", "#fd79a8", self.sales)
        
        #------------- STATISTICS RIBBON --------------
        stats_ribbon = Frame(self.root, bg="#1a1f3a", height=80)
        stats_ribbon.pack(side=BOTTOM, fill=X, pady=0)
        
        # Accent line
        Frame(self.root, bg="#00d4ff", height=2).pack(side=BOTTOM, fill=X)
        
        # Stats container
        stats_container = Frame(stats_ribbon, bg="#1a1f3a")
        stats_container.pack(expand=True, fill=BOTH, pady=15)
        
        # Individual stat items - horizontal layout
        self.lbl_employee = Label(stats_container, text="EMPLOYEES: 0",
                                 font=("Consolas", 11, "bold"), bg="#1a1f3a", fg="#00d4ff")
        self.lbl_employee.pack(side=LEFT, padx=30)
        
        Label(stats_container, text="|", font=("Consolas", 14), 
              bg="#1a1f3a", fg="#2d3436").pack(side=LEFT)
        
        self.lbl_supplier = Label(stats_container, text="SUPPLIERS: 0",
                                 font=("Consolas", 11, "bold"), bg="#1a1f3a", fg="#00d4ff")
        self.lbl_supplier.pack(side=LEFT, padx=30)
        
        Label(stats_container, text="|", font=("Consolas", 14), 
              bg="#1a1f3a", fg="#2d3436").pack(side=LEFT)
        
        self.lbl_category = Label(stats_container, text="CATEGORIES: 0",
                                 font=("Consolas", 11, "bold"), bg="#1a1f3a", fg="#00d4ff")
        self.lbl_category.pack(side=LEFT, padx=30)
        
        Label(stats_container, text="|", font=("Consolas", 14), 
              bg="#1a1f3a", fg="#2d3436").pack(side=LEFT)
        
        self.lbl_product = Label(stats_container, text="PRODUCTS: 0",
                                font=("Consolas", 11, "bold"), bg="#1a1f3a", fg="#00d4ff")
        self.lbl_product.pack(side=LEFT, padx=30)
        
        Label(stats_container, text="|", font=("Consolas", 14), 
              bg="#1a1f3a", fg="#2d3436").pack(side=LEFT)
        
        self.lbl_sales = Label(stats_container, text="SALES: 0",
                              font=("Consolas", 11, "bold"), bg="#1a1f3a", fg="#00d4ff")
        self.lbl_sales.pack(side=LEFT, padx=30)
        
        Label(stats_container, text="|", font=("Consolas", 14), 
              bg="#1a1f3a", fg="#2d3436").pack(side=LEFT)
        
        self.lbl_status = Label(stats_container, text="STATUS: ACTIVE",
                               font=("Consolas", 11, "bold"), bg="#1a1f3a", fg="#00ff88")
        self.lbl_status.pack(side=LEFT, padx=30)
        
        #------------- FOOTER INFO --------------
        footer = Frame(self.root, bg="#0a0e27", height=50)
        footer.pack(side=BOTTOM, fill=X)
        
        Label(footer, text="IMS v2.0 • Developed by Keerthana Pathipati • Support: keerthanapathipati236@gmail.com",
              font=("Segoe UI", 9), bg="#0a0e27", fg="#535c68").pack(pady=15)
        
        self.update_content()
    
    def create_action_button(self, parent, text, color, command):
        """Create modern action button with hover effect"""
        btn_frame = Frame(parent, bg=color, width=180, height=100, bd=0)
        btn_frame.pack(side=LEFT, padx=15)
        btn_frame.pack_propagate(False)
        
        btn = Button(btn_frame, text=text, font=("Segoe UI", 12, "bold"),
                    bg=color, fg="white", cursor="hand2", bd=0,
                    activebackground=color, activeforeground="white",
                    command=command, relief=FLAT)
        btn.pack(expand=True, fill=BOTH)
        
        # Hover effects
        original_color = color
        hover_color = self.lighten_color(color)
        
        btn.bind("<Enter>", lambda e: btn.config(bg=hover_color))
        btn.bind("<Leave>", lambda e: btn.config(bg=original_color))
    
    def lighten_color(self, color):
        """Simple color lightening for hover"""
        color_map = {
            "#e84393": "#fd79a8",
            "#00b894": "#55efc4",
            "#fdcb6e": "#ffeaa7",
            "#6c5ce7": "#a29bfe",
            "#fd79a8": "#fab1a0",
            "#00d4ff": "#4ae0ff",
            "#2d3436": "#636e72"
        }
        return color_map.get(color, color)
    
    def logout(self):
        """Logout and return to login window"""
        response = messagebox.askyesno("Logout", 
                                      f"Are you sure you want to logout, {self.username}?",
                                      parent=self.root)
        if response:
            self.root.destroy()
            login_root = Tk()
            LoginWindow(login_root)
            login_root.mainloop()
    
    #-------------- MODULE FUNCTIONS ----------------
    def employee(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = employeeClass(self.new_win)
        
    def supplier(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = supplierClass(self.new_win)
        
    def category(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = categoryClass(self.new_win)
        
    def product(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = productClass(self.new_win)
    
    def billing(self):
        """Open Billing System"""
        self.new_win = Toplevel(self.root)
        self.new_obj = billClass(self.new_win)
        
    def sales(self):
        """Open Sales Records"""
        self.new_win = Toplevel(self.root)
        self.new_obj = salesClass(self.new_win)
    
    def reports(self):
        """Open Reports window"""
        reports_win = Toplevel(self.root)
        reports_win.geometry("1200x700+150+50")
        reports_win.title("Reports & Analytics Module")
        reports_win.config(bg="#0a0e27")
        reports_win.resizable(True, True)
        
        # Header
        header = Frame(reports_win, bg="#1a1f3a", height=80)
        header.pack(fill=X)
        
        Label(header, text="📊 REPORTS & ANALYTICS", 
              font=("Consolas", 24, "bold"), bg="#1a1f3a", fg="#00d4ff").pack(pady=25)
        
        Frame(reports_win, bg="#00d4ff", height=2).pack(fill=X)
        
        # Main content area
        content = Frame(reports_win, bg="#0a0e27")
        content.pack(fill=BOTH, expand=True, padx=30, pady=20)
        
        # Report categories
        Label(content, text="» AVAILABLE REPORTS", 
              font=("Consolas", 16, "bold"), bg="#0a0e27", fg="#ffffff").pack(pady=15, anchor=W)
        
        # Report buttons container
        reports_container = Frame(content, bg="#0a0e27")
        reports_container.pack(fill=BOTH, expand=True)
        
        # Row 1
        row1 = Frame(reports_container, bg="#0a0e27")
        row1.pack(fill=X, pady=10)
        
        self.create_report_card(row1, "📦 INVENTORY REPORT", 
                               "View current stock levels, low stock alerts, and product availability",
                               "#6c5ce7", lambda: self.generate_inventory_report(reports_win))
        
        self.create_report_card(row1, "💰 SALES REPORT", 
                               "Analyze sales trends, revenue, and top-selling products",
                               "#00b894", lambda: self.generate_sales_report(reports_win))
        
        # Row 2
        row2 = Frame(reports_container, bg="#0a0e27")
        row2.pack(fill=X, pady=10)
        
        self.create_report_card(row2, "👥 EMPLOYEE REPORT", 
                               "View employee details, roles, and performance metrics",
                               "#e84393", lambda: self.generate_employee_report(reports_win))
        
        self.create_report_card(row2, "🏭 SUPPLIER REPORT", 
                               "Track supplier information, contact details, and supply history",
                               "#fdcb6e", lambda: self.generate_supplier_report(reports_win))
        
        # Row 3
        row3 = Frame(reports_container, bg="#0a0e27")
        row3.pack(fill=X, pady=10)
        
        self.create_report_card(row3, "📁 CATEGORY REPORT", 
                               "Overview of product categories and distribution",
                               "#fd79a8", lambda: self.generate_category_report(reports_win))
        
        self.create_report_card(row3, "📈 ANALYTICS DASHBOARD", 
                               "Comprehensive analytics with charts and insights",
                               "#00d4ff", lambda: self.show_analytics_dashboard(reports_win))
        
        # Close button
        Button(reports_win, text="CLOSE", font=("Segoe UI", 12, "bold"),
               bg="#ff4757", fg="white", cursor="hand2", bd=0,
               command=reports_win.destroy, padx=30, pady=10).pack(pady=20)
    
    def create_report_card(self, parent, title, description, color, command):
        """Create a report card button"""
        card = Frame(parent, bg=color, bd=0)
        card.pack(side=LEFT, fill=BOTH, expand=True, padx=10)
        
        btn = Button(card, text=f"{title}\n\n{description}", 
                    font=("Segoe UI", 11, "bold"),
                    bg=color, fg="white", cursor="hand2", bd=0,
                    activebackground=color, activeforeground="white",
                    command=command, relief=FLAT, justify=LEFT,
                    wraplength=250, pady=20, padx=15)
        btn.pack(fill=BOTH, expand=True)
        
        # Hover effect
        hover_color = self.lighten_color(color)
        btn.bind("<Enter>", lambda e: btn.config(bg=hover_color))
        btn.bind("<Leave>", lambda e: btn.config(bg=color))
    
    def generate_inventory_report(self, parent):
        """Generate inventory report"""
        try:
            con = sqlite3.connect(database=r'ims.db')
            cur = con.cursor()
            cur.execute("SELECT * FROM product")
            products = cur.fetchall()
            con.close()
            
            if len(products) == 0:
                messagebox.showinfo("Info", "No products found in inventory", parent=parent)
                return
            
            report_win = Toplevel(parent)
            report_win.geometry("900x600+250+100")
            report_win.title("Inventory Report")
            report_win.config(bg="#0a0e27")
            
            Label(report_win, text="📦 INVENTORY REPORT", 
                  font=("Consolas", 20, "bold"), bg="#0a0e27", fg="#00d4ff").pack(pady=20)
            
            frame = Frame(report_win, bg="#0a0e27")
            frame.pack(fill=BOTH, expand=True, padx=20, pady=10)
            
            scrollbar = Scrollbar(frame, orient=VERTICAL)
            
            tree = ttk.Treeview(frame, columns=("name", "category", "qty", "price", "status"),
                               show="headings", yscrollcommand=scrollbar.set, height=20)
            scrollbar.config(command=tree.yview)
            scrollbar.pack(side=RIGHT, fill=Y)
            
            tree.heading("name", text="Product Name")
            tree.heading("category", text="Category")
            tree.heading("qty", text="Quantity")
            tree.heading("price", text="Price")
            tree.heading("status", text="Status")
            
            tree.column("name", width=200)
            tree.column("category", width=150)
            tree.column("qty", width=100)
            tree.column("price", width=100)
            tree.column("status", width=150)
            
            for product in products:
                qty = int(product[5]) if product[5] else 0
                status = "🔴 Low Stock" if qty < 10 else "🟢 In Stock"
                tree.insert("", END, values=(product[3], product[1], qty, f"₹{product[4]}", status))
            
            tree.pack(fill=BOTH, expand=True)
            
            Label(report_win, text=f"Total Products: {len(products)}", 
                  font=("Segoe UI", 11, "bold"), bg="#0a0e27", fg="#00d4ff").pack(pady=10)
            
        except Exception as ex:
            messagebox.showerror("Error", f"Error generating report: {str(ex)}", parent=parent)
    
    def generate_sales_report(self, parent):
        """Generate sales report"""
        try:
            bill_count = len(os.listdir("Inventory-Management-System/bill"))
            
            report_win = Toplevel(parent)
            report_win.geometry("700x500+300+150")
            report_win.title("Sales Report")
            report_win.config(bg="#0a0e27")
            
            Label(report_win, text="💰 SALES REPORT", 
                  font=("Consolas", 20, "bold"), bg="#0a0e27", fg="#00d4ff").pack(pady=30)
            
            info_frame = Frame(report_win, bg="#1a1f3a", bd=2, relief=RIDGE)
            info_frame.pack(padx=50, pady=20, fill=X)
            
            Label(info_frame, text=f"Total Bills Generated: {bill_count}", 
                  font=("Segoe UI", 14, "bold"), bg="#1a1f3a", fg="#ffffff").pack(pady=15)
            
            Label(info_frame, text="📂 Bills Location: Inventory-Management-System/bill/", 
                  font=("Segoe UI", 11), bg="#1a1f3a", fg="#7f8fa6").pack(pady=10)
            
            Label(report_win, text="Sales tracking and analytics available", 
                  font=("Segoe UI", 12), bg="#0a0e27", fg="#ffffff").pack(pady=20)
            
        except Exception as ex:
            messagebox.showerror("Error", f"Error generating report: {str(ex)}", parent=parent)
    
    def generate_employee_report(self, parent):
        """Generate employee report"""
        try:
            con = sqlite3.connect(database=r'ims.db')
            cur = con.cursor()
            cur.execute("SELECT * FROM employee")
            employees = cur.fetchall()
            con.close()
            
            if len(employees) == 0:
                messagebox.showinfo("Info", "No employees found", parent=parent)
                return
            
            report_win = Toplevel(parent)
            report_win.geometry("900x600+250+100")
            report_win.title("Employee Report")
            report_win.config(bg="#0a0e27")
            
            Label(report_win, text="👥 EMPLOYEE REPORT", 
                  font=("Consolas", 20, "bold"), bg="#0a0e27", fg="#00d4ff").pack(pady=20)
            
            frame = Frame(report_win, bg="#0a0e27")
            frame.pack(fill=BOTH, expand=True, padx=20, pady=10)
            
            scrollbar = Scrollbar(frame, orient=VERTICAL)
            
            tree = ttk.Treeview(frame, columns=("name", "email", "contact", "designation"),
                               show="headings", yscrollcommand=scrollbar.set, height=20)
            scrollbar.config(command=tree.yview)
            scrollbar.pack(side=RIGHT, fill=Y)
            
            tree.heading("name", text="Name")
            tree.heading("email", text="Email")
            tree.heading("contact", text="Contact")
            tree.heading("designation", text="Designation")
            
            tree.column("name", width=180)
            tree.column("email", width=220)
            tree.column("contact", width=150)
            tree.column("designation", width=150)
            
            for emp in employees:
                tree.insert("", END, values=(emp[1], emp[2], emp[4], emp[8]))
            
            tree.pack(fill=BOTH, expand=True)
            
            Label(report_win, text=f"Total Employees: {len(employees)}", 
                  font=("Segoe UI", 11, "bold"), bg="#0a0e27", fg="#00d4ff").pack(pady=10)
            
        except Exception as ex:
            messagebox.showerror("Error", f"Error generating report: {str(ex)}", parent=parent)
    
    def generate_supplier_report(self, parent):
        """Generate supplier report"""
        try:
            con = sqlite3.connect(database=r'ims.db')
            cur = con.cursor()
            cur.execute("SELECT * FROM supplier")
            suppliers = cur.fetchall()
            con.close()
            
            if len(suppliers) == 0:
                messagebox.showinfo("Info", "No suppliers found", parent=parent)
                return
            
            report_win = Toplevel(parent)
            report_win.geometry("900x600+250+100")
            report_win.title("Supplier Report")
            report_win.config(bg="#0a0e27")
            
            Label(report_win, text="🏭 SUPPLIER REPORT", 
                  font=("Consolas", 20, "bold"), bg="#0a0e27", fg="#00d4ff").pack(pady=20)
            
            frame = Frame(report_win, bg="#0a0e27")
            frame.pack(fill=BOTH, expand=True, padx=20, pady=10)
            
            scrollbar = Scrollbar(frame, orient=VERTICAL)
            
            tree = ttk.Treeview(frame, columns=("invoice", "name", "contact", "desc"),
                               show="headings", yscrollcommand=scrollbar.set, height=20)
            scrollbar.config(command=tree.yview)
            scrollbar.pack(side=RIGHT, fill=Y)
            
            tree.heading("invoice", text="Invoice")
            tree.heading("name", text="Name")
            tree.heading("contact", text="Contact")
            tree.heading("desc", text="Description")
            
            tree.column("invoice", width=100)
            tree.column("name", width=180)
            tree.column("contact", width=150)
            tree.column("desc", width=300)
            
            for sup in suppliers:
                try:
                    invoice = sup[0] if len(sup) > 0 else "N/A"
                    name = sup[1] if len(sup) > 1 else "N/A"
                    contact = sup[2] if len(sup) > 2 else "N/A"
                    desc = sup[3] if len(sup) > 3 else "N/A"
                    tree.insert("", END, values=(invoice, name, contact, desc))
                except:
                    continue
            
            tree.pack(fill=BOTH, expand=True)
            
            Label(report_win, text=f"Total Suppliers: {len(suppliers)}", 
                  font=("Segoe UI", 11, "bold"), bg="#0a0e27", fg="#00d4ff").pack(pady=10)
            
        except Exception as ex:
            messagebox.showerror("Error", f"Error generating report: {str(ex)}", parent=parent)
    
    def generate_category_report(self, parent):
        """Generate category report"""
        try:
            con = sqlite3.connect(database=r'ims.db')
            cur = con.cursor()
            cur.execute("SELECT * FROM category")
            categories = cur.fetchall()
            con.close()
            
            if len(categories) == 0:
                messagebox.showinfo("Info", "No categories found", parent=parent)
                return
            
            report_win = Toplevel(parent)
            report_win.geometry("700x600+300+100")
            report_win.title("Category Report")
            report_win.config(bg="#0a0e27")
            
            Label(report_win, text="📁 CATEGORY REPORT", 
                  font=("Consolas", 20, "bold"), bg="#0a0e27", fg="#00d4ff").pack(pady=20)
            
            frame = Frame(report_win, bg="#0a0e27")
            frame.pack(fill=BOTH, expand=True, padx=20, pady=10)
            
            scrollbar = Scrollbar(frame, orient=VERTICAL)
            
            tree = ttk.Treeview(frame, columns=("id", "name"),
                               show="headings", yscrollcommand=scrollbar.set, height=20)
            scrollbar.config(command=tree.yview)
            scrollbar.pack(side=RIGHT, fill=Y)
            
            tree.heading("id", text="Category ID")
            tree.heading("name", text="Category Name")
            
            tree.column("id", width=150)
            tree.column("name", width=300)
            
            for cat in categories:
                tree.insert("", END, values=(cat[0], cat[1]))
            
            tree.pack(fill=BOTH, expand=True)
            
            Label(report_win, text=f"Total Categories: {len(categories)}", 
                  font=("Segoe UI", 11, "bold"), bg="#0a0e27", fg="#00d4ff").pack(pady=10)
            
        except Exception as ex:
            messagebox.showerror("Error", f"Error generating report: {str(ex)}", parent=parent)
    
    def show_analytics_dashboard(self, parent):
        """Show analytics dashboard with summary"""
        try:
            con = sqlite3.connect(database=r'ims.db')
            cur = con.cursor()
            
            cur.execute("SELECT COUNT(*) FROM product")
            product_count = cur.fetchone()[0]
            
            cur.execute("SELECT COUNT(*) FROM category")
            category_count = cur.fetchone()[0]
            
            cur.execute("SELECT COUNT(*) FROM employee")
            employee_count = cur.fetchone()[0]
            
            cur.execute("SELECT COUNT(*) FROM supplier")
            supplier_count = cur.fetchone()[0]
            
            cur.execute("SELECT COUNT(*) FROM product WHERE CAST(qty AS INTEGER) < 10")
            low_stock = cur.fetchone()[0]
            
            con.close()
            
            bill_count = len(os.listdir("Inventory-Management-System/bill"))
            
            dashboard_win = Toplevel(parent)
            dashboard_win.geometry("800x650+300+80")
            dashboard_win.title("Analytics Dashboard")
            dashboard_win.config(bg="#0a0e27")
            
            Label(dashboard_win, text="📈 ANALYTICS DASHBOARD", 
                  font=("Consolas", 20, "bold"), bg="#0a0e27", fg="#00d4ff").pack(pady=20)
            
            stats_frame = Frame(dashboard_win, bg="#0a0e27")
            stats_frame.pack(padx=40, pady=20)
            
            row1 = Frame(stats_frame, bg="#0a0e27")
            row1.pack(pady=10)
            
            self.create_stat_box(row1, "📦 PRODUCTS", product_count, "#6c5ce7")
            self.create_stat_box(row1, "📁 CATEGORIES", category_count, "#fdcb6e")
            
            row2 = Frame(stats_frame, bg="#0a0e27")
            row2.pack(pady=10)
            
            self.create_stat_box(row2, "👥 EMPLOYEES", employee_count, "#e84393")
            self.create_stat_box(row2, "🏭 SUPPLIERS", supplier_count, "#00b894")
            
            row3 = Frame(stats_frame, bg="#0a0e27")
            row3.pack(pady=10)
            
            self.create_stat_box(row3, "💰 SALES", bill_count, "#00d4ff")
            self.create_stat_box(row3, "⚠️ LOW STOCK", low_stock, "#ff4757")
            
            summary_frame = Frame(dashboard_win, bg="#1a1f3a", bd=2, relief=RIDGE)
            summary_frame.pack(padx=40, pady=20, fill=X)
            
            Label(summary_frame, text="SYSTEM OVERVIEW", 
                  font=("Consolas", 14, "bold"), bg="#1a1f3a", fg="#00d4ff").pack(pady=10)
            
            summary_text = f"""
Total Records: {product_count + category_count + employee_count + supplier_count}
Active Products: {product_count}
Low Stock Alerts: {low_stock}
Total Bills: {bill_count}
            """
            
            Label(summary_frame, text=summary_text, 
                  font=("Segoe UI", 11), bg="#1a1f3a", fg="#ffffff").pack(pady=10)
            
        except Exception as ex:
            messagebox.showerror("Error", f"Error loading analytics: {str(ex)}", parent=parent)
    
    def create_stat_box(self, parent, title, value, color):
        """Create a statistics box"""
        box = Frame(parent, bg=color, width=200, height=120, bd=0)
        box.pack(side=LEFT, padx=15)
        box.pack_propagate(False)
        
        Label(box, text=title, font=("Segoe UI", 10, "bold"),
              bg=color, fg="white").pack(pady=15)
        Label(box, text=str(value), font=("Consolas", 28, "bold"),
              bg=color, fg="white").pack()
    
    def settings(self):
        """Open Settings window"""
        settings_win = Toplevel(self.root)
        settings_win.geometry("1000x700+250+50")
        settings_win.title("Settings Module")
        settings_win.config(bg="#0a0e27")
        settings_win.resizable(True, True)
        
        header = Frame(settings_win, bg="#1a1f3a", height=80)
        header.pack(fill=X)
        
        Label(header, text="⚙️ SYSTEM SETTINGS", 
              font=("Consolas", 24, "bold"), bg="#1a1f3a", fg="#00d4ff").pack(pady=25)
        
        Frame(settings_win, bg="#00d4ff", height=2).pack(fill=X)
        
        content = Frame(settings_win, bg="#0a0e27")
        content.pack(fill=BOTH, expand=True, padx=30, pady=20)
        
        Label(content, text="» CONFIGURATION OPTIONS", 
              font=("Consolas", 16, "bold"), bg="#0a0e27", fg="#ffffff").pack(pady=15, anchor=W)
        
        settings_container = Frame(content, bg="#0a0e27")
        settings_container.pack(fill=BOTH, expand=True, pady=10)
        
        db_section = Frame(settings_container, bg="#1a1f3a", bd=2, relief=RIDGE)
        db_section.pack(fill=X, pady=10)
        
        Label(db_section, text="🗄️ DATABASE SETTINGS", 
              font=("Segoe UI", 14, "bold"), bg="#1a1f3a", fg="#00d4ff").pack(anchor=W, padx=20, pady=15)
        
        db_info = Frame(db_section, bg="#1a1f3a")
        db_info.pack(fill=X, padx=40, pady=10)
        
        Label(db_info, text="Database File: ims.db", 
              font=("Segoe UI", 11), bg="#1a1f3a", fg="#ffffff").pack(anchor=W, pady=5)
        Label(db_info, text="Status: Connected ✓", 
              font=("Segoe UI", 11), bg="#1a1f3a", fg="#00ff88").pack(anchor=W, pady=5)
        
        db_buttons = Frame(db_section, bg="#1a1f3a")
        db_buttons.pack(pady=15, padx=40, anchor=W)
        
        Button(db_buttons, text="BACKUP DATABASE", font=("Segoe UI", 10, "bold"),
               bg="#00b894", fg="white", cursor="hand2", bd=0,
               command=lambda: self.backup_database(settings_win),
               padx=20, pady=8).pack(side=LEFT, padx=5)
        
        Button(db_buttons, text="VIEW TABLES", font=("Segoe UI", 10, "bold"),
               bg="#6c5ce7", fg="white", cursor="hand2", bd=0,
               command=lambda: self.view_database_tables(settings_win),
               padx=20, pady=8).pack(side=LEFT, padx=5)
        
        user_section = Frame(settings_container, bg="#1a1f3a", bd=2, relief=RIDGE)
        user_section.pack(fill=X, pady=10)
        
        Label(user_section, text="👤 USER MANAGEMENT", 
              font=("Segoe UI", 14, "bold"), bg="#1a1f3a", fg="#00d4ff").pack(anchor=W, padx=20, pady=15)
        
        user_info = Frame(user_section, bg="#1a1f3a")
        user_info.pack(fill=X, padx=40, pady=10)
        
        Label(user_info, text=f"Current User: {self.username}", 
              font=("Segoe UI", 11), bg="#1a1f3a", fg="#ffffff").pack(anchor=W, pady=5)
        Label(user_info, text=f"Role: {self.role}", 
              font=("Segoe UI", 11), bg="#1a1f3a", fg="#ffffff").pack(anchor=W, pady=5)
        
        user_buttons = Frame(user_section, bg="#1a1f3a")
        user_buttons.pack(pady=15, padx=40, anchor=W)
        
        Button(user_buttons, text="CHANGE PASSWORD", font=("Segoe UI", 10, "bold"),
               bg="#e84393", fg="white", cursor="hand2", bd=0,
               command=lambda: self.change_password(settings_win),
               padx=20, pady=8).pack(side=LEFT, padx=5)
        
        Button(user_buttons, text="VIEW ALL USERS", font=("Segoe UI", 10, "bold"),
               bg="#fdcb6e", fg="white", cursor="hand2", bd=0,
               command=lambda: self.view_all_users(settings_win),
               padx=20, pady=8).pack(side=LEFT, padx=5)
        
        system_section = Frame(settings_container, bg="#1a1f3a", bd=2, relief=RIDGE)
        system_section.pack(fill=X, pady=10)
        
        Label(system_section, text="🖥️ SYSTEM PREFERENCES", 
              font=("Segoe UI", 14, "bold"), bg="#1a1f3a", fg="#00d4ff").pack(anchor=W, padx=20, pady=15)
        
        system_info = Frame(system_section, bg="#1a1f3a")
        system_info.pack(fill=X, padx=40, pady=10)
        
        Label(system_info, text="Application Version: IMS v2.0", 
              font=("Segoe UI", 11), bg="#1a1f3a", fg="#ffffff").pack(anchor=W, pady=5)
        Label(system_info, text="Bill Directory: Inventory-Management-System/bill/", 
              font=("Segoe UI", 11), bg="#1a1f3a", fg="#ffffff").pack(anchor=W, pady=5)
        Label(system_info, text="Auto-refresh: Enabled (200ms)", 
              font=("Segoe UI", 11), bg="#1a1f3a", fg="#ffffff").pack(anchor=W, pady=5)
        
        system_buttons = Frame(system_section, bg="#1a1f3a")
        system_buttons.pack(pady=15, padx=40, anchor=W)
        
        Button(system_buttons, text="CLEAR CACHE", font=("Segoe UI", 10, "bold"),
               bg="#fd79a8", fg="white", cursor="hand2", bd=0,
               command=lambda: messagebox.showinfo("Info", "Cache cleared successfully!", parent=settings_win),
               padx=20, pady=8).pack(side=LEFT, padx=5)
        
        Button(settings_win, text="CLOSE", font=("Segoe UI", 12, "bold"),
               bg="#ff4757", fg="white", cursor="hand2", bd=0,
               command=settings_win.destroy, padx=30, pady=10).pack(pady=20)
    
    def backup_database(self, parent):
        """Backup database"""
        try:
            import shutil
            from datetime import datetime
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_name = f"ims_backup_{timestamp}.db"
            
            shutil.copy2("ims.db", backup_name)
            messagebox.showinfo("Success", 
                              f"Database backed up successfully!\nBackup file: {backup_name}",
                              parent=parent)
        except Exception as ex:
            messagebox.showerror("Error", f"Backup failed: {str(ex)}", parent=parent)
    
    def view_database_tables(self, parent):
        """View database tables info"""
        try:
            con = sqlite3.connect(database=r'ims.db')
            cur = con.cursor()
            
            cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = cur.fetchall()
            
            con.close()
            
            table_win = Toplevel(parent)
            table_win.geometry("600x500+350+150")
            table_win.title("Database Tables")
            table_win.config(bg="#0a0e27")
            
            Label(table_win, text="📊 DATABASE TABLES", 
                  font=("Consolas", 18, "bold"), bg="#0a0e27", fg="#00d4ff").pack(pady=20)
            
            info_frame = Frame(table_win, bg="#1a1f3a", bd=2, relief=RIDGE)
            info_frame.pack(padx=30, pady=10, fill=BOTH, expand=True)
            
            Label(info_frame, text="Available Tables:", 
                  font=("Segoe UI", 12, "bold"), bg="#1a1f3a", fg="#ffffff").pack(anchor=W, padx=20, pady=10)
            
            for table in tables:
                Label(info_frame, text=f"• {table[0]}", 
                      font=("Segoe UI", 11), bg="#1a1f3a", fg="#00d4ff").pack(anchor=W, padx=40, pady=5)
            
            Label(table_win, text=f"Total Tables: {len(tables)}", 
                  font=("Segoe UI", 11, "bold"), bg="#0a0e27", fg="#00ff88").pack(pady=15)
            
        except Exception as ex:
            messagebox.showerror("Error", f"Error: {str(ex)}", parent=parent)
    
    def change_password(self, parent):
        """Change user password"""
        password_win = Toplevel(parent)
        password_win.geometry("500x450+400+200")
        password_win.title("Change Password")
        password_win.config(bg="#0a0e27")
        password_win.resizable(False, False)
        
        Label(password_win, text="🔒 CHANGE PASSWORD", 
              font=("Consolas", 18, "bold"), bg="#0a0e27", fg="#00d4ff").pack(pady=30)
        
        Label(password_win, text="Current Password:", 
              font=("Segoe UI", 11, "bold"), bg="#0a0e27", fg="#7f8fa6").pack(anchor=W, padx=50, pady=(10,5))
        current_pass = Entry(password_win, font=("Segoe UI", 12), show="●", width=30)
        current_pass.pack(padx=50, pady=5)
        
        Label(password_win, text="New Password:", 
              font=("Segoe UI", 11, "bold"), bg="#0a0e27", fg="#7f8fa6").pack(anchor=W, padx=50, pady=(15,5))
        new_pass = Entry(password_win, font=("Segoe UI", 12), show="●", width=30)
        new_pass.pack(padx=50, pady=5)
        
        Label(password_win, text="Confirm New Password:", 
              font=("Segoe UI", 11, "bold"), bg="#0a0e27", fg="#7f8fa6").pack(anchor=W, padx=50, pady=(15,5))
        confirm_pass = Entry(password_win, font=("Segoe UI", 12), show="●", width=30)
        confirm_pass.pack(padx=50, pady=5)
        
        def update_password():
            if current_pass.get() == "" or new_pass.get() == "" or confirm_pass.get() == "":
                messagebox.showerror("Error", "All fields are required", parent=password_win)
                return
            
            if new_pass.get() != confirm_pass.get():
                messagebox.showerror("Error", "New passwords do not match", parent=password_win)
                return
            
            try:
                con = sqlite3.connect(database=r'ims.db')
                cur = con.cursor()
                
                cur.execute("SELECT * FROM users WHERE username=? AND password=?",
                          (self.username, current_pass.get()))
                
                if cur.fetchone() is None:
                    messagebox.showerror("Error", "Current password is incorrect", parent=password_win)
                else:
                    cur.execute("UPDATE users SET password=? WHERE username=?",
                              (new_pass.get(), self.username))
                    con.commit()
                    messagebox.showinfo("Success", "Password changed successfully!", parent=password_win)
                    password_win.destroy()
                
                con.close()
            except Exception as ex:
                messagebox.showerror("Error", f"Error: {str(ex)}", parent=password_win)
        
        Button(password_win, text="UPDATE PASSWORD", font=("Segoe UI", 11, "bold"),
               bg="#00d4ff", fg="#0a0e27", cursor="hand2", bd=0,
               command=update_password, padx=30, pady=10).pack(pady=30)
    
    def view_all_users(self, parent):
        """View all registered users"""
        try:
            con = sqlite3.connect(database=r'ims.db')
            cur = con.cursor()
            cur.execute("SELECT uid, username, role FROM users")
            users = cur.fetchall()
            con.close()
            
            users_win = Toplevel(parent)
            users_win.geometry("700x500+350+150")
            users_win.title("All Users")
            users_win.config(bg="#0a0e27")
            
            Label(users_win, text="👥 REGISTERED USERS", 
                  font=("Consolas", 18, "bold"), bg="#0a0e27", fg="#00d4ff").pack(pady=20)
            
            frame = Frame(users_win, bg="#0a0e27")
            frame.pack(fill=BOTH, expand=True, padx=20, pady=10)
            
            scrollbar = Scrollbar(frame, orient=VERTICAL)
            
            tree = ttk.Treeview(frame, columns=("id", "username", "role"),
                               show="headings", yscrollcommand=scrollbar.set, height=15)
            scrollbar.config(command=tree.yview)
            scrollbar.pack(side=RIGHT, fill=Y)
            
            tree.heading("id", text="User ID")
            tree.heading("username", text="Username")
            tree.heading("role", text="Role")
            
            tree.column("id", width=100)
            tree.column("username", width=250)
            tree.column("role", width=200)
            
            for user in users:
                tree.insert("", END, values=user)
            
            tree.pack(fill=BOTH, expand=True)
            
            Label(users_win, text=f"Total Users: {len(users)}", 
                  font=("Segoe UI", 11, "bold"), bg="#0a0e27", fg="#00d4ff").pack(pady=10)
            
        except Exception as ex:
            messagebox.showerror("Error", f"Error: {str(ex)}", parent=parent)
    
    def help(self):
        """Open Help window"""
        help_win = Toplevel(self.root)
        help_win.geometry("800x600+300+100")
        help_win.title("Help & Support")
        help_win.config(bg="#0a0e27")
        
        Label(help_win, text="❓ HELP & SUPPORT", 
              font=("Consolas", 24, "bold"), bg="#0a0e27", fg="#00d4ff").pack(pady=30)
        
        help_text = """
        Welcome to Inventory Management System Help
        
        📧 Email Support: keerthanapathipati236@gmail.com
        💬 Technical Assistance Available
        
        Quick Guide:
        • Use EMPLOYEE to manage staff records
        • Use SUPPLIER to manage vendor information
        • Use CATEGORY to organize product types
        • Use PRODUCT to manage inventory items
        • Use BILLING SYSTEM to process sales and generate bills
        • Use SALES RECORDS to view transaction history
        
        For technical assistance, contact support team.
        """
        
        Label(help_win, text=help_text, 
              font=("Segoe UI", 12), bg="#0a0e27", fg="#ffffff",
              justify=LEFT).pack(pady=20, padx=50)
        
        Button(help_win, text="CLOSE", font=("Segoe UI", 12, "bold"),
               bg="#ff4757", fg="white", cursor="hand2", bd=0,
               command=help_win.destroy, padx=30, pady=10).pack(pady=30)

    def update_content(self):
        """Update dashboard content with live data"""
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            # Update product count
            cur.execute("select * from product")
            product = cur.fetchall()
            self.lbl_product.config(text=f"PRODUCTS: {len(product)}")

            # Update category count
            cur.execute("select * from category")
            category = cur.fetchall()
            self.lbl_category.config(text=f"CATEGORIES: {len(category)}")

            # Update employee count
            cur.execute("select * from employee")
            employee = cur.fetchall()
            self.lbl_employee.config(text=f"EMPLOYEES: {len(employee)}")

            # Update supplier count
            cur.execute("select * from supplier")
            supplier = cur.fetchall()
            self.lbl_supplier.config(text=f"SUPPLIERS: {len(supplier)}")
            
            # Update sales count
            bill = len(os.listdir("Inventory-Management-System/bill"))
            self.lbl_sales.config(text=f"SALES: {bill}")
            
            # System status
            self.lbl_status.config(text="STATUS: ● ACTIVE")

            # Update clock
            time_ = time.strftime("%I:%M:%S %p")
            date_ = time.strftime("%d-%m-%Y")
            day_ = time.strftime("%A")
            self.lbl_clock.config(
                text=f"System Online • {day_}, {date_} • {time_}"
            )
            
            # Refresh every 200ms
            self.lbl_clock.after(200, self.update_content)
            
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", 
                               parent=self.root)
        finally:
            con.close()

if __name__ == "__main__":
    root = Tk()
    obj = LoginWindow(root)
    root.mainloop()