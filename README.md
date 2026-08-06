FinSight Analytics - Business Intelligence Dashboard
📊 Overview

FinSight Analytics is a full-stack Business Intelligence Dashboard built using Flask, Python, MySQL, HTML, CSS, Bootstrap, and JavaScript. It helps businesses manage customers, products, sales, and reports through an intuitive dashboard with real-time analytics and interactive charts.

✨ Features
🔐 User Authentication (Login & Register)
👥 Customer Management (Add, Edit, Delete, Search)
📦 Product Management (Add, Edit, Delete, Search)
📈 Sales Analytics Dashboard
📊 Interactive Charts using Chart.js
📄 Business Reports
📥 Export Customer Data to CSV
📱 Responsive Bootstrap UI
🗄️ MySQL Database Integration

🛠️ Tech Stack
Frontend
HTML5
CSS3
Bootstrap 5
JavaScript
Chart.js
Backend
Python
Flask
Database
MySQL

📁 Project Structure
FinSight-Analytics/
│
├── app.py
├── config.py
├── database.sql
├── requirements.txt
│
├── templates/
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── customers.html
│   ├── add_customer.html
│   ├── edit_customer.html
│   ├── products.html
│   ├── add_product.html
│   ├── edit_product.html
│   ├── sales.html
│   └── reports.html
│
├── static/
│   ├── css/
│   ├── js/
│   └── images/
│
├── routes/
│   ├── auth.py
│   ├── customer.py
│   ├── product.py
│   └── sales.py
│
├── models/
│   ├── user.py
│   ├── customer.py
│   ├── product.py
│   └── order.py
│
└── utils/
    └── database.py

