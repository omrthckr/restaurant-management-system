# Restaurant Management System

A full-featured web-based restaurant management application developed as a term project for the Fundamentals of Software Engineering course (June 2025).

## 👥 Team Members

* Ozan Bülen (05220000972)
* Ömer Taha Çakır (05210000940)
* Oğulcan Kahraman (5180000053)
* Beste Yalca (5240000816)

---

## 🚀 Project Overview

The Restaurant Management System is designed to streamline operations for both customers and restaurant staff. It includes functionalities such as menu browsing, order placement, kitchen management, admin dashboard, and secure payment processing.

---

## 🧰 Technologies Used

* **Backend:** Python Flask
* **Frontend:** HTML5, CSS3, JavaScript
* **Database:** SQLite (dev), PostgreSQL (prod ready)
* **Security:** HTTPS, AES-256 encryption, GDPR/KVKK compliant

---

## 🔑 Features

### Customer Module

* View menu and food categories
* Add/remove items from cart
* Submit orders and view order history

### Kitchen Module

* View incoming orders
* Update order status (preparing, ready, completed)

### Admin Panel

* Manage tables (availability, reservations)
* Monitor inventory and ingredient stock
* Manage menu items and preparation times
* Staff management

### Payment

* Multi-method secure payments
* Encrypted transaction processing

### System

* Mobile-responsive UI
* RESTful APIs
* Role-based access control

---

## 📦 Installation

```bash
git clone https://github.com/omrthckr/restaurant-management-system.git
cd restaurant-management-system
pip install -r requirements.txt
```

Start the Flask app:

```bash
python app.py
```

Visit: `http://127.0.0.1:5000`

---

## 📸 Screenshots & Demo

> *Add screenshots manually in your Canva slides if needed.*

---

## 📝 Project Structure

```
restaurant-management-system/
├── app.py
├── fix_encoding.py
├── requirements.txt
├── admin_dashboard.html
├── kitchen_system.html
├── restaurant_menu_html.html
└── restaurant_env/  # (your virtual environment)
```

---

## 📚 Use Case Examples

* Customer places order → kitchen receives → admin tracks status
* Admin updates menu → changes reflected live
* Inventory drops below minimum → alert displayed

---

## ✅ Status

✅ Functional prototype ready for demonstration and submission.
🎯 30 system requirements met as per project documentation.

---

## 📄 License

This project was developed for academic purposes under Ege University. All rights reserved.
