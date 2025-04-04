# 🦸‍♀️ Superheroes API

This is a Flask-based RESTful API for managing superheroes, their powers, and their relationships. It supports creating, retrieving, and updating heroes, powers, and hero-power associations.

🔗 **GitHub Repository:** [github.com/Khalid1170/Superheros](https://github.com/Khalid1170/Superheros)

---

## 📚 This README Goes Over:

- Project Overview
- Project Structure
- Setup Instructions
- Testing with Postman
- API Endpoints and Expected Outputs
- Tech Stack
- License Information

---

## 📁 Project Structure

```
superheros/
├── app.py             # Main Flask app with routes
├── models.py          # SQLAlchemy models
├── migrations/        # Alembic migrations
├── heroes.db          # SQLite database
├── seed.py            # Seed script to populate the database
├── Pipfile            # Pipenv dependency management
├── Pipfile.lock       # Pipenv lock file
└── README.md          # Project documentation
```

---

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/Khalid1170/Superheros.git
cd Superheros
```

### 2. Install Dependencies with Pipenv

If you haven’t installed Pipenv yet, you can install it using:

```bash
pip install pipenv
```

### 3. Enter Virtual Environment

```bash
pipenv shell
```

### 4. Install Dependencies

```bash
pipenv install
```

### 5. Run Migrations

```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

### 6. Seed the Database

```bash
python seed.py
```

### 7. Start the Server

```bash
flask run
```

---

## 🧪 Testing with Postman

### 🔸 Base URL:  
```
http://localhost:5000
```

---

## 🔹 GET /heroes

- **Method:** `GET`  
- **URL:** `http://localhost:5000/heroes`

**Expected Output:**
```json
[
  {
    "id": 1,
    "name": "Kamala Khan",
    "super_name": "Ms. Marvel"
  },
  ...
]
```

---

## 🔹 GET /heroes/:id

- **Method:** `GET`  
- **URL:** `http://localhost:5000/heroes/1`

**Expected Output:**
```json
{
  "id": 1,
  "name": "Kamala Khan",
  "super_name": "Ms. Marvel",
  "hero_powers": [
    {
      "id": 3,
      "hero_id": 1,
      "power_id": 2,
      "strength": "Weak",
      "power": {
        "id": 2,
        "name": "Flight",
        "description": "Allows the wielder to fly at high speeds and navigate through the air effortlessly."
      }
    }
  ]
}
```

---

## 🔹 GET /powers

- **Method:** `GET`  
- **URL:** `http://localhost:5000/powers`

**Expected Output:**
```json
[
  {
    "id": 1,
    "name": "Telekinesis",
    "description": "Move things with your mind."
  }
]
```

---

## 🔹 GET /powers/:id

- **Method:** `GET`  
- **URL:** `http://localhost:5000/powers/1`

**Expected Output:**
```json
{
  "id": 1,
  "name": "Telekinesis",
  "description": "Move things with your mind."
}
```

---

## 🔹 PATCH /powers/:id

- **Method:** `PATCH`  
- **URL:** `http://localhost:5000/powers/1`  
- **Body > JSON:**
```json
{
  "description": "Updated description for this power"
}
```

**Expected Output:**
```json
{
  "id": 1,
  "name": "Telekinesis",
  "description": "Updated description for this power"
}
```

---

## 🔹 POST /hero_powers

- **Method:** `POST`  
- **URL:** `http://localhost:5000/hero_powers`  
- **Body > JSON:**
```json
{
  "hero_id": 1,
  "power_id": 2,
  "strength": "Average"
}
```

**Expected Output:**
```json
{
  "id": 11,
  "hero_id": 1,
  "power_id": 2,
  "strength": "Average",
  "hero": {
    "id": 1,
    "name": "Kamala Khan",
    "super_name": "Ms. Marvel"
  },
  "power": {
    "id": 2,
    "name": "Flight",
    "description": "Allows the wielder to fly at high speeds and navigate through the air effortlessly."
  }
}
```

❗ **Validation Note:**  
Strength must be `"Strong"`, `"Weak"`, or `"Average"` or else you'll get:
```json
{
  "errors": ["Validation errors"]
}
```

---

## 🧰 Tech Stack

- Python 3
- Flask
- Flask SQLAlchemy
- Flask Migrate (Alembic)
- SQLite
- Pipenv (for managing dependencies)
- Postman (for API testing)

---

## 📝 License

MIT License — Free to use and modify.
