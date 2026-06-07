# AI Shopping Application

A full-stack AI-powered shopping application built with React, FastAPI, SQLite, and Sentence Transformers.

This project demonstrates authentication, product browsing, semantic product search, user activity tracking, and personalized recommendations based on onboarding, search, view, and purchase behavior.

## Features

* User signup and login
* JWT-based authentication
* Secure password hashing
* Product catalog with 5,000 products
* Natural-language semantic search
* Personalized recommendations
* Related product recommendations
* User onboarding
* Search, view, and purchase activity tracking
* React frontend connected to FastAPI backend

## Tech Stack

### Frontend

* React
* Vite
* JavaScript
* CSS

### Backend

* FastAPI
* SQLAlchemy
* SQLite
* JWT Authentication
* bcrypt password hashing

### AI / Machine Learning

* Sentence Transformers
* Product description embeddings
* Cosine similarity search
* User-profile-based recommendations

## How Semantic Search Works

Each product name and description is converted into an embedding vector using a Sentence Transformers model.

When a user searches with natural language, the query is also converted into an embedding. The backend compares the query embedding against product embeddings using cosine similarity and returns the most relevant products.

Example queries:

* "things for cooking dinner at home"
* "something useful for charging my phone"
* "a gift for a kid who likes games"

## How Recommendations Work

The app records user activity, including:

* Onboarding interests
* Searches
* Product views
* Purchases

The recommendation system builds a user profile from those signals and recommends products with similar embeddings that the user has not already interacted with.

## Project Structure

```text
ai-shopping-app/
├── backend/
│   ├── app/
│   │   ├── auth.py
│   │   ├── database.py
│   │   ├── main.py
│   │   ├── models.py
│   │   ├── recommendations.py
│   │   ├── schemas.py
│   │   └── search.py
│   ├── scripts/
│   │   └── load_catalog.py
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   └── App.css
│   └── package.json
│
├── data/
│   ├── products_catalog.csv
│   └── categories.csv
│
└── README.md
```

## Running Locally

### Backend

```bash
cd backend
pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

Backend API docs:

```text
http://127.0.0.1:8000/docs
```

### Load Product Catalog

```bash
cd backend
python scripts/load_catalog.py
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend URL:

```text
http://localhost:5173
```

## Main API Endpoints

### Auth

```text
POST /auth/signup
POST /auth/login
```

### Products

```text
GET /products
GET /products/{product_id}
GET /products/{product_id}/related
```

### AI Features

```text
GET /search?q=...
GET /recommendations
```

### Activity

```text
POST /onboarding
POST /purchase
```

## Screenshots

Screenshots will be added in the `screenshots/` folder.

Recommended screenshots:

* Signup and onboarding
* Product browsing
* Semantic search results
* Personalized recommendations

## Future Improvements

* Add shopping cart
* Add checkout flow
* Add order history
* Improve frontend styling
* Add pagination and filters
* Deploy frontend and backend
* Add automated tests
* Replace SQLite with PostgreSQL for production
* Use a vector database for larger catalogs

## Resume Summary

Built an AI-powered e-commerce application using React, FastAPI, SQLite, and Sentence Transformers. Implemented JWT authentication, semantic product search over 5,000 products, user activity tracking, and personalized recommendations based on onboarding, search, view, and purchase behavior.
