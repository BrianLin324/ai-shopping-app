import json
import numpy as np
from sentence_transformers import SentenceTransformer
from sqlalchemy.orm import Session

from .models import Product


MODEL_NAME = "sentence-transformers/paraphrase-MiniLM-L3-v2"

_model = None


def get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer(MODEL_NAME)
    return _model


def cosine_similarity(a, b):
    a = np.array(a)
    b = np.array(b)

    denominator = np.linalg.norm(a) * np.linalg.norm(b)

    if denominator == 0:
        return 0.0

    return float(np.dot(a, b) / denominator)


def semantic_search(db: Session, query: str, limit: int = 10):
    query = query.strip()

    if len(query) < 2:
        return []

    model = get_model()
    query_embedding = model.encode(query).tolist()

    products = db.query(Product).filter(Product.embedding.isnot(None)).all()

    scored_results = []

    for product in products:
        try:
            product_embedding = json.loads(product.embedding)
        except Exception:
            continue

        score = cosine_similarity(query_embedding, product_embedding)

        scored_results.append(
            {
                "product": product,
                "score": score,
            }
        )

    scored_results.sort(key=lambda item: item["score"], reverse=True)

    return scored_results[:limit]