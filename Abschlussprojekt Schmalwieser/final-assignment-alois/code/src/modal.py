from __future__ import annotations
import numpy as np
import scipy.signal as sig

def pick_modes(f: np.ndarray, M: np.ndarray, n_modes: int = 5, fmax: float = 60.0, prominence_rel: float = 0.05):
    """Simple peak picking on a magnitude spectrum.

    Returns peak indices in original arrays.
    """
    mask = f <= fmax
    if not np.any(mask):
        return np.array([], dtype=int)

    prom = prominence_rel * float(np.max(M[mask]))
    peaks, _ = sig.find_peaks(M[mask], prominence=prom)
    if peaks.size == 0:
        return np.array([], dtype=int)

    # Map to full indices
    full_idx = np.flatnonzero(mask)[peaks]

    # Choose top n by magnitude, then sort by frequency
    top = full_idx[np.argsort(M[full_idx])[::-1]][:n_modes]
    return np.sort(top)

def participation_vector_at(frfs: list[np.ndarray], idx: int, ref: int = 0) -> np.ndarray:
    """Vector of complex FRF values across excitations at one frequency bin.

    NOTE: With your data (one output point), this represents how strongly each
    excitation point drives the measured response at that frequency.
    It is NOT a spatial mode shape of the building response.
    """
    v = np.array([H[idx] for H in frfs], dtype=complex)

    # Phase reference: rotate so ref element has phase 0
    if np.abs(v[ref]) > 0:
        v = v * np.exp(-1j * np.angle(v[ref]))

    # Normalize max abs to 1
    m = np.max(np.abs(v))
    if m > 0:
        v = v / m
    return v
