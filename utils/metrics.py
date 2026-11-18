import sys
from pathlib

import pandas as pd

from src.pipeline import process

FILDS = ["name", "edicao", "collector_number"]

def _norm(v) -> str:
    return str(v).strip().lower().lstrip("0") if pd.notna(v) and v is not None else ""

def evaluate(folder: str) -> pd.DataFrame:
    folder = Path(folder)
    gab = pd.read_csv(folder / "gabarito.csv", dtype=str)
    rows = []
    for _, g in gab.iterrows():
        try:
            data, t = process(str(folder / g["arquivo"]))
            error = None
        except Exception as e:  # noqa: BLE001
            data, t, error = {}, {}, str(e)
        row = {"arquivo": g["arquivo"], "error": error, **{f"t_{k}": v for k, v in t.items()}}
        for c in FILDS:
            row[f"ok_{c}"] = _norm(data.get(c)) == _norm(g[c])
        row["validated"] = data.get("validated", False)
        rows.append(row)
    return pd.DataFrame(rows)

if __name__ == "__main__":
    df = evaluate(sys.argv[1] if len(sys.argv) > 1 else "utils/dataset_teste")
    df.to_csv("result_metrics.csv", index=False)
    print("Accuracy by field:")
    print(df[[c for c in df if c.startswith("ok_")]].mean().round(3))
    print("\nAverage time per step (s):")
    print(df[[c for c in df if c.startswith("t_")]].mean().round(3))
    print(f"\nFailures: {df['error'].notna().sum()} / {len(df)}")