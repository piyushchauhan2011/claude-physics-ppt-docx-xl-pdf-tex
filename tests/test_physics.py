"""Unit tests for physics.py: closed-form vacuum trajectory, numerically
integrated quadratic-drag trajectory, and the physical invariants that
should hold between/within them."""

import math

import numpy as np
import pytest

from physics import (
    calculate_vacuum_analytical,
    compute_drag_constant,
    drag_derivatives,
    solve_trajectory,
)

# ---------------------------------------------------------------------------
# Shared defaults for tests that don't care about specific values
# ---------------------------------------------------------------------------
G = 9.81
V0 = 30.0
THETA = 40.0  # deliberately not 45 deg, so tests don't hide bugs behind symmetry
M = 0.5
RADIUS = 0.05
CD = 0.47
RHO = 1.2


# ---------------------------------------------------------------------------
# Test 1: vacuum analytical comparison
# ---------------------------------------------------------------------------
def test_vacuum_limit():
    theta_rad = math.radians(THETA)
    R_expected = V0 ** 2 * math.sin(2 * theta_rad) / G
    H_expected = (V0 * math.sin(theta_rad)) ** 2 / (2 * G)
    T_expected = 2 * V0 * math.sin(theta_rad) / G

    # closed-form analytical function
    ideal = calculate_vacuum_analytical(V0, THETA, y0=0.0, g=G)
    assert ideal["R"] == pytest.approx(R_expected, rel=1e-3)
    assert ideal["H"] == pytest.approx(H_expected, rel=1e-3)
    assert ideal["T"] == pytest.approx(T_expected, rel=1e-3)

    # numerical solver with rho=0 should match the same closed form
    drag_no_air = solve_trajectory(V0, THETA, 0.0, M, RADIUS, CD, rho=0.0, g=G)
    assert drag_no_air["R"] == pytest.approx(R_expected, rel=1e-3)
    assert drag_no_air["H"] == pytest.approx(H_expected, rel=1e-3)
    assert drag_no_air["T"] == pytest.approx(T_expected, rel=1e-3)


# ---------------------------------------------------------------------------
# Test 2: drag degradation invariant
# ---------------------------------------------------------------------------
def test_drag_degradation():
    ideal = calculate_vacuum_analytical(V0, THETA, y0=0.0, g=G)
    drag = solve_trajectory(V0, THETA, 0.0, M, RADIUS, CD, RHO, G)

    assert drag["R"] < ideal["R"]
    assert drag["H"] < ideal["H"]

    # vx(t) must monotonically decrease: drag always opposes horizontal
    # motion, so successive samples should never increase (tiny float
    # slack for the ODE solver's own step error).
    assert np.all(np.diff(drag["vx"]) <= 1e-9)
    assert drag["vx"][-1] < drag["vx"][0]


# ---------------------------------------------------------------------------
# Test 3: mechanical energy conservation & dissipation
# ---------------------------------------------------------------------------
def test_energy_conservation():
    # Vacuum: total mechanical energy should be (numerically) constant.
    vacuum = solve_trajectory(V0, THETA, 0.0, M, RADIUS, CD, rho=0.0, g=G)
    E_vacuum = 0.5 * M * vacuum["v"] ** 2 + M * G * vacuum["y"]
    rel_dev = np.abs(E_vacuum - E_vacuum[0]) / E_vacuum[0]
    assert np.max(rel_dev) < 0.005  # within 0.5%

    # With drag: total mechanical energy must strictly decrease (dE/dt <= 0).
    drag = solve_trajectory(V0, THETA, 0.0, M, RADIUS, CD, RHO, G)
    E_drag = 0.5 * M * drag["v"] ** 2 + M * G * drag["y"]
    assert np.all(np.diff(E_drag) <= 1e-6)
    assert E_drag[-1] < E_drag[0]


