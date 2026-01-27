from __future__ import annotations
import numpy as np
import scipy.signal as sig

def estimate_fs(t_s: np.ndarray) -> float:
    dt = np.mean(np.diff(t_s))
    if not np.isfinite(dt) or dt <= 0:
        raise ValueError("Invalid time vector; cannot estimate sampling rate.")
    return 1.0 / dt

def compute_frf_h1(acc: np.ndarray, force: np.ndarray, fs: float, nperseg: int = 4096):
    """Compute FRF using H1 estimator: H = S_af / S_ff.

    Returns f [Hz], H(f) complex.
    """
    acc = sig.detrend(acc)
    force = sig.detrend(force)

    f, S_ff = sig.welch(force, fs=fs, nperseg=nperseg)
    _, S_af = sig.csd(acc, force, fs=fs, nperseg=nperseg)  # S_yx

    # avoid divide-by-zero
    eps = np.finfo(float).eps
    H = S_af / (S_ff + eps)
    return f, H

def avg_magnitude(frfs: list[np.ndarray]) -> np.ndarray:
    mags = np.vstack([np.abs(H) for H in frfs])
    return mags.mean(axis=0)
