from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from .search import semantic_search
from .recommendations import recommend_products
from fastapi.middleware.cors import CORSMiddleware

from .database import Base, engine, get_db
from .models import User, Product, Activity
from .schemas import SignupRequest, LoginRequest, ProductResponse, OnboardingRequest, PurchaseRequest
from .auth import hash_password, verify_password, create_access_token, get_current_user

Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Shopping App")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5174",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/auth/signup")
def signup(payload: SignupRequest, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == payload.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    user = User(
        email=payload.email,
        password_hash=hash_password(payload.password)
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    token = create_access_token({"sub": str(user.id)})

    return {
        "message": "User created",
        "access_token": token,
        "token_type": "bearer"
    }


@app.post("/auth/login")
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()

    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = create_access_token({"sub": str(user.id)})

    return {
        "access_token": token,
        "token_type": "bearer"
    }


@app.get("/products", response_model=list[ProductResponse])
def get_products(
    page: int = 1,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    offset = (page - 1) * limit
    return db.query(Product).offset(offset).limit(limit).all()

@app.get("/recommendations")
def get_recommendations(
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    results = recommend_products(db, current_user.id, limit)

    return [
        {
            "score": item["score"],
            "product": {
                "product_id": item["product"].product_id,
                "name": item["product"].name,
                "description": item["product"].description,
                "price": item["product"].price,
                "brand": item["product"].brand,
                "category": item["product"].category,
                "subcategory": item["product"].subcategory,
                "image_url": item["product"].image_url,
            }
        }
        for item in results
    ]

@app.get("/products/{product_id}", response_model=ProductResponse)
def get_product(
    product_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    product = db.query(Product).filter(Product.product_id == product_id).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    activity = Activity(
        user_id=current_user.id,
        product_id=product_id,
        activity_type="view"
    )
    db.add(activity)
    db.commit()

    return product


@app.post("/onboarding")
def onboarding(
    payload: OnboardingRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    activity = Activity(
        user_id=current_user.id,
        query=payload.interests,
        activity_type="onboarding"
    )
    db.add(activity)
    db.commit()

    return {"message": "Onboarding saved"}


@app.post("/purchase")
def purchase(
    payload: PurchaseRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    product = db.query(Product).filter(Product.product_id == payload.product_id).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    activity = Activity(
        user_id=current_user.id,
        product_id=payload.product_id,
        activity_type="purchase"
    )
    db.add(activity)
    db.commit()

    return {"message": "Purchase recorded"}

@app.get("/search")
def search_products(
    q: str,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not q or len(q.strip()) < 2:
        raise HTTPException(status_code=400, detail="Search query is too short")

    activity = Activity(
        user_id=current_user.id,
        query=q,
        activity_type="search"
    )
    db.add(activity)
    db.commit()

    results = semantic_search(db, q, limit)

    return [
        {
            "score": item["score"],
            "product": {
                "product_id": item["product"].product_id,
                "name": item["product"].name,
                "description": item["product"].description,
                "price": item["product"].price,
                "brand": item["product"].brand,
                "category": item["product"].category,
                "subcategory": item["product"].subcategory,
                "image_url": item["product"].image_url,
            }
        }
        for item in results
    ]

@app.get("/products/{product_id}/related")
def related_products(
    product_id: str,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    product = db.query(Product).filter(Product.product_id == product_id).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    if not product.embedding:
        return []

    import json
    from .search import cosine_similarity

    target_embedding = json.loads(product.embedding)

    products = db.query(Product).filter(Product.embedding.isnot(None)).all()

    scored = []

    for other in products:
        if other.product_id == product_id:
            continue

        try:
            other_embedding = json.loads(other.embedding)
        except Exception:
            continue

        score = cosine_similarity(target_embedding, other_embedding)

        scored.append({
            "score": score,
            "product": {
                "product_id": other.product_id,
                "name": other.name,
                "description": other.description,
                "price": other.price,
                "brand": other.brand,
                "category": other.category,
                "subcategory": other.subcategory,
                "image_url": other.image_url,
            }
        })

    scored.sort(key=lambda x: x["score"], reverse=True)

    return scored[:limit]