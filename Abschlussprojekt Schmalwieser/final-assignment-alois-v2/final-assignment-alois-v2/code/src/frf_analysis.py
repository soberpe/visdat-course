from __future__ import annotations
import numpy as np
import scipy.signal as sig

def estimate_fs(t_s: np.ndarray) -> float:
    """Estimate sampling frequency from time vector."""
    dt = float(np.mean(np.diff(t_s)))
    if not np.isfinite(dt) or dt <= 0:
        raise ValueError("Invalid time vector; cannot estimate sampling frequency.")
    return 1.0 / dt

def compute_frf_h1_and_coherence(acc: np.ndarray, force: np.ndarray, fs: float, nperseg: int = 4096):
    """Compute FRF (H1) and coherence from time signals.

    H1: H = S_af / S_ff
    Coherence: gamma^2(f) in [0,1]
    """
    acc = sig.detrend(acc)
    force = sig.detrend(force)

    f, S_ff = sig.welch(force, fs=fs, nperseg=nperseg)
    _, S_af = sig.csd(acc, force, fs=fs, nperseg=nperseg)

    H = S_af / (S_ff + np.finfo(float).eps)

    f_coh, coh = sig.coherence(acc, force, fs=fs, nperseg=nperseg)
    if len(f_coh) != len(f) or np.max(np.abs(f_coh - f)) > 1e-9:
        coh = np.interp(f, f_coh, coh)

    return f, H, coh

def avg_magnitude(frfs: list[np.ndarray]) -> np.ndarray:
    mags = np.vstack([np.abs(H) for H in frfs])
    return mags.mean(axis=0)

def pick_modes_peak_picking(f: np.ndarray, M: np.ndarray, n_modes: int = 5, fmax: float = 60.0, prominence_rel: float = 0.05):
    mask = f <= fmax
    if not np.any(mask):
        return np.array([], dtype=int)

    prom = prominence_rel * float(np.max(M[mask]))
    peaks, _ = sig.find_peaks(M[mask], prominence=prom)
    if peaks.size == 0:
        return np.array([], dtype=int)

    full_idx = np.flatnonzero(mask)[peaks]
    top = full_idx[np.argsort(M[full_idx])[::-1]][:n_modes]
    return np.sort(top)

def participation_vector_windowed(frfs: list[np.ndarray], f: np.ndarray, idx_center: int, band_hz: float, ref: int = 0) -> np.ndarray:
    """Complex participation vector by averaging FRF values in ±band_hz around the peak."""
    f0 = float(f[idx_center])
    idx_window = np.where((f >= f0 - band_hz) & (f <= f0 + band_hz))[0]
    if idx_window.size == 0:
        idx_window = np.array([idx_center], dtype=int)

    v = np.array([np.mean(H[idx_window]) for H in frfs], dtype=complex)

    if np.abs(v[ref]) > 0:
        v = v * np.exp(-1j * np.angle(v[ref]))

    m = np.max(np.abs(v))
    if m > 0:
        v = v / m
    return v
