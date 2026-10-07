"""Generate the motorcycle ride used in the data processing deck.

The file data/motorcycle_ride.csv is synthetic. It imitates a data logger on a
road motorcycle that records at 100 Hz during a ride of about ten minutes on a
country road: a village, a junction, fast straights, a section of bends, a
traffic light and a stop at the end. The ride starts and ends at standstill.

Synthetic data has one advantage over a real log: we know exactly what is
wrong with it, because we put it there. A real log has the same kinds of
problems, but nobody hands you the list.

Usage:

    python tools/make-motorcycle-ride.py

The random generator is seeded, so every run writes the same file.

Columns
-------

timestamp        s      time since the logger started
speed_kmh        km/h   wheel speed sensor, reads 0 below 3 km/h
rpm              1/min  engine speed
gear             -      0 is neutral
throttle_pct     %      throttle opening
brake_front_bar  bar    front brake line pressure
brake_rear_bar   bar    rear brake line pressure
lean_deg         deg    lean angle from the IMU, positive is to the right
accel_x          m/s^2  longitudinal acceleration from the IMU
coolant_c        degC   coolant temperature, the sensor updates once a second
ride_mode        -      riding mode selected on the dashboard

What is wrong with the data (the answer key for the lecturer)
-------------------------------------------------------------

Timing
    The logger clock jitters, the step between two samples varies by about
    0.2 ms around the nominal 10 ms.
    Six short dropouts of a few samples each, and one stall of 1.25 s while
    the logger writes to its memory card.

Missing values
    coolant_c has three stretches without a value, between 1 and 3 seconds.
    lean_deg has four short stretches, the IMU message was lost.
    throttle_pct has two short stretches.

Implausible values
    coolant_c reads -40 for the first seconds. That is the value the sensor
    sends before it is ready, not a temperature.
    brake_front_bar jumps to 409.5 in a few samples. That is the top of the
    12 bit converter, a loose connector, not a pressure.
    speed_kmh reads 255.0 in three single samples. That is an error frame
    from the bus, the largest value one byte can hold.

Real events that look like faults
    One emergency stop on a straight, with a deceleration close to 1 g. It is
    an outlier and it is the most interesting part of the ride.
    The bends: lean angles of 25 to 35 degrees are rare compared to riding
    upright, so an outlier test on lean_deg flags every one of them.

Calibration and drift
    accel_x carries an offset of about 0.25 m/s^2 that grows slowly while the
    sensor warms up. The first 20 seconds are standstill, which is the honest
    baseline. Integrated without correction, the velocity runs away.
"""

from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "motorcycle_ride.csv"

RATE = 100.0  # Hz
DT = 1.0 / RATE
G = 9.81

rng = np.random.default_rng(20261008)

# --------------------------------------------------------------------------
# The route
#
# Each segment: (kind, length in m or hold time in s, target speed in km/h,
# curve radius in m, positive is a right hand bend, 0 is straight, ride mode)
# "stop" brings the bike to standstill and holds it for the given seconds.
# "surprise" is an obstacle the rider only sees 55 m ahead.
# --------------------------------------------------------------------------

ROUTE = [
    ("road", 350, 50, 0, "road"),
    ("road", 250, 50, 0, "road"),
    ("stop", 4.0, 0, 0, "road"),  # junction
    ("road", 700, 100, 0, "road"),
    ("road", 160, 85, -120, "road"),
    ("road", 450, 100, 0, "road"),
    ("road", 120, 65, 60, "road"),
    ("road", 420, 100, 0, "road"),
    ("surprise", 0, 15, 0, "road"),  # emergency stop, a deer on the road
    ("road", 500, 100, 0, "road"),
    ("road", 90, 50, -40, "sport"),
    ("road", 60, 70, 0, "sport"),
    ("road", 95, 48, 35, "sport"),
    ("road", 70, 70, 0, "sport"),
    ("road", 110, 55, -45, "sport"),
    ("road", 80, 75, 0, "sport"),
    ("road", 100, 52, 38, "sport"),
    ("road", 1100, 110, 0, "sport"),
    ("road", 600, 50, 0, "road"),  # village
    ("stop", 7.0, 0, 0, "road"),  # traffic light
    ("road", 350, 50, 0, "road"),
    ("road", 40, 28, 22, "road"),
    ("road", 1500, 100, 0, "road"),
    ("road", 220, 95, -150, "road"),
    ("road", 700, 100, 0, "road"),
    ("road", 130, 72, 75, "road"),
    ("road", 1200, 100, 0, "road"),
    ("road", 450, 50, 0, "road"),
    ("road", 35, 25, -20, "road"),
    ("road", 220, 30, 0, "road"),
    ("stop", 0.0, 0, 0, "road"),  # arrival
]

STANDSTILL_START = 20.0  # s, engine idling, rider on the bike
STANDSTILL_END = 12.0  # s


