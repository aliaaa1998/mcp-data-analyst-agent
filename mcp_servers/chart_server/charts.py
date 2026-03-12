from __future__ import annotations

import uuid
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def _save(fig: plt.Figure, out_dir: str) -> dict:
    Path(out_dir).mkdir(parents=True, exist_ok=True)
    chart_id = uuid.uuid4().hex[:12]
    path = Path(out_dir) / f"{chart_id}.png"
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    return {"chart_id": chart_id, "path": str(path)}


def create_line_chart(rows: list[dict], x: str, y: str, title: str, out_dir: str) -> dict:
    df = pd.DataFrame(rows)
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(df[x], df[y], marker="o")
    ax.set_title(title)
    ax.tick_params(axis="x", rotation=45)
    result = _save(fig, out_dir)
    return {**result, "title": title}


def create_bar_chart(rows: list[dict], x: str, y: str, title: str, out_dir: str) -> dict:
    df = pd.DataFrame(rows)
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(df[x], df[y])
    ax.set_title(title)
    ax.tick_params(axis="x", rotation=45)
    result = _save(fig, out_dir)
    return {**result, "title": title}


def create_pie_chart(rows: list[dict], labels: str, values: str, title: str, out_dir: str) -> dict:
    df = pd.DataFrame(rows)
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.pie(df[values], labels=df[labels], autopct="%1.1f%%")
    ax.set_title(title)
    result = _save(fig, out_dir)
    return {**result, "title": title}


def create_table_preview(rows: list[dict], max_rows: int = 10) -> dict:
    df = pd.DataFrame(rows)
    return {"preview": df.head(max_rows).to_dict(orient="records"), "rows": len(df)}
