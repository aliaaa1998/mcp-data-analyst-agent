from pathlib import Path

import pandas as pd
from sqlalchemy import text
from sqlalchemy.orm import Session

TABLES = ["sales", "products", "customers", "regions", "churn"]


def load_sample_data(db: Session, data_dir: str = "data") -> dict[str, int]:
    counts: dict[str, int] = {}
    for table in TABLES:
        csv_path = Path(data_dir) / f"{table}.csv"
        df = pd.read_csv(csv_path)
        df.to_sql(table, db.bind, if_exists="append", index=False)
        counts[table] = len(df)
    db.execute(text("ANALYZE"))
    db.commit()
    return counts
