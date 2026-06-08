# 🛒 E-Com API

![Python 3.11](https://img.shields.io/badge/Python-3.11-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue.svg)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg)

A complete, production-ready E-Commerce Backend API built using **Python**, **FastAPI**, **SQLAlchemy**, and **PostgreSQL**. The project is fully containerized with **Docker** and **Docker Compose** for seamless local setup.

---

## 🚀 Features

* **🔑 Phone-Number Authentication:** Secure registration, login, and profile fetching using JWT (JSON Web Tokens) with passwords hashed via `bcrypt`.
* **📦 Product Catalog:** Read, search, create, update, and delete products, categorized by sections (e.g., Electronics, Clothing, Footwear).
* **🛒 Shopping Cart:** Add items to cart, dynamically update quantities, and calculate totals.
* **📋 Order & Inventory Management:** Place orders, automatically decrement product stock on successful checkout, cancel pending orders to restore inventory stock, and track delivery status.
* **📍 Address Management:** Save multiple shipping addresses and configure default shipping location preferences.
* **💳 Payment Gateway Integration:** Draft templates ready to integrate with payment gateways like Razorpay or Stripe (`/payments/initiate` and `/payments/verify`).
* **🛡️ Admin Operations:** Dedicated routes for administrators (based on `user_id == 1`) to fetch overall sales statistics, create products, and update order statuses.
* **🐳 Docker Orchestration:** Multi-container configuration out of the box using PostgreSQL 15 and FastAPI.

---

## 📂 Project Structure

```text
e-com-main/
├── app/
│   ├── models/           # SQLAlchemy Database Models (e.g., User model)
│   ├── routes/           # API Routers (Auth, Products, Cart, Orders, Addresses, Payments)
│   ├── schemas/          # Pydantic Schemas for Request/Response validation
│   ├── utils/            # Helper modules (e.g., SMTP/SMS templates)
│   ├── auth.py           # Password hashing & JWT Token generation logic
│   ├── database.py       # DB connections, Session generators, & state management
│   └── main.py           # Application entrypoint & CORS middleware setup
├── Dockerfile            # Docker image configuration for the FastAPI service
├── docker-compose.yml    # Service composer (FastAPI + Postgres)
└── requirements.txt      # Python dependencies

```

---

## ⚙️ Tech Stack & Dependencies

* **Language & Framework:** Python 3.11, FastAPI
* **Database & ORM:** PostgreSQL 15, SQLAlchemy 2.0
* **Security & Tokens:** `python-jose` (JWT), `passlib` with `bcrypt` (Secure password hashing)
* **Data Validation:** `pydantic` v2 (including phone number format regex validation)
* **Server:** `uvicorn` (ASGI Web Server)
* **Containerization:** Docker, Docker Compose

---

## 🛠️ Quick Start & Installation

### Option A: Run via Docker Compose (Recommended)

This is the fastest way to get the entire project up and running with a Postgres database without installing local Python dependencies.

1. **Create a `.env` file** in the root directory:

```env
   POSTGRES_USER=postgres
   POSTGRES_PASSWORD=secure_password_here
   POSTGRES_DB=ecommerce

```

2. **Start the containers:**

```bash
   docker compose up --build

```

3. **Verify the installation:**

* API server: [http://localhost:8000](https://www.google.com/search?q=http://localhost:8000)
* Swagger UI Docs: [http://localhost:8000/docs](https://www.google.com/search?q=http://localhost:8000/docs)
* ReDoc Docs: [http://localhost:8000/redoc](https://www.google.com/search?q=http://localhost:8000/redoc)

---

### Option B: Run Locally (Manual Setup)

If you prefer to run the application outside of Docker:

1. **Create and activate a Python virtual environment:**

```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate

```

2. **Install dependencies:**

```bash
   pip install -r requirements.txt

```

3. **Configure environment variables:**
Set up your environment variables locally. For example, in Bash:

```bash
   export POSTGRES_USER=postgres
   export POSTGRES_PASSWORD=secure_password_here
   export POSTGRES_DB=ecommerce
   export DATABASE_URL=postgresql://postgres:secure_password_here@localhost:5432/ecommerce

```

4. **Run the application:**

```bash
   uvicorn app.main:app --reload

```

Now access the interactive docs at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

---

## 📡 API Endpoints

The API is fully documented using OpenAPI standards. View the interactive `/docs` route for full payload schemas.

* **🔑 Authentication (`/auth`):** Signup, Login, Fetch current user (`/auth/me`).
* **📦 Products (`/products`):** CRUD operations for the product catalog.
* **🛒 Shopping Cart (`/cart`):** Add, update, and remove items; calculate totals.
* **📋 Orders (`/orders`):** Place orders, view history, cancel pending orders.
* **📍 Addresses (`/addresses`):** Manage shipping addresses and set defaults.
* **💳 Payments (`/payments`):** Mock gateway initialization and verification.
* **🛡️ Admin (`/admin`):** System-wide order tracking and product management.

---

## 💡 Architecture Note

The project is designed in a modular, route-separated fashion:

* **Database Architecture:** Currently implements a hybrid state model. While SQLAlchemy models manage persistent structures (e.g., Users) in PostgreSQL, other parts of the app utilize in-memory storage structures (`_db` lists inside `database.py`) for rapid local prototyping.
* **Testing:** To test endpoints locally, utilize the interactive Swagger UI (`/docs`) or import the API routes into client utilities such as Postman.

---

## 🤝 Contributing

Contributions are welcome! If you'd like to improve the API or help migrate the remaining in-memory structures fully to PostgreSQL, please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature-name`).
3. Commit your changes (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature/your-feature-name`).
5. Open a Pull Request.

---
