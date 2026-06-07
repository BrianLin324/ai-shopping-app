import json
import pandas as pd
import sys
from pathlib import Path
from sentence_transformers import SentenceTransformer

sys.path.append(str(Path(__file__).resolve().parents[1]))

from app.database import SessionLocal, engine, Base
from app.models import Product


CATALOG_PATH = Path(__file__).resolve().parents[2] / "data" / "products_catalog.csv"

MODEL_NAME = "sentence-transformers/paraphrase-MiniLM-L3-v2"


def clean_value(value):
    if pd.isna(value):
        return None
    return str(value).strip()


def main():
    Base.metadata.create_all(bind=engine)

    if not CATALOG_PATH.exists():
        raise FileNotFoundError(f"Could not find catalog file: {CATALOG_PATH}")

    print("Loading embedding model...")
    model = SentenceTransformer(MODEL_NAME)

    df = pd.read_csv(CATALOG_PATH)

    db = SessionLocal()

    try:
        inserted = 0

        for _, row in df.iterrows():
            product_id = clean_value(row.get("product_id"))

            if not product_id:
                continue

            existing = db.query(Product).filter(Product.product_id == product_id).first()
            if existing:
                continue

            name = clean_value(row.get("name")) or "Unnamed Product"
            description = clean_value(row.get("description")) or ""

            embedding_text = f"{name}. {description}"
            embedding_vector = model.encode(embedding_text).tolist()

            product = Product(
                product_id=product_id,
                name=name,
                description=description,
                price=float(row.get("price")) if not pd.isna(row.get("price")) else None,
                brand=clean_value(row.get("brand")),
                category=clean_value(row.get("category")),
                subcategory=clean_value(row.get("subcategory")),
                category_path=clean_value(row.get("category_path")),
                type=clean_value(row.get("type")),
                image_url=clean_value(row.get("image_url")),
                embedding=json.dumps(embedding_vector),
            )

            db.add(product)
            inserted += 1

        db.commit()
        print(f"Catalog loaded successfully. Inserted {inserted} products with embeddings.")

    finally:
        db.close()


if __name__ == "__main__":
    main()