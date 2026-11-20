"""CLI and immutable artifact writer for bounded memory scenario №13."""
import argparse
import json
import platform
import uuid
from datetime import datetime, timezone
from pathlib import Path
from .scenarios.article13 import run

def main():
    parser = argparse.ArgumentParser(description="HIAI research scenario 13")
    parser.add_argument("command", choices=["run","list"])
    parser.add_argument("article_id", nargs="?", default="13")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--out", type=Path, default=Path("results/local"))
    a = parser.parse_args()
    if a.command == "list":
        print("13 — bounded exact-string memory window")
        return 0
    if a.article_id != "13":
        parser.error("This repository contains scenario 13 only")
    result = run(seed=a.seed)
    result["created_utc"] = datetime.now(timezone.utc).isoformat()
    result["python_version"] = platform.python_version()
    a.out.mkdir(parents=True, exist_ok=True)
    dest = a.out / ("article-13-" + uuid.uuid4().hex[:12] + ".json")
    with dest.open("x", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    print(dest)
    return 0
