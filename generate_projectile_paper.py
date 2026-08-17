#!/usr/bin/env python3
"""Generate 'projectile_motion_paper.pdf' — a publication-style LaTeX paper
on 2D projectile motion, with two matplotlib figures, compiled via pdflatex."""

import math
import os
import shutil
import subprocess
import sys

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

G = 9.81
V0 = 25.0

BUILD_DIR = "paper_build"
TEX_NAME = "projectile_motion_paper"
FIG1 = "fig1_trajectories.png"
FIG2 = "fig2_range_angle.png"

os.makedirs(BUILD_DIR, exist_ok=True)

# ---------------------------------------------------------------------------
# Publication plot styling
# ---------------------------------------------------------------------------
plt.rcParams.update({
    "font.family": "serif",
    "mathtext.fontset": "cm",
    "font.size": 11,
    "axes.linewidth": 0.9,
    "axes.edgecolor": "#1B222D",
    "axes.labelcolor": "#1B222D",
    "text.color": "#1B222D",
    "xtick.color": "#1B222D",
    "ytick.color": "#1B222D",
})

# ---------------------------------------------------------------------------
# Figure 1 — trajectories for several launch angles
# ---------------------------------------------------------------------------
angles_deg = [15, 30, 45, 60, 75]
palette = ["#E0473A", "#F2A63D", "#0B1F3A", "#2E8FC4", "#7A6FDB"]

fig, ax = plt.subplots(figsize=(7.2, 4.6), dpi=300)

for ang, color in zip(angles_deg, palette):
    th = math.radians(ang)
    vx0, vy0 = V0 * math.cos(th), V0 * math.sin(th)
    t_flight = 2 * vy0 / G
    t = np.linspace(0, t_flight, 400)
    x = vx0 * t
    y = vy0 * t - 0.5 * G * t ** 2
    y = np.clip(y, 0, None)
    ax.plot(x, y, color=color, linewidth=2.0, label=rf"$\theta = {ang}^\circ$")

    t_apex = vy0 / G
    h_max = vy0 ** 2 / (2 * G)
    ax.scatter([vx0 * t_apex], [h_max], s=32, color=color, edgecolor="white",
               linewidth=0.9, zorder=5)

ax.set_xlabel(r"Horizontal Distance, $x$ (m)")
ax.set_ylabel(r"Height, $y$ (m)")
ax.set_title(r"Projectile Trajectories for $v_0 = 25\ \mathrm{m/s}$ at Varying Launch Angles")
ax.grid(True, linestyle="--", linewidth=0.5, alpha=0.55)
ax.set_axisbelow(True)
ax.set_xlim(0, 66)
ax.set_ylim(0, 24)
for spine in ("top", "right"):
    ax.spines[spine].set_visible(False)
leg = ax.legend(loc="upper right", frameon=True, fontsize=9.5, title="Launch Angle",
                 title_fontsize=9.5, ncol=1)
leg.get_frame().set_edgecolor("#C7CFDB")
leg.get_frame().set_linewidth(0.7)

fig.tight_layout()
fig.savefig(os.path.join(BUILD_DIR, FIG1), dpi=300, facecolor="white")
plt.close(fig)

# ---------------------------------------------------------------------------
# Figure 2 — range vs. launch angle, 0-90 degrees
# ---------------------------------------------------------------------------
theta_deg = np.linspace(0, 90, 500)
theta_rad = np.radians(theta_deg)
R = V0 ** 2 * np.sin(2 * theta_rad) / G

fig2, ax2 = plt.subplots(figsize=(7.2, 4.3), dpi=300)
ax2.plot(theta_deg, R, color="#0B1F3A", linewidth=2.2)
ax2.fill_between(theta_deg, R, 0, color="#2EC4B6", alpha=0.12)

