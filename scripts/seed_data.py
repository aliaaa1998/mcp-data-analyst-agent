from app.db.session import SessionLocal
from app.services.data_loader import load_sample_data

if __name__ == "__main__":
    db = SessionLocal()
    try:
        print(load_sample_data(db))
    finally:
        db.close()
