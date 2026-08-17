# PROMPT 3

Please write a Python script using `openpyxl` that generates an Excel workbook (`Projectile_Motion_With_Drag.xlsx`) comparing ideal vacuum motion against motion with quadratic air resistance.

Requirements:
1. Input Parameters Section:
   - Initial Velocity v0 (m/s): 25
   - Launch Angle theta (degrees): 45
   - Acceleration due to Gravity g (m/s^2): 9.81
   - Time Step dt (s): 0.02
   - Air Density rho (kg/m^3): 1.225
   - Drag Coefficient Cd: 0.47 (sphere)
   - Projectile Radius r (m): 0.05
   - Projectile Mass m (kg): 0.25
   - Cross-sectional Area A = PI() * r^2
   - Drag Constant k = 0.5 * rho * Cd * A

2. Numerical Integration Table (Euler's Method):
   - Columns: Time t (s), x_drag (m), y_drag (m), vx (m/s), vy (m/s), v_total (m/s), ax (m/s^2), ay (m/s^2), x_ideal (m), y_ideal (m)
   - Row 0 (t = 0):
     * x_drag = 0, y_drag = 0
     * vx = v0 * COS(RADIANS(theta)), vy = v0 * SIN(RADIANS(theta))
     * v_total = SQRT(vx^2 + vy^2)
     * ax = -(k / m) * vx * v_total
     * ay = -g - (k / m) * vy * v_total
     * x_ideal = 0, y_ideal = 0
   - Subsequent rows (t = t_prev + dt):
     * vx = vx_prev + ax_prev * dt
     * vy = vy_prev + ay_prev * dt
     * x_drag = x_drag_prev + vx_prev * dt
     * y_drag = MAX(0, y_drag_prev + vy_prev * dt)
     * v_total = SQRT(vx^2 + vy^2)
     * ax = IF(y_drag > 0, -(k / m) * vx * v_total, 0)
     * ay = IF(y_drag > 0, -g - (k / m) * vy * v_total, 0)
     * x_ideal = v0 * COS(RADIANS(theta)) * t
     * y_ideal = MAX(0, (v0 * SIN(RADIANS(theta)) * t) - (0.5 * g * t^2))
   - Continue step-by-step until the projectile returns to ground level.

3. Trajectory Comparison Chart:
   - Create a Scatter Chart with smooth lines (`openpyxl.chart.ScatterChart`).
   - Plot Series 1: Trajectory with Drag (X = x_drag, Y = y_drag).
   - Plot Series 2: Ideal Trajectory (X = x_ideal, Y = y_ideal).
   - X-Axis Title: "Horizontal Distance (m)"
   - Y-Axis Title: "Height (m)"
   - Chart Title: "Projectile Motion: Ideal Vacuum vs. Air Resistance"
   - Position legend at the bottom.

4. Execute the script to generate `Projectile_Motion_With_Drag.xlsx`.
