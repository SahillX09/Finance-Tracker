# 💰 MoneyMap – Personal Finance Tracker

> A modern, intuitive web application for tracking personal finances, managing budgets, and gaining meaningful financial insights.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Django](https://img.shields.io/badge/Django-5.0+-green.svg)

---

## 📌 Overview

MoneyMap is a full-stack personal finance management web application built using **Django**. It allows users to track income and expenses, define monthly budgets, analyze spending patterns, and export financial data for further analysis.

The application focuses on **clarity, simplicity, and real-world usability**, making it suitable for students, professionals, and anyone looking to gain control over their finances.

### Why MoneyMap?

- Simple and intuitive UI
- Detailed financial insights
- Budget tracking with alerts
- Secure authentication
- Multi-currency support
- Data export for external analysis

---

## ✨ Features

### 🔐 User Authentication
- Secure user registration and login
- Django’s built-in authentication system
- Encrypted password storage
- Individual user data isolation

### 💳 Transaction Management
- Add, edit, and delete transactions
- Categorize income and expenses
- Optional descriptions for clarity
- Date-based tracking
- Supports bulk data handling

### 📊 Dashboard & Insights
- Real-time balance calculation
- Monthly income vs expense summary
- Category-wise expense breakdown
- Interactive charts and graphs
- Recent transaction history

### 🎯 Budget Goals
- Set monthly limits per category
- Visual budget utilization tracking
- Over-budget alerts
- Spending vs limit comparison

### 🔍 Filtering & Search
- Filter by month, year, category, and type
- Search by title or description
- Paginated transaction lists
- Persistent filter states

### 📈 Analytics
- 6-month income vs expense trends
- Category-wise expense visualization
- Top spending categories
- Monthly comparison insights

### 💱 Multi-Currency Support
- INR (default)
- USD, EUR, GBP, JPY
- User-selectable preferred currency

### 📥 Data Export
- Export transactions as CSV
- Filtered export support
- Excel and Google Sheets compatible

### ⚙️ Profile Settings
- Update monthly income
- Change preferred currency
- Manage personal details

---

## 🛠️ Tech Stack

### Backend
- **Python** 3.8+
- **Django** 5.0+
- **Django ORM**
- SQLite (development)
- PostgreSQL (production-ready)

### Frontend
- HTML5
- CSS3 (custom design system)
- Vanilla JavaScript
- Chart.js (data visualization)

### Design Approach
- Minimal and modern UI
- Mobile-responsive layout
- Fintech-inspired color palette
- System font stack for performance

---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8+
- pip
- Git (optional)

### Step 1: Clone or Download

```bash
git clone <repository-url>
cd moneymap
Or extract the ZIP and navigate to the project folder.

Step 2: Create Virtual Environment
Windows:
python -m venv venv
venv\Scripts\activate

macOS / Linux:
python3 -m venv venv
source venv/bin/activate

Step 3: Install Dependencies
pip install django
pip install -r requirements.txt

Step 4: Database Setup
python manage.py makemigrations
python manage.py migrate

Step 5: Setup Default Currencies
python manage.py setup_currencies

Step 6: Create Admin User (Optional)
python manage.py createsuperuser

Admin panel:
/admin/

Step 7: Run Server
python manage.py runserver
Open:
http://127.0.0.1:8000/

📖 Usage Guide

1️⃣ Register & Login
Create an account
Default income and expense categories are auto-generated

2️⃣ Set Monthly Income
Required for accurate budgeting
Choose preferred currency

3️⃣ Add Transactions
Specify title, amount, category, date, and type
Optional description supported

4️⃣ Dashboard Overview
Monthly summary
Balance calculation
Category breakdown
Recent transactions

5️⃣ Budget Goal
Define monthly spending limits
Track progress visually
Over-budget indicators

6️⃣ Analytics
Income vs expense trends
Category-wise spending charts

7️⃣ Export Data
Download CSV reports
Use externally for deeper analysis

📁 Project Structure

moneymap/
│
├── config/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── tracker/
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   ├── admin.py
│   ├── templates/
│   └── management/
│       └── commands/
│           └── setup_currencies.py
│
├── templates/
│   └── base.html
│
├── static/
│
├── db.sqlite3
├── manage.py
├── requirements.txt
└── README.md

🗄️ Database Models (Summary)
UserProfile
Monthly income
Preferred currency
Linked to Django User

Transaction
Title
Amount
Date
Category
Type (Income / Expense)
Description

Category
Name
Type (Income / Expense)

BudgetGoal
Category
Monthly limit

Currency
Code
Name
Symbol

🔌 Key Routes
| Route                | Purpose             |
| -------------------- | ------------------- |
| `/`                  | Landing page        |
| `/register/`         | User registration   |
| `/dashboard/`        | Main dashboard      |
| `/add-transaction/`  | Add transaction     |
| `/analytics/`        | Financial analytics |
| `/budget-goals/`     | Budget management   |
| `/profile-settings/` | User preferences    |
| `/export/`           | CSV export          |


🔧 Troubleshooting
Django not found
pip install django

Database errors
python manage.py makemigrations
python manage.py migrate

Currency errors
python manage.py setup_currencies

Port already in use
python manage.py runserver 8080

🔒 Security Highlights
CSRF protection
Password hashing
ORM-based SQL injection prevention
XSS-safe templates
Secure session handling

📊 Performance Notes
Paginated transaction lists
Optimized ORM queries
Scalable for PostgreSQL
Export-friendly data handling

📌 Project Status
Version: 1.0.0
Last Updated: December 2025
Python: 3.8+
Django: 5.0+
