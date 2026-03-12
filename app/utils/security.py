import re
from pathlib import Path

SAFE_FILE_RE = re.compile(r"^[a-zA-Z0-9_.-]+$")


def sanitize_filename(name: str) -> str:
    if not SAFE_FILE_RE.match(name):
        raise ValueError("Unsafe filename")
    return name


def safe_join(base: str, child: str) -> Path:
    child = sanitize_filename(child)
    path = Path(base) / child
    path = path.resolve()
    base_path = Path(base).resolve()
    if base_path not in path.parents and base_path != path.parent:
        raise ValueError("Unsafe path")
    return path