def build_track():
    """Turn the route into position markers along the road."""
    marks = []  # (start position m, end position m, kind, v_target m/s, radius, mode, hold)
    pos = 0.0
    for kind, length, v_kmh, radius, mode in ROUTE:
        v = v_kmh / 3.6
        if kind == "road":
            marks.append((pos, pos + length, kind, v, radius, mode, 0.0))
            pos += length
        else:
            marks.append((pos, pos, kind, v, 0, mode, length))
    return marks, pos


def allowed_speed(pos, marks, a_plan=4.0, surprise_seen=55.0):
    """The speed the rider accepts here, looking ahead to slower sections."""
    v_allow = np.inf
    for start, end, kind, v, _, _, _ in marks:
        if kind == "stop" or end < pos:  # stops are handled in simulate()
            continue
        if kind == "surprise":
            dist = start - pos
            if dist > surprise_seen or dist < -1.0:
                continue
            v_allow = min(v_allow, np.sqrt(v**2 + 2 * 9.0 * max(dist, 0.0)))
            continue
        dist = max(start - pos, 0.0)
        v_allow = min(v_allow, np.sqrt(v**2 + 2 * a_plan * dist))
    return v_allow


def segment_at(pos, marks):
    for m in marks:
        if m[2] == "road" and m[0] <= pos < m[1]:
            return m
    return marks[-1]


def simulate():
    marks, total = build_track()
    stops = [m for m in marks if m[2] == "stop"]
    surprises = [m for m in marks if m[2] == "surprise"]

    t, pos, v, a = 0.0, 0.0, 0.0, 0.0
    lean = 0.0
    hold_until = STANDSTILL_START
    next_stop = 0
    surprise_done = False
    rows = []

    while True:
        seg = segment_at(pos, marks)
        mode = seg[5]

        if t < hold_until:
            a_cmd = 0.0
            v = 0.0
        else:
            v_allow = allowed_speed(pos, marks)
            v_target = min(seg[3], v_allow)

            # stops: aim for zero exactly at the stop line
            if next_stop < len(stops):
                dist = stops[next_stop][0] - pos
                v_stop = np.sqrt(2 * 3.5 * max(dist, 0.0))
                v_target = min(v_target, v_stop)
                if dist < 0.5 and v < 0.4:
                    v, a = 0.0, 0.0
                    hold = stops[next_stop][6]
                    next_stop += 1
                    if next_stop == len(stops):  # arrived, idle and end the log
                        end_t = t + STANDSTILL_END
                        while t < end_t:
                            rows.append((t, 0.0, 0.0, 0.0, mode))
                            t += DT
                        break
                    hold_until = t + hold
                    continue

            # the emergency stop: the rider brakes as hard as the tyre allows
            hard = False
            for s in surprises:
                if not surprise_done and 0 < s[0] - pos < 55.0:
                    hard = True
                if pos > s[0] + 5:
                    surprise_done = True

            a_max = 4.0 - 0.07 * v
            if hard and v > surprises[0][3]:
                a_cmd = -9.3  # full braking until the bike is down to walking pace
            else:
                a_cmd = np.clip(1.2 * (v_target - v), -6.5, a_max)

        # the rider and the tyre do not change the deceleration instantly
        tau = 0.12 if a_cmd < -7 else 0.35
        a += (a_cmd - a) * DT / tau
        if t < hold_until:
            a = 0.0
        v = max(v + a * DT, 0.0)
        if v == 0.0 and a < 0:
            a = 0.0
        pos += v * DT

        radius = seg[4]
        lean_target = 0.0
        if radius != 0 and v > 1:
            lean_target = np.degrees(np.arctan(v**2 / (G * abs(radius)))) * np.sign(radius)
        lean += (lean_target - lean) * DT / 0.45

        rows.append((t, v, a, lean, mode))
        t += DT

    return pd.DataFrame(rows, columns=["t", "v", "a", "lean", "mode"])


