from __future__ import annotations
import pandas as pd

def load_lvm_time_force_acc(path: str) -> pd.DataFrame:
    """Load LabVIEW .lvm time-domain measurement.

    Expects a tab-separated table with columns including:
      - X_Value (time)
      - Acceleration
      - Force

    Returns DataFrame with columns:
      - t_s
      - acc_g
      - force_N
    """
    with open(path, "r", errors="ignore") as f:
        lines = f.readlines()

    start = None
    for i, l in enumerate(lines):
        s = l.strip()
        if s.startswith("X_Value") and ("Acceleration" in s) and ("Force" in s):
            start = i
            break
    if start is None:
        raise ValueError("Could not find data header line in .lvm file.")

    df = pd.read_csv(path, sep="\t", decimal=",", skiprows=start, engine="python")
    cols = df.columns.tolist()

    # Find accel/force columns robustly
    acc_col = next((c for c in cols if "Acceleration" in c), None)
    force_col = next((c for c in cols if "Force" in c), None)
    if acc_col is None or force_col is None:
        raise ValueError(f"Missing expected columns in {path}. Found: {cols}")

    t_col = cols[0]
    out = df[[t_col, acc_col, force_col]].rename(columns={t_col: "t_s", acc_col: "acc_g", force_col: "force_N"})
    out = out.dropna()
    return out