R_max = V0 ** 2 / G  # at theta = 45
ax2.scatter([45], [R_max], s=70, color="#E0473A", zorder=5, edgecolor="white", linewidth=1.2)
ax2.axvline(45, color="#8A93A3", linestyle="--", linewidth=0.9)
ax2.annotate(rf"$\theta = 45^\circ,\ R_{{\max}} = {R_max:.2f}\ \mathrm{{m}}$",
             xy=(45, R_max), xytext=(48, R_max - 6),
             fontsize=9.5, color="#1B222D", fontweight="bold")

ax2.set_xlabel(r"Launch Angle, $\theta$ (degrees)")
ax2.set_ylabel(r"Horizontal Range, $R$ (m)")
ax2.set_title(r"Horizontal Range as a Function of Launch Angle ($v_0 = 25\ \mathrm{m/s}$)")
ax2.grid(True, linestyle="--", linewidth=0.5, alpha=0.55)
ax2.set_axisbelow(True)
ax2.set_xlim(0, 90)
ax2.set_ylim(0, R_max * 1.15)
for spine in ("top", "right"):
    ax2.spines[spine].set_visible(False)

fig2.tight_layout()
fig2.savefig(os.path.join(BUILD_DIR, FIG2), dpi=300, facecolor="white")
plt.close(fig2)

print(f"Saved {FIG1} and {FIG2} to {BUILD_DIR}/")

# ---------------------------------------------------------------------------
# Quantitative summary table data (theta, T, H, R)
# ---------------------------------------------------------------------------
table_angles = [15, 30, 45, 60, 75]
table_rows = []
for ang in table_angles:
    th = math.radians(ang)
    vy0 = V0 * math.sin(th)
    T = 2 * vy0 / G
    H = vy0 ** 2 / (2 * G)
    R_val = V0 ** 2 * math.sin(2 * th) / G
    table_rows.append((ang, T, H, R_val))

table_tex_rows = "\n".join(
    rf"{ang}$^\circ$ & {T:.3f} & {H:.3f} & {R_val:.3f} \\"
    for ang, T, H, R_val in table_rows
)

