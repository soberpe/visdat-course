from __future__ import annotations
import pandas as pd

def load_lvm_time_force_acc(path: str) -> pd.DataFrame:
    """Load LabVIEW .lvm time-domain data (time, acceleration, force).

    The header length varies, so we search for the table header line that starts
    with 'X_Value' and contains 'Acceleration' and 'Force'.

    Returns columns:
      - t_s      time [s]
      - acc_g    acceleration [g]
      - force_N  force [N]
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
        raise ValueError(
            "Could not find data header line in .lvm file. "
            "Expected line starting with 'X_Value' containing 'Acceleration' and 'Force'."
        )

    df = pd.read_csv(path, sep="\t", decimal=",", skiprows=start, engine="python")
    cols = df.columns.tolist()

    t_col = cols[0]
    acc_col = next((c for c in cols if "Acceleration" in c), None)
    force_col = next((c for c in cols if "Force" in c), None)
    if acc_col is None or force_col is None:
        raise ValueError(f"Missing expected columns. Found: {cols}")

    out = df[[t_col, acc_col, force_col]].rename(
        columns={t_col: "t_s", acc_col: "acc_g", force_col: "force_N"}
    ).dropna()
    return out
