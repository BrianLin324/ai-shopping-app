import json
import numpy as np
from sqlalchemy.orm import Session
from sentence_transformers import SentenceTransformer

from .models import Product, Activity
from .search import cosine_similarity, MODEL_NAME


_model = None


def get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer(MODEL_NAME)
    return _model


def build_user_profile(db: Session, user_id: int):
    activities = db.query(Activity).filter(Activity.user_id == user_id).all()

    vectors = []

    for activity in activities:
        if activity.product_id:
            product = db.query(Product).filter(Product.product_id == activity.product_id).first()
            if product and product.embedding:
                vectors.append(json.loads(product.embedding))

        if activity.query:
            model = get_model()
            vectors.append(model.encode(activity.query).tolist())

    if not vectors:
        return None

    return np.mean(np.array(vectors), axis=0).tolist()


def recommend_products(db: Session, user_id: int, limit: int = 10):
    profile = build_user_profile(db, user_id)

    if profile is None:
        return []

    seen_product_ids = {
        a.product_id
        for a in db.query(Activity).filter(Activity.user_id == user_id).all()
        if a.product_id
    }

    products = db.query(Product).filter(Product.embedding.isnot(None)).all()

    scored = []

    for product in products:
        if product.product_id in seen_product_ids:
            continue

        try:
            product_embedding = json.loads(product.embedding)
        except Exception:
            continue

        score = cosine_similarity(profile, product_embedding)

        scored.append({
            "product": product,
            "score": score
        })

    scored.sort(key=lambda x: x["score"], reverse=True)

    return scored[:limit]