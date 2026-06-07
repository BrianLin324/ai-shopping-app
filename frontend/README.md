# AI Shopping Application

AI-powered e-commerce application built with React, FastAPI, SQLite, and Sentence Transformers.

## Features

### Authentication

* User signup and login
* JWT-based authentication
* Secure password hashing

### Product Catalog

* Browse products
* Product detail retrieval
* Purchase tracking

### AI Features

* Semantic product search using embeddings
* Personalized recommendations
* Related product recommendations
* User onboarding and preference tracking

## Tech Stack

### Frontend

* React
* Vite
* JavaScript

### Backend

* FastAPI
* SQLAlchemy
* SQLite
* JWT Authentication

### AI / Machine Learning

* Sentence Transformers
* Embedding Similarity Search
* Recommendation Engine

## Architecture

Frontend (React)
↓
FastAPI REST API
↓
SQLite Database
↓
Embedding Search & Recommendation Engine

## Local Setup

### Backend

```bash
cd backend
pip install -r requirements.txt
py -m uvicorn app.main:app --reload
```

Backend API:

```text
http://127.0.0.1:8000/docs
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend:

```text
http://localhost:5173
```

## Main Endpoints

### Authentication

```text
POST /auth/signup
POST /auth/login
```

### Products

```text
GET /products
GET /products/{product_id}
```

### AI Features

```text
GET /search
GET /recommendations
GET /products/{product_id}/related
```

### User Activity

```text
POST /onboarding
POST /purchase
```

## Project Highlights

* Built a full-stack AI-powered shopping application from scratch.
* Implemented semantic search over a catalog of 5,000 products.
* Developed personalized recommendations using onboarding, search history, and purchase activity.
* Integrated React frontend with FastAPI backend through authenticated REST APIs.
