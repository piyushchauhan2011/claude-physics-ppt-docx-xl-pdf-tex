"""Pure physics functions for 2D projectile motion with quadratic air drag.

No Streamlit/Plotly dependency here on purpose — everything in this module
is a plain function of its arguments, so it can be imported and unit-tested
(see tests/test_physics.py) independently of the dashboard UI.
"""

import numpy as np
from scipy.integrate import solve_ivp


def compute_drag_constant(rho, Cd, radius):
    """k = 0.5 * rho * Cd * pi * r^2, the quadratic-drag proportionality constant."""
    return 0.5 * rho * Cd * np.pi * radius ** 2


def drag_derivatives(t, state, k, m, g):
    """ODE right-hand side for [x, y, vx, vy] under gravity + quadratic drag."""
    _x, _y, vx, vy = state
    v = np.hypot(vx, vy)
    ax = -(k / m) * v * vx
    ay = -g - (k / m) * v * vy
    return [vx, vy, ax, ay]


def _ground_event(t, state, k, m, g):
    return state[1]


_ground_event.terminal = True
_ground_event.direction = -1  # only a downward crossing counts as landing


def calculate_vacuum_analytical(v0, theta_deg, y0, g, n_samples=400):
    """Exact closed-form vacuum (no-drag) trajectory and flight metrics.

    Returns a dict with sampled arrays (t, x, y, vx, vy, v) plus scalar
    metrics: T (time of flight), R (range), H (max height), t_peak (time
    to reach max height), vx0, vy0.
    """
    theta = np.radians(theta_deg)
    vx0 = v0 * np.cos(theta)
    vy0 = v0 * np.sin(theta)

    # y0 + vy0*t - 0.5*g*t^2 = 0, positive root
    T = (vy0 + np.sqrt(max(vy0 ** 2 + 2 * g * y0, 0.0))) / g

    t = np.linspace(0, T, n_samples)
    x = vx0 * t
    y = np.clip(y0 + vy0 * t - 0.5 * g * t ** 2, 0, None)
    vx = np.full_like(t, vx0)
    vy = vy0 - g * t
    v = np.hypot(vx, vy)

    R = float(vx0 * T)
    H = float(y0 + (vy0 ** 2) / (2 * g)) if vy0 > 0 else float(y0)
    t_peak = float(vy0 / g) if vy0 > 0 else 0.0

    return {
        "t": t, "x": x, "y": y, "vx": vx, "vy": vy, "v": v,
        "T": float(T), "R": R, "H": H, "t_peak": t_peak,
        "vx0": float(vx0), "vy0": float(vy0),
    }


def solve_trajectory(v0, theta_deg, y0, m, radius, Cd, rho, g, n_samples=400):
    """Numerically integrate the drag trajectory to ground impact.

    Uses scipy.integrate.solve_ivp with a terminal y=0 event. Unlike
    range/height, flight *time* under quadratic drag is not guaranteed to
    be shorter than the vacuum case (a light/draggy object can fall slower
    than free-fall once it nears terminal velocity on the way down), so the
    integration span is grown and retried until the ground event actually
    fires, rather than trusting the vacuum flight time as an upper bound.

    Returns a dict with sampled arrays (t, x, y, vx, vy, v) plus scalar
    metrics: T, R, H, t_peak, impact_speed, impact_angle, k, landed, vx0, vy0.
    """
    theta = np.radians(theta_deg)
    vx0 = v0 * np.cos(theta)
    vy0 = v0 * np.sin(theta)
    k = compute_drag_constant(rho, Cd, radius)

    t_ideal = calculate_vacuum_analytical(v0, theta_deg, y0, g, n_samples=2)["T"]

    span_mult = 4.0
    base_guess = max(t_ideal, 0.5)
    sol = None
    for _ in range(6):
        t_max = base_guess * span_mult
        sol = solve_ivp(
            drag_derivatives,
            (0.0, t_max),
            [0.0, y0, vx0, vy0],
            args=(k, m, g),
            events=_ground_event,
            dense_output=True,
            max_step=t_max / 2000,
            rtol=1e-9,
            atol=1e-10,
        )
        if sol.status == 1 and len(sol.t_events[0]) > 0:
            break
        span_mult *= 3.0
        if t_max > 20000:
            break

    landed = sol.status == 1 and len(sol.t_events[0]) > 0
    t_land = sol.t_events[0][0] if landed else sol.t[-1]
    land_state = sol.y_events[0][0] if landed else sol.y[:, -1]

    t = np.linspace(0, t_land, n_samples)
    x, y, vx, vy = sol.sol(t)
    y = np.clip(y, 0, None)
    v = np.hypot(vx, vy)

    R = float(land_state[0])
    H = float(np.max(y))
    t_peak = float(t[int(np.argmax(y))])

    impact_vx, impact_vy = float(land_state[2]), float(land_state[3])
    impact_speed = float(np.hypot(impact_vx, impact_vy))
    impact_angle = float(np.degrees(np.arctan2(-impact_vy, impact_vx)))

    return {
        "t": t, "x": x, "y": y, "vx": vx, "vy": vy, "v": v,
        "T": float(t_land), "R": R, "H": H, "t_peak": t_peak,
        "impact_speed": impact_speed, "impact_angle": impact_angle,
        "k": float(k), "landed": landed,
        "vx0": float(vx0), "vy0": float(vy0),
    }
