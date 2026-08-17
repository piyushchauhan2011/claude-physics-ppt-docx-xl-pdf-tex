# PROMPT 10

Please create a robust unit testing suite using PyTest to verify the physics calculations, numerical integration, and edge cases for the projectile motion engine.

Requirements:
1. Physics Module Refactoring (if needed):
   - Ensure core physics logic in `app.py` is isolated into pure, testable functions (or create a `physics.py` module imported by `app.py`):
     * `compute_drag_constant(rho, Cd, radius)`
     * `drag_derivatives(t, state, k, m, g)`
     * `solve_trajectory(v0, theta_deg, y0, m, radius, Cd, rho, g)`
     * `calculate_vacuum_analytical(v0, theta_deg, y0, g)`

2. PyTest Test Suite (`tests/test_physics.py`):
   - Test 1: Vacuum Analytical Comparison (`test_vacuum_limit`):
     * Set `rho = 0` (or `Cd = 0`).
     * Compare numerical solver outputs against closed-form equations ($R = \frac{v_0^2 \sin 2\theta}{g}$, $H = \frac{(v_0 \sin\theta)^2}{2g}$, $T = \frac{2v_0 \sin\theta}{g}$).
     * Assert equality within `pytest.approx` (tolerance: rtol=1e-3).
   - Test 2: Drag Degradation Invariant (`test_drag_degradation`):
     * Assert $R_{\text{drag}} < R_{\text{vacuum}}$ and $H_{\text{drag}} < H_{\text{vacuum}}$ for non-zero drag.
     * Assert $v_x(t)$ monotonically decreases over time due to drag.
   - Test 3: Mechanical Energy Conservation & Dissipation (`test_energy_conservation`):
     * In vacuum: Assert Total Energy ($E_k + E_p$) remains constant within 0.5% tolerance across all time steps.
     * With drag: Assert Total Energy strictly decreases over time ($\frac{dE}{dt} \le 0$).
   - Test 4: Trajectory Asymmetry (`test_trajectory_asymmetry`):
     * In vacuum: Peak height occurs at exactly $t = T / 2$.
     * With drag: Assert time to peak height occurs *earlier* than the descent time ($t_{\text{peak}} < T_{\text{drag}} / 2$).
   - Test 5: Edge Cases (`test_edge_cases`):
     * Vertical Launch ($\theta = 90^\circ$): Range $x_{\text{final}} \approx 0$.
     * Horizontal Launch ($\theta = 0^\circ$ from height $y_0 = 10\text{ m}$): Verify landing time matches $\sqrt{2 y_0 / g}$.
     * High Mass vs. Low Mass: Higher mass projectile travels farther under identical drag parameters.

3. Environment & CI Updates:
   - Add `pytest` and `pytest-cov` to `requirements.txt`.
   - Update `.github/workflows/ci.yml` to run `pytest -v` in the `lint-and-check` job prior to Docker container build.

4. Execution:
   - Run `pytest -v` in the terminal to execute all tests and ensure 100% test pass rate.
