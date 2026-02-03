# 🌍 EcoSwap: Community-Driven Circular Marketplace

**EcoSwap** is a full-stack Django application designed to reduce waste by facilitating a direct "Give-and-Take" economy. The platform enables users to list underutilized assets and connect with others for local swaps, directly supporting environmental sustainability goals.

---

## 🚀 Key Features

* **Real-time Interaction Engine**: A robust `SwapRequest` system allowing users to signal interest and message owners directly.
* **Automated Inventory Management**: Once a swap is accepted, the item is automatically removed from the public gallery to prevent duplicate requests.
* **Personalized Dashboards**: User-centric views for tracking 'Incoming' and 'Outgoing' requests with status updates (Pending/Accepted/Rejected).

---

## 🛠️ Tech Stack

* **Backend**: Django 5.x (Python 3.11)
* **Frontend**: HTML5, CSS3, JavaScript
* **Database**: MySQL
* **Version Control**: Git & GitHub

---

## 💻 Local Setup & Installation

Follow these steps to run the project locally in your environment (e.g., IntelliJ):

1. **Clone the repository**:
   ```bash
   git clone [https://github.com/Ujjawal-Bisht/MarketPlace-1](https://github.com/Ujjawal-Bisht/MarketPlace-1)
   ```

2. Initialize Virtual Environment
Create and activate a virtual environment to keep dependencies isolated:

### Create the environment
```
python -m venv venv
```

### Activate it (Windows)
```
venv\Scripts\activate
```

### Activate it (Mac/Linux)
```
source venv/bin/activate
```

3. Install Dependencies
Install the required Django framework:

```
pip install requirements.txt
```

4. Apply Database Migrations
Set up your local SQLite database based on the project models:

```
python manage.py makemigrations
python manage.py migrate
```

5. Launch the Development Server

Start the local server:
```
python manage.py runserver
```
Once running, open your browser and go to http://127.0.0.1:8000/ to view the app.

6. Create a Superuser (Admin) To access the Django Admin panel and manage categories or users:
```
python manage.py createsuperuser
```

## Team:

[Shraddha] (https://github.com/shraddha1603) <br>
[Ujjawal Bisht] (https://github.com/Ujjawal-Bisht/)<br>
[Riya] (https://github.com/riyasharma-coder)<br>
[Shivani Sisodiya] (https://github.com/ShivaniRSisodiya)<br>
[Parineet] (https://github.com/Parineet0509)