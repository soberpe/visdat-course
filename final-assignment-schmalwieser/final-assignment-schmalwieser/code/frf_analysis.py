from __future__ import annotations

"""FRF analysis helpers.

This module contains the signal-processing parts of the project.

Change requested for the final submission:
- All *coherence* related code was removed. The analysis now only computes the FRF
  (H1 estimator) and derived modal/participation information.

Functions in this module are intentionally pure (no GUI code).
"""

import numpy as np
import scipy.signal as sig


def estimate_fs(t_s: np.ndarray) -> float:
    """Estimate sampling frequency from time vector.

    Parameters
    ----------
    t_s:
        Time vector in seconds.

    Returns
    -------
    fs:
        Sampling frequency in Hz.
    """
    dt = float(np.mean(np.diff(t_s)))
    if not np.isfinite(dt) or dt <= 0:
        raise ValueError("Invalid time vector; cannot estimate sampling frequency.")
    return 1.0 / dt


def compute_frf_h1(acc: np.ndarray, force: np.ndarray, fs: float, nperseg: int = 4096):
    """Compute FRF using the H1 estimator.

    H1 estimator:
        H(f) = S_af(f) / S_ff(f)

    where:
        S_ff ... auto spectrum of the input (force)
        S_af ... cross spectrum between output (acc) and input (force)

    Parameters
    ----------
    acc:
        Acceleration time signal (units: "g" in the provided dataset; we keep units as-is).
    force:
        Force time signal (N).
    fs:
        Sampling frequency (Hz).
    nperseg:
        Segment length for Welch/CSD.

    Returns
    -------
    f:
        Frequency vector (Hz).
    H:
        Complex FRF H(f) (acc/force).
    """
    acc = sig.detrend(acc)
    force = sig.detrend(force)

    f, S_ff = sig.welch(force, fs=fs, nperseg=nperseg)
    _, S_af = sig.csd(acc, force, fs=fs, nperseg=nperseg)

    # Numerical epsilon avoids division by zero.
    H = S_af / (S_ff + np.finfo(float).eps)
    return f, H


def avg_magnitude(frfs: list[np.ndarray]) -> np.ndarray:
    """Average magnitude spectrum |H(f)| across multiple FRFs."""
    mags = np.vstack([np.abs(H) for H in frfs])
    return mags.mean(axis=0)


def pick_modes_peak_picking(
    f: np.ndarray,
    M: np.ndarray,
    n_modes: int = 5,
    fmax: float = 60.0,
    prominence_rel: float = 0.05,
) -> np.ndarray:
    """Find modal peaks by simple peak picking.

    We peak-pick on the averaged magnitude M(f) in the range [0, fmax].

    Parameters
    ----------
    f:
        Frequency vector.
    M:
        Mean magnitude spectrum.
    n_modes:
        Number of peaks to return.
    fmax:
        Only consider peaks below this frequency.
    prominence_rel:
        Minimum prominence relative to max(M) in the considered band.

    Returns
    -------
    indices:
        Sorted indices into f/M for the selected peaks.
    """
    mask = f <= fmax
    if not np.any(mask):
        return np.array([], dtype=int)

    prom = prominence_rel * float(np.max(M[mask]))
    peaks, _ = sig.find_peaks(M[mask], prominence=prom)
    if peaks.size == 0:
        return np.array([], dtype=int)

    full_idx = np.flatnonzero(mask)[peaks]

    # Choose strongest peaks (by magnitude), keep them sorted by frequency.
    top = full_idx[np.argsort(M[full_idx])[::-1]][:n_modes]
    return np.sort(top)


def participation_vector_windowed(
    frfs: list[np.ndarray],
    f: np.ndarray,
    idx_center: int,
    band_hz: float,
    ref: int = 0,
) -> np.ndarray:
    """Compute a robust complex participation vector around a peak.

    Instead of taking a single FFT bin at the peak frequency, we average complex
    FRF values in a frequency window ±band_hz around the peak. This reduces
    sensitivity to noise and frequency-grid effects.

    Parameters
    ----------
    frfs:
        List of complex FRFs (one per excitation point).
    f:
        Frequency vector.
    idx_center:
        Peak index in f.
    band_hz:
        Half band width (Hz) for averaging.
    ref:
        Reference FRF index for phase alignment.

    Returns
    -------
    v:
        Complex participation vector (len(frfs),) normalized to max(|v|)=1.
    """
    f0 = float(f[idx_center])
    idx_window = np.where((f >= f0 - band_hz) & (f <= f0 + band_hz))[0]
    if idx_window.size == 0:
        idx_window = np.array([idx_center], dtype=int)

    v = np.array([np.mean(H[idx_window]) for H in frfs], dtype=complex)

    # Align phase to reference entry so visualisation is consistent.
    if np.abs(v[ref]) > 0:
        v = v * np.exp(-1j * np.angle(v[ref]))

    # Normalise amplitude.
    m = np.max(np.abs(v))
    if m > 0:
        v = v / m

    return v