# ---------------------------------------------------------------------------
# Test 4: trajectory asymmetry
# ---------------------------------------------------------------------------
def test_trajectory_asymmetry():
    # Vacuum, ground-level launch: ascent and descent are symmetric in time.
    ideal = calculate_vacuum_analytical(V0, THETA, y0=0.0, g=G)
    assert ideal["t_peak"] == pytest.approx(ideal["T"] / 2, rel=1e-6)

    # With drag: drag shortens the (steeper-decelerated) ascent and
    # lengthens the (terminal-velocity-limited) descent, so the peak
    # occurs before the midpoint of the now-longer total flight time.
    drag = solve_trajectory(V0, THETA, 0.0, M, RADIUS, CD, RHO, G)
    assert drag["t_peak"] < drag["T"] / 2


# ---------------------------------------------------------------------------
# Test 5: edge cases
# ---------------------------------------------------------------------------
def test_edge_cases():
    # (a) Vertical launch: no horizontal velocity component -> range ~ 0
    # for the entire flight, not just at landing.
    vertical = solve_trajectory(V0, 90.0, 0.0, M, RADIUS, CD, RHO, G)
    assert vertical["R"] == pytest.approx(0.0, abs=1e-6)
    assert np.max(np.abs(vertical["x"])) < 1e-6

    # (b) Horizontal launch from height y0, in vacuum: axis independence
    # means landing time is exactly the free-fall time regardless of
    # horizontal speed.
    y0_test = 10.0
    expected_T = math.sqrt(2 * y0_test / G)

    horizontal_ideal = calculate_vacuum_analytical(20.0, 0.0, y0_test, G)
    assert horizontal_ideal["T"] == pytest.approx(expected_T, rel=1e-6)

    horizontal_drag = solve_trajectory(20.0, 0.0, y0_test, M, RADIUS, CD, rho=0.0, g=G)
    assert horizontal_drag["T"] == pytest.approx(expected_T, rel=1e-3)

    # (c) Higher mass -> smaller k/m ratio -> less relative drag -> farther range.
    low_mass = solve_trajectory(V0, THETA, 0.0, 0.05, RADIUS, CD, RHO, G)
    high_mass = solve_trajectory(V0, THETA, 0.0, 5.0, RADIUS, CD, RHO, G)
    assert high_mass["R"] > low_mass["R"]


# ---------------------------------------------------------------------------
# Bonus: direct unit coverage for the small pure helpers
# ---------------------------------------------------------------------------
def test_compute_drag_constant():
    k = compute_drag_constant(rho=1.225, Cd=0.47, radius=0.05)
    expected = 0.5 * 1.225 * 0.47 * math.pi * 0.05 ** 2
    assert k == pytest.approx(expected, rel=1e-9)
    assert compute_drag_constant(0.0, 0.47, 0.05) == 0.0


def test_solve_trajectory_retries_span_when_initial_guess_undershoots():
    # A very light, high-drag object dropped from a modest height approaches
    # terminal velocity almost immediately, so it falls far slower than
    # free-fall and its true flight time vastly exceeds the vacuum-based
    # initial time-span guess. This forces solve_trajectory's retry loop
    # (growing t_max and re-running solve_ivp) to actually execute more than
    # once before the ground event fires.
    result = solve_trajectory(0.0, 0.0, 5.0, 0.001, 1.0, 2.2, 1.2, G)
    assert result["landed"] is True
    assert result["T"] > 50.0  # vacuum free-fall from 5 m would be ~1 s


def test_drag_derivatives():
    # Falling straight down at 10 m/s with no drag (k=0): pure gravity.
    dxdt, dydt, dvxdt, dvydt = drag_derivatives(0.0, [0.0, 5.0, 0.0, -10.0], k=0.0, m=1.0, g=9.81)
    assert dxdt == 0.0
    assert dydt == -10.0
    assert dvxdt == 0.0
    assert dvydt == pytest.approx(-9.81)

    # With drag, horizontal deceleration opposes a positive vx.
    _, _, dvxdt_drag, _ = drag_derivatives(0.0, [0.0, 5.0, 10.0, 0.0], k=0.01, m=1.0, g=9.81)
    assert dvxdt_drag < 0