# ---------------------------------------------------------------------------
# LaTeX source
# ---------------------------------------------------------------------------
tex_source = r"""
\documentclass[11pt]{article}

\usepackage[margin=0.75in]{geometry}
\usepackage{amsmath}
\usepackage{amssymb}
\usepackage{graphicx}
\usepackage{booktabs}
\usepackage{caption}
\usepackage{microtype}
\usepackage{xcolor}
\usepackage[colorlinks=true, linkcolor=blue!50!black, citecolor=blue!50!black, urlcolor=blue!50!black]{hyperref}

\title{\textbf{Analytical and Numerical Investigation of \\ Two-Dimensional Projectile Motion}}
\author{Physics Mechanics 101 Course Staff}
\date{\today}

\begin{document}

\maketitle

\begin{abstract}
\noindent
This paper presents an analytical and numerical investigation of two-dimensional projectile motion under
the idealized assumptions of constant gravitational acceleration and negligible air resistance. Beginning
from Newton's second law, we derive the governing kinematic equations for horizontal and vertical motion
and show that they decouple into two independent one-dimensional problems. Closed-form expressions for the
time of flight, maximum height, and horizontal range are obtained and evaluated numerically for a launch
speed of $v_0 = 25~\mathrm{m/s}$ across a range of launch angles. Trajectories and the range--angle
relationship are visualized, confirming the well-known result that range is maximized at a launch angle of
$45^\circ$ on level terrain.
\end{abstract}

\section{Introduction and Kinematic Foundations}
\label{sec:intro}

Projectile motion is the archetypal example of two-dimensional (2D) kinematics: an object is launched with
initial speed $v_0$ at an angle $\theta$ above the horizontal and subsequently moves under the influence of
gravity alone. The central simplification that makes this problem analytically tractable is the
\emph{independence of the horizontal and vertical components of motion}. Because gravitational acceleration
acts exclusively along the vertical axis, the initial velocity vector may be decomposed into orthogonal
components,
\[
v_{x0} = v_0 \cos\theta, \qquad v_{y0} = v_0 \sin\theta,
\]
and each component evolves according to its own one-dimensional equations of motion: the horizontal
component under zero acceleration, and the vertical component under constant acceleration $-g$. This
decoupling allows the full two-dimensional trajectory to be reconstructed by solving two independent
one-dimensional problems and combining the results parametrically in time.

\section{Derivation of Governing Equations}
\label{sec:derivation}

Taking the launch point as the origin, with $x$ measured horizontally and $y$ measured vertically upward,
the equations of motion under constant gravitational acceleration $g$ are

\begin{align}
  x(t) &= v_0 \cos\theta \; t, \label{eq:xt} \\
  y(t) &= v_0 \sin\theta \; t - \tfrac{1}{2} g t^2. \label{eq:yt}
\end{align}

The corresponding velocity components follow by differentiation with respect to time:
\begin{align}
  v_x(t) &= v_0 \cos\theta, \label{eq:vx} \\
  v_y(t) &= v_0 \sin\theta - g t. \label{eq:vy}
\end{align}

Equation~\eqref{eq:vx} shows that the horizontal velocity is constant throughout the flight, while
Equation~\eqref{eq:vy} shows that the vertical velocity decreases linearly, reaching zero at the apex of the
trajectory. Setting $v_y(t) = 0$ gives the time to reach maximum height, $t_{\mathrm{apex}} = v_0 \sin\theta
/ g$. Assuming the projectile lands at the same elevation from which it was launched ($y = 0$), the total
time of flight is twice the time to apex:
\begin{equation}
  T = \frac{2 v_0 \sin\theta}{g}. \label{eq:T}
\end{equation}

Substituting $t_{\mathrm{apex}}$ into Equation~\eqref{eq:yt} yields the maximum height,
\begin{equation}
  H = \frac{\left(v_0 \sin\theta\right)^2}{2g}. \label{eq:H}
\end{equation}

Finally, substituting the total time of flight $T$ into Equation~\eqref{eq:xt} and applying the double-angle
identity $2\sin\theta\cos\theta = \sin(2\theta)$ gives the horizontal range,
\begin{equation}
  R = \frac{v_0^2 \sin(2\theta)}{g}. \label{eq:R}
\end{equation}

Equation~\eqref{eq:R} is maximized when $\sin(2\theta) = 1$, i.e.\ at $\theta = 45^\circ$, independent of the
launch speed $v_0$.

\section{Trajectory and Parametric Analysis}
\label{sec:analysis}

Figure~\ref{fig:trajectories} shows trajectories computed from Equations~\eqref{eq:xt}--\eqref{eq:yt} for a
fixed launch speed of $v_0 = 25~\mathrm{m/s}$ across five representative launch angles. Each curve's apex,
corresponding to the maximum height given by Equation~\eqref{eq:H}, is marked with a filled circle. As
$\theta$ increases from $15^\circ$ toward $75^\circ$, the trajectories become progressively taller and
narrower, trading horizontal range for vertical reach.

\begin{figure}[htbp]
  \centering
  \includegraphics[width=0.85\textwidth]{fig1_trajectories.png}
  \caption{Projectile trajectories for $v_0 = 25~\mathrm{m/s}$ at launch angles
  $\theta \in \{15^\circ, 30^\circ, 45^\circ, 60^\circ, 75^\circ\}$. Filled circles mark the maximum height
  of each trajectory.}
  \label{fig:trajectories}
\end{figure}

Figure~\ref{fig:range} evaluates Equation~\eqref{eq:R} continuously over $\theta \in [0^\circ, 90^\circ]$,
illustrating the symmetric, single-peaked relationship between range and launch angle. The range vanishes at
both $\theta = 0^\circ$ (a purely horizontal launch that never gains altitude) and $\theta = 90^\circ$ (a
purely vertical launch with no horizontal component), and is maximized at $\theta = 45^\circ$, as predicted
analytically in Section~\ref{sec:derivation}.

\begin{figure}[htbp]
  \centering
  \includegraphics[width=0.85\textwidth]{fig2_range_angle.png}
  \caption{Horizontal range $R$ as a function of launch angle $\theta$ for $v_0 = 25~\mathrm{m/s}$, with the
  maximum range at $\theta = 45^\circ$ highlighted.}
  \label{fig:range}
\end{figure}

\section{Quantitative Summary Table}
\label{sec:table}

Table~\ref{tab:summary} lists the time of flight $T$, maximum height $H$, and horizontal range $R$ computed
from Equations~\eqref{eq:T}--\eqref{eq:R} for the same five launch angles shown in
Figure~\ref{fig:trajectories}, with $v_0 = 25~\mathrm{m/s}$ and $g = 9.81~\mathrm{m/s^2}$ held fixed.

\begin{table}[htbp]
  \centering
  \caption{Time of flight, maximum height, and range for $v_0 = 25~\mathrm{m/s}$ at five launch angles.}
  \label{tab:summary}
  \begin{tabular}{@{}lccc@{}}
    \toprule
    Launch Angle $\theta$ & Time of Flight $T$ (s) & Max Height $H$ (m) & Range $R$ (m) \\
    \midrule
%%TABLE_ROWS%%
    \bottomrule
  \end{tabular}
\end{table}

\section{Conclusion and Discussion}
\label{sec:conclusion}

The analysis presented here confirms, both analytically and numerically, that idealized two-dimensional
projectile motion under constant gravity decouples into independent horizontal and vertical
one-dimensional problems. The derived closed-form expressions for time of flight, maximum height, and
range (Equations~\eqref{eq:T}--\eqref{eq:R}) accurately describe the trajectories in
Figure~\ref{fig:trajectories} and the range--angle relationship in Figure~\ref{fig:range}, with the maximum
range occurring at $\theta = 45^\circ$ as expected from the $\sin(2\theta)$ dependence in
Equation~\eqref{eq:R}. This idealized model neglects air resistance, which in practice reduces range and
introduces an asymmetric trajectory with an optimal launch angle typically below $45^\circ$; extending this
analysis to include quadratic drag is a natural next step and is treated in a companion numerical study.

\end{document}
"""

