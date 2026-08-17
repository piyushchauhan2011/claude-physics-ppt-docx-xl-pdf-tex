# PROMPT 2

Please create a Python script that generates a clean, fully functional Excel spreadsheet (.xlsx) for 2D Projectile Motion with an embedded trajectory chart.

Requirements:
1. Use `openpyxl` to build `Projectile_Motion.xlsx`. Install `openpyxl` via pip if needed.
2. Section 1 - Input Parameters (with clear formatting/cell fills):
   - Initial Velocity v0 (m/s): 25
   - Launch Angle theta (degrees): 45
   - Acceleration due to Gravity g (m/s^2): 9.81
   - Time Step dt (s): 0.1
3. Section 2 - Analytical Summary (calculated via Excel formulas):
   - Initial Horizontal Velocity Vx = v0 * COS(RADIANS(theta))
   - Initial Vertical Velocity Vy = v0 * SIN(RADIANS(theta))
   - Total Time of Flight t_total = 2 * Vy / g
   - Maximum Height H_max = Vy^2 / (2 * g)
   - Total Range R_max = v0^2 * SIN(RADIANS(2 * theta)) / g
4. Section 3 - Trajectory Data Table:
   - Columns: Time t (s), Distance x (m), Height y (m), Vx (m/s), Vy (m/s).
   - Generate rows from t = 0 up to t_total in steps of dt using dynamic cell references (e.g., =B$3*COS(RADIANS(B$4))*A12).
   - For height y(t), use `=MAX(0, (v0*SIN(RADIANS(theta))*t) - (0.5*g*t^2))` so values stop at ground level.
5. Section 4 - Trajectory Chart:
   - Add a Scatter Chart (`openpyxl.chart.ScatterChart`) with smooth lines.
   - Set X-axis to Distance x (m) and Y-axis to Height y (m).
   - Title: "Projectile Trajectory (Height vs Distance)".
   - Enable gridlines and legend.
6. Execute the script to generate `Projectile_Motion.xlsx`.
