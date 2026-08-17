# PROMPT 7

Please write a Python script `app.py` that builds an interactive, browser-based Streamlit application for analyzing 2D Projectile Motion with quadratic air resistance using Plotly for dynamic graph rendering.

Requirements:
1. Dependencies & Setup:
   - Ensure `streamlit`, `plotly`, `numpy`, and `scipy` are installed via pip if missing.
   - Execute `streamlit run app.py` upon script creation.

2. Physics Model:
   - Implement differential equations for quadratic air drag:
     dx/dt = vx
     dy/dt = vy
     dvx/dt = -(k / m) * sqrt(vx^2 + vy^2) * vx
     dvy/dt = -g - (k / m) * sqrt(vx^2 + vy^2) * vy
     where k = 0.5 * rho * Cd * (pi * r^2)
   - Use `scipy.integrate.solve_ivp` with an event function `y(t) = 0` (stopping at ground level) for high-accuracy numerical integration.
   - Compute the ideal vacuum trajectory simultaneously for side-by-side comparison.

3. Streamlit Sidebar Controls:
   - Presets Dropdown: "Baseball", "Golf Ball", "Cannonball", "Table Tennis Ball" (auto-populates mass m, radius r, and Cd).
   - Launch Parameters: Initial Velocity v0 (m/s), Launch Angle theta (degrees), Launch Height y0 (m).
   - Projectile Specs: Mass m (kg), Radius r (m), Drag Coefficient Cd.
   - Environment Specs: Air Density rho (kg/m^3), Acceleration due to Gravity g (m/s^2).

4. Dashboard & KPI Metrics:
   - Display comparative metrics using `st.metric` in a top row (Ideal vs. Drag):
     * Total Range (m) and % loss due to drag
     * Maximum Height (m)
     * Flight Duration (s)
     * Impact Velocity & Angle

5. Interactive Plotly Visualizations (Tabbed Layout):
   - Tab 1 (Trajectory Curve): Scatter plot of Height y vs Range x. Plot both Ideal (dashed red) and Drag (solid blue) paths with interactive hover tooltips (time, velocity, position). Add visual markers for max height and landing impact.
   - Tab 2 (Kinematics over Time): Multi-line charts showing vx, vy, and total speed v vs time t.
   - Tab 3 (Energy Dissipation): Stacked area or line chart tracking Kinetic Energy, Potential Energy, and Total Energy lost to air resistance over time.

6. Execution:
   - Save the code to `app.py` and run `streamlit run app.py` in the terminal to launch the dashboard in the web browser.
