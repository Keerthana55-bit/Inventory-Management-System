# 🏢 Inventory Management System - Command Center

A comprehensive, enterprise-grade desktop application designed to streamline business operations for small to medium-sized enterprises. Built with Python and Tkinter, featuring a modern dark-themed interface that reduces eye strain during extended use.

![Dashboard](images/dashboard.png.png)

## ✨ Features

### 🔐 Authentication System
- User Login & Registration with role-based access (Admin, Manager, Employee)
- Password Management with change password functionality
- Secure Authentication with username/password validation
- **Default Admin Account**: Username: `admin`, Password: `admin123`

### 📦 Core Modules

#### 1. Employee Management
![Employee Module](images/employee.png.png)

- Add, update, delete, and search employees
- Store comprehensive employee details (ID, name, email, gender, contact, DOB, DOJ, salary, address)
- User type assignment (Admin/Employee)
- Real-time data validation

#### 2. Supplier Management
![Supplier Module](images/supplier.png.png)

- Manage supplier information with invoice tracking
- Store supplier details (invoice number, name, contact, description)
- Search functionality by invoice number
- Complete CRUD operations

#### 3. Category Management
![Category Module](images/category.png.png)

- Organize products into categories
- Simple add and delete operations
- Real-time category updates
- Used for product classification

#### 4. Product Management
![Product Module](images/product.png.png)

- Complete product inventory control
- Link products with categories and suppliers
- Track product price, quantity, and status (Active/Inactive)
- Advanced search functionality
- Stock status monitoring

#### 5. 💳 Billing System
![Billing Module](images/billing.png.png)

- Interactive Point of Sale (POS) interface
- Product catalog with search functionality
- Shopping cart management
- Built-in calculator for quick calculations
- Customer details capture
- Automatic discount calculation (5%)
- Professional invoice generation
- Print receipt functionality
- Real-time inventory updates after sales

#### 6. Sales Records
![Sales Module](images/sales.png.png)

- View all generated bills/invoices
- Search invoices by number
- Bill preview functionality
- Sales statistics and tracking

### 📊 Reports & Analytics

- **Inventory Report** - Stock levels and low stock alerts
- **Sales Report** - Total bills and revenue tracking
- **Employee Report** - Staff details and roles
- **Supplier Report** - Vendor information
- **Category Report** - Product distribution
- **Analytics Dashboard** - Comprehensive system overview with statistics

### ⚙️ Settings & Configuration

- **Database Management** - Backup and restore functionality
- **User Management** - View all users and their roles
- **Password Management** - Secure password change
- **System Information** - Application version and configuration details

## 🚀 Getting Started

### Prerequisites

Ensure you have Python 3.x installed on your PC along with the following packages:
```bash
pip install pillow
pip install sqlite3
```

**Note**: `time` and `os` are built-in Python modules and don't require installation.

### Installation

1. Clone the repository:
```bash
git clone https://github.com/Keerthana55-bit/inventory-management-system.git
cd inventory-management-system
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

3. Initialize the database:
```bash
python create_db.py
```

4. Run the application:
```bash
python dashboard.py
```

## 📖 User Guide

### First Time Setup

1. **Login with default credentials:**
   - Username: `admin`
   - Password: `admin123`

2. **Create additional users:**
   - Click "Register Here" on login screen
   - Fill in username, password, and select role
   - Login with new credentials

3. **Set up your inventory:**
   - Add categories (e.g., Electronics, Clothing, Food)
   - Add suppliers with contact information
   - Add employees with their details
   - Add products linking them to categories and suppliers

## 📁 Project Structure
```
inventory-management-system/
│
├── dashboard.py          # Main dashboard and navigation
├── employee.py           # Employee management module
├── supplier.py           # Supplier management module
├── product.py            # Product management module
├── category.py           # Category management module
├── sales.py              # Sales records module
├── billing.py            # Billing/POS system
├── create_db.py          # Database initialization
└── ims.db               # SQLite database (created automatically)
```

## 🛠️ Technologies Used

- **Python 3.x** - Core programming language
- **Tkinter** - GUI framework
- **SQLite3** - Database management
- **PIL (Pillow)** - Image processing

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👤 Author

Your Name - Keerthana Pathipati
Project Link: [https://github.com/yourusername/inventory-management-system](https://github.com/Keerthana55-bit/Inventory-Management-System)


⭐ Star this repository if you find it helpful!
```

**Note**: Remember to:
1. Replace `yourusername` with your actual GitHub username
2. Replace `Your Name` and social links in the Author section
3. Add a `requirements.txt` file with:
```
   pillow
