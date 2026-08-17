# PROMPT 4

Please write a Python script that creates a polished, professional Word document (.docx) titled "Projectile_Motion_Report.docx" covering 2D Kinematics and Trajectory Analysis.

Requirements:
1. Install `python-docx` and `matplotlib` via pip if not already available.

2. Generate Trajectory Visualization Plot (`matplotlib`):
   - Calculate trajectory points for v0 = 25 m/s, theta = 45 degrees, g = 9.81 m/s^2.
   - Plot Height y (m) vs Horizontal Distance x (m).
   - Mark key points on the curve: Launch Point (0,0), Maximum Height (H_max), and Landing Point (R_max).
   - Apply a clean style: high DPI (300 DPI), grid lines, labeled axes, titled legend, and modern color palette (e.g., deep blue line, accent markers).
   - Save the chart temporarily as `trajectory_plot.png`.

3. Build Word Document (`python-docx`):
   - Title Header: "Physics Mechanics 101: 2D Projectile Motion Analysis" with a styled subtitle and author metadata line.
   - Section 1: Executive Summary & Overview (2 paragraphs introducing 1D vs 2D motion and independence of x/y axes).
   - Section 2: Governing Mathematical Model:
     * Bullet points showing formulas for x(t), y(t), v_x, v_y, Max Height, Total Range, and Time of Flight.
     * Highlight callout block for key assumptions (flat terrain, negligible air resistance, constant acceleration g).
   - Section 3: Summary Table:
     * A styled table with header row coloring and subtle borders.
     * Columns: Parameter / Quantity, Formula, Calculated Value, Units.
     * Include Initial Velocity (25 m/s), Launch Angle (45°), Max Height (~15.93 m), Total Range (~63.71 m), and Time of Flight (~3.60 s).
   - Section 4: Trajectory Plot & Visual Analysis:
     * Embed `trajectory_plot.png` centered at 6 inches width.
     * Add a formal image caption underneath the figure.
     * Brief analytical text discussing trajectory symmetry and parabolic curvature.
   - Section 5: Conclusion & Key Takeaways.

4. Execute the script to generate `Projectile_Motion_Report.docx`.