tex_source = tex_source.replace("%%TABLE_ROWS%%", table_tex_rows)

tex_path = os.path.join(BUILD_DIR, f"{TEX_NAME}.tex")
with open(tex_path, "w") as f:
    f.write(tex_source)

print(f"Wrote {tex_path}")

# ---------------------------------------------------------------------------
# Compile with pdflatex (run twice to resolve references)
# ---------------------------------------------------------------------------
pdflatex = shutil.which("pdflatex")
if not pdflatex:
    sys.exit("pdflatex not found on PATH — install a LaTeX distribution (e.g. MacTeX/TeX Live).")

for i in range(2):
    result = subprocess.run(
        [pdflatex, "-interaction=nonstopmode", "-halt-on-error", f"{TEX_NAME}.tex"],
        cwd=BUILD_DIR, capture_output=True, text=True,
    )
    if result.returncode != 0:
        print(result.stdout[-4000:])
        print(result.stderr[-2000:])
        sys.exit(f"pdflatex failed on pass {i + 1}")
    print(f"pdflatex pass {i + 1} succeeded")

built_pdf = os.path.join(BUILD_DIR, f"{TEX_NAME}.pdf")
final_pdf = f"{TEX_NAME}.pdf"
shutil.copy(built_pdf, final_pdf)

# also keep a copy of the .tex source at the top level, per the spec
shutil.copy(tex_path, f"{TEX_NAME}.tex")

# ---------------------------------------------------------------------------
# Clean up build artifacts
# ---------------------------------------------------------------------------
for ext in (".aux", ".log", ".out"):
    p = os.path.join(BUILD_DIR, f"{TEX_NAME}{ext}")
    if os.path.exists(p):
        os.remove(p)
shutil.rmtree(BUILD_DIR)

print(f"Saved {final_pdf}")
