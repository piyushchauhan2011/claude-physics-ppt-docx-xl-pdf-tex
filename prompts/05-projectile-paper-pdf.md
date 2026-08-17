# PROMPT 5

Please write a Python script that generates a publication-ready, academic-style PDF report titled "projectile_motion_paper.pdf" on 2D Kinematics and Trajectory Analysis using LaTeX.

Requirements:
1. Python Plot Generation:
   - Use `matplotlib` and `numpy` to build two high-resolution (300 DPI) publication-grade figures:
     a) `fig1_trajectories.png`: Plot trajectories for v0 = 25 m/s across launch angles theta = 15°, 30°, 45°, 60°, and 75°. Include markers for peak heights.
     b) `fig2_range_angle.png`: Plot Horizontal Range R vs. Launch Angle theta (0° to 90°), visually highlighting the maximum range peak at theta = 45°.
   - Use publication styling: math-formatted labels (LaTeX formatting in labels), clear grid lines, high-contrast palette, and professional legends.

2. LaTeX Source Generation (`projectile_motion_paper.tex`):
   - Document Class: `article` (11pt, single or two-column format).
   - Essential Packages: `geometry` (margins 0.75 in), `amsmath`, `amssymb`, `graphicx`, `booktabs`, `caption`, `hyperref`, `microtype`.
   - Content Layout:
     * Header: Title ("Analytical and Numerical Investigation of Two-Dimensional Projectile Motion"), Author, Date, and Abstract.
     * Section 1: Introduction & Kinematic Foundations (Vector decomposition into independent x and y components).
     * Section 2: Derivation of Governing Equations (Numbered LaTeX equations using `align` or `equation` environments for x(t), y(t), Time of Flight T, Max Height H, and Range R).
     * Section 3: Trajectory & Parametric Analysis (Include Figure 1 and Figure 2 with proper LaTeX captions and cross-references `\ref{fig:trajectories}`).
     * Section 4: Quantitative Summary Table (A clean LaTeX `booktabs` table listing launch angle, time of flight, max height, and range for theta = 15°, 30°, 45°, 60°, 75°).
     * Section 5: Conclusion & Discussion.

3. PDF Compilation:
   - Execute `pdflatex` (or `xelatex`) twice via Python `subprocess` to correctly resolve equation labels, figure references, and page numbering.
   - Clean up temporary build artifacts (`.aux`, `.log`, `.out`).
   - Output final file: `projectile_motion_paper.pdf`.

4. Execute the Python script to create the figures, write the LaTeX file, and compile `projectile_motion_paper.pdf`.