def add_channels(sim):
    n = len(sim)
    t = np.arange(n) * DT
    v = sim["v"].to_numpy()
    a = sim["a"].to_numpy()
    v_kmh = v * 3.6

    # gear from speed, with hysteresis so it does not chatter
    up = [0, 1, 20, 35, 50, 65, 80]  # km/h to shift into gear i
    gear = np.zeros(n, dtype=int)
    g = 0
    for i in range(n):
        if v_kmh[i] < 0.5:
            g = 1 if (i + 1 < n and v_kmh[i + 1] > v_kmh[i]) else (0 if a[i] == 0 else g)
        else:
            g = max(g, 1)
            while g < 6 and v_kmh[i] > up[g + 1]:
                g += 1
            while g > 1 and v_kmh[i] < up[g] - 6:
                g -= 1
        gear[i] = g

    ratio = np.array([0, 160, 115, 90, 75, 64, 57])  # rpm per km/h
    rpm = ratio[gear] * v_kmh
    rpm = np.where(gear == 0, 1250, rpm)
    rpm = np.where((gear == 1) & (v_kmh < 12) & (a > 0.2), np.maximum(rpm, 2000), rpm)
    rpm = np.maximum(rpm, 1250) + rng.normal(0, 15, n)
    rpm = np.round(rpm).astype(int)

    drag = 0.15 + 0.0006 * v**2
    throttle = np.clip(100 * (a + drag) / 4.2, 0, 100)
    throttle = np.where((a < -0.3) | (v < 0.1) & (a <= 0), 0.0, throttle)
    throttle = pd.Series(throttle).rolling(15, min_periods=1).mean().to_numpy()
    throttle = np.round(throttle + np.abs(rng.normal(0, 0.2, n)), 1)

    brake_f = np.clip((-a - 0.5) * 1.6, 0, None)
    brake_f = np.where(v == 0, 3.0, brake_f)  # rider holds the brake at standstill
    brake_f = np.where(t < STANDSTILL_START - 2, 0.0, brake_f)
    brake_f = np.round(np.clip(brake_f + rng.normal(0, 0.05, n), 0, None), 1)
    brake_r = np.round(np.clip(0.3 * brake_f + rng.normal(0, 0.05, n), 0, None), 1)

    lean = np.round(sim["lean"].to_numpy() + rng.normal(0, 0.3, n), 1)

    # the IMU offset, growing slowly while the sensor warms up
    offset = 0.25 + 0.04 * (1 - np.exp(-t / 300.0))
    noise = rng.normal(0, 1, n) * (0.06 + 0.00004 * rpm)
    accel_x = np.round(a + offset + noise, 3)

    # coolant: warms up, the fan holds it near 90, updates once per second
    coolant = 90 - (90 - 47) * np.exp(-t / 260.0)
    coolant_held = np.round(coolant[np.searchsorted(t, np.floor(t))])

    speed = np.round(v_kmh, 1)
    speed = np.where(speed < 3.0, 0.0, speed)

    return pd.DataFrame(
        {
            "timestamp": t,
            "speed_kmh": speed,
            "rpm": rpm,
            "gear": gear,
            "throttle_pct": throttle,
            "brake_front_bar": brake_f,
            "brake_rear_bar": brake_r,
            "lean_deg": lean,
            "accel_x": accel_x,
            "coolant_c": coolant_held,
            "ride_mode": sim["mode"].to_numpy(),
        }
    )


USED = []  # indices that already carry a defect, so two defects never overlap


def pick(count, low, high):
    """Random positions for a defect, well away from every other defect."""
    chosen = []
    while len(chosen) < count:
        i = int(rng.integers(low, high))
        if all(abs(i - j) > 1500 for j in USED):
            chosen.append(i)
            USED.append(i)
    return sorted(chosen)


def add_defects(df):
    n = len(df)
    start = int(STANDSTILL_START * RATE) + 500
    end = n - int(STANDSTILL_END * RATE) - 500

    # coolant sensor not ready yet
    df.loc[: int(2.6 * RATE), "coolant_c"] = -40.0

    # missing values
    for i in pick(3, start, end):
        df.loc[i : i + int(rng.integers(100, 300)), "coolant_c"] = np.nan
    # two of the IMU dropouts fall into bends, where interpolating matters
    cornering = df.index[df["lean_deg"].abs() > 15].to_numpy()
    in_bends = [int(i) for i in rng.choice(cornering, 2, replace=False)]
    USED.extend(in_bends)
    lean_gaps = in_bends + pick(2, start, end)
    for i in lean_gaps:
        df.loc[i : i + int(rng.integers(6, 40)), "lean_deg"] = np.nan
    for i in pick(2, start, end):
        df.loc[i : i + int(rng.integers(10, 30)), "throttle_pct"] = np.nan

    # implausible values
    for i in pick(2, start, end):
        df.loc[i : i + int(rng.integers(1, 3)), "brake_front_bar"] = 409.5
    for i in pick(3, start, end):
        df.loc[i, "speed_kmh"] = 255.0

    # clock jitter
    jitter = rng.normal(0, 150e-6, n)
    jitter[0] = 0.0  # the log starts at exactly zero
    df["timestamp"] = np.round(df["timestamp"] + jitter, 6)

    # dropouts: six short ones, and one stall on a fast straight
    drop = []
    for i in pick(6, start, end):
        drop.extend(range(i, i + int(rng.integers(2, 9))))
    straight = df.index[(df["speed_kmh"] > 95) & (df["speed_kmh"] < 105) & (df["lean_deg"].abs() < 2)]
    i = int(straight[len(straight) // 3])
    drop.extend(range(i, i + int(1.25 * RATE)))
    df = df.drop(index=sorted(set(drop))).reset_index(drop=True)
    return df


def main():
    sim = simulate()
    df = add_channels(sim)
    df = add_defects(df)
    df.to_csv(OUT, index=False)
    duration = df["timestamp"].iloc[-1]
    print(f"wrote {OUT.relative_to(ROOT)}: {len(df)} rows, {duration / 60:.1f} min, "
          f"{OUT.stat().st_size / 1e6:.1f} MB")


if __name__ == "__main__":
    main()
