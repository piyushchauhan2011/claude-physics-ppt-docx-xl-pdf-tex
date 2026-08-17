# PROMPT 6

Please build a self-contained, single-file interactive web application (`index.html`) that simulates 2D Projectile Motion with quadratic air resistance using HTML5 Canvas and vanilla JavaScript.

Requirements:
1. Tech Stack & Output:
   - Generate a single `index.html` containing HTML, modern CSS, and vanilla JS (no external library dependencies).
   - Canvas-based rendering running smooth animation loops via `requestAnimationFrame`.

2. Physics Engine (Numerical Integration):
   - Model quadratic drag force ($F_d = \frac{1}{2} \rho C_d A v^2$) using Euler integration:
     * $a_x = -\frac{k}{m} \cdot v \cdot v_x$
     * $a_y = -g - \frac{k}{m} \cdot v \cdot v_y$
     * where $k = \frac{1}{2} \cdot \rho \cdot C_d \cdot \pi r^2$
   - Parallel Reference Trail: Draw an ideal vacuum trajectory (dashed line) simultaneously so the user can visually compare drag vs. non-drag motion.

3. Interactive Controls (Real-Time Sliders):
   - Launch Velocity $v_0$ (5 – 100 m/s)
   - Launch Angle $\theta$ (0° – 90°)
   - Mass $m$ (0.05 – 10 kg)
   - Radius $r$ (0.01 – 0.5 m)
   - Drag Coefficient $C_d$ (0.0 – 1.0)
   - Air Density $\rho$ (0.0 – 2.0 kg/m³, 0 = vacuum)
   - Acceleration due to Gravity $g$ (1.0 – 25.0 m/s²)
   - Simulation Speed multiplier (0.5x, 1x, 2x, 5x)
   - Action Buttons: Launch, Pause/Resume, Reset, Clear Trajectories

4. UI & Visual Dashboard:
   - Modern dark-theme UI with a responsive layout (control sidebar + prominent canvas view).
   - Real-time telemetry overlay: Elapsed Time ($t$), Position ($x, y$), Speed ($v$), Max Height ($H_{\text{max}}$), and Horizontal Range ($R$).
   - Toggle options for Velocity Vector Arrows ($v_x, v_y, v_{\text{total}}$) and Grid Overlay.
   - Dynamic Canvas Scaling: Auto-fit scale and grid lines based on max height and range so trajectories never go off-screen.

5. Final Step:
   - Write the file to `index.html` and run `open index.html` to launch it directly in the default macOS web browser.
