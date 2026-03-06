# 🌍 EcoSwap — Community-Driven Circular Marketplace

**EcoSwap** is a full-stack web application built with **Django** that promotes sustainable living by enabling users to **exchange or donate reusable household items** instead of discarding them.
The platform creates a **community-driven circular marketplace**, reducing waste and encouraging responsible consumption.

By connecting individuals who want to give away items with those who need them, EcoSwap helps **extend product lifecycles and minimize landfill waste**.

---

# 🚀 Key Features

### 🔁 Interactive Swap Request Workflow

Users can send swap requests for listed items and communicate directly with item owners.
Owners can **accept or reject requests**, enabling a structured and transparent exchange process.

### 📦 Automated Inventory Control

Once a swap request is accepted, the item is **automatically removed from the public listings** to prevent duplicate or conflicting requests.

### 📊 Personalized User Dashboards

Each user has a dashboard that displays:

* Incoming swap requests
* Outgoing requests
* Request status updates *(Pending / Accepted / Rejected)*

### 🗂️ Optimized Item Categorization

Items can be listed under **7 structured categories**:

* Electronics
* Furniture
* Books
* Clothing
* Toys
* Kitchenware
* General

This ensures easier discovery and browsing.

### 🔐 Secure Authentication System

Django's built-in authentication system ensures:

* Secure password hashing
* Protected login sessions
* Access control for user actions

---

# 🛠️ Technology Stack

### Backend

* **Django 5.x**
* Python 3.11
* MVC-based architecture
* Built-in authentication and ORM

### Frontend

* Semantic **HTML5**
* **CSS3**
* Django Template Engine
* Responsive UI structure

### Database

* **SQLite3 (Relational Database)**
  Used for efficient development and lightweight deployment.

### Development Tools

* **Git & GitHub** — Version control
* **VS Code / IntelliJ** — Development environment

---

# 🏗️ System Workflow

1. User registers or logs into the platform
2. User lists an item under a category
3. Other users browse available items
4. Interested users send a **swap request**
5. Item owner reviews the request
6. Owner accepts or rejects the request
7. If accepted, the item is **removed from public listings**

---

# 💻 Local Setup & Installation

Follow these steps to run EcoSwap locally.

---

## 1️⃣ Clone the Repository

```bash
git clone https://github.com/riyasharma-coder/MarketPlace.git
cd MarketPlace
```

---

## 2️⃣ Create a Virtual Environment

Create a virtual environment to isolate project dependencies.

```bash
python -m venv venv
```

### Activate Environment

**Windows**

```
venv\Scripts\activate
```

**Mac / Linux**

```
source venv/bin/activate
```

---

## 3️⃣ Install Dependencies

Install Django:

```bash
pip install django
```

*(Optional improvement)*

```bash
pip install -r requirements.txt
```

---

## 4️⃣ Apply Database Migrations

Initialize the SQLite database.

```bash
python manage.py makemigrations
python manage.py migrate
```

---

## 5️⃣ Run the Development Server

```bash
python manage.py runserver
```

Open your browser and visit:

```
http://127.0.0.1:8000/
```

---

## 6️⃣ Create an Admin Account

To access the Django Admin panel:

```bash
python manage.py createsuperuser
```

Admin panel URL:

```
http://127.0.0.1:8000/admin
```

---

# 📈 Future Improvements

* Geolocation based item discovery
* Real-time notifications for swap requests
* Mobile-friendly progressive web app
* AI-based item recommendation system
* Integration with recycling centers and NGOs

---

# 🤝 Contributors

* Shraddha(https://github.com/shraddha1603)
* Ujjawal Bisht(https://github.com/Ujjawal-Bisht)
* Riya Sharma(https://github.com/riyasharma-coder/)
* Shivani Sisodiya(https://github.com/ShivaniRSisodiya)
* Parineet Verma(https://github.com/Parineet0509)


**Inderprastha Engineering College, Ghaziabad**

---

# 🌱 Impact

EcoSwap encourages a **circular economy** by enabling communities to reuse items instead of discarding them, reducing environmental waste and promoting sustainable consumption.
