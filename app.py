"""Streamlit dashboard: 2D projectile motion with quadratic air drag,
compared against the ideal (vacuum) trajectory, integrated with scipy's
solve_ivp and visualized with Plotly."""

import numpy as np
import plotly.graph_objects as go
import streamlit as st

from physics import calculate_vacuum_analytical, solve_trajectory

# ---------------------------------------------------------------------------
# Page setup
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Projectile Motion — Air Resistance Dashboard",
    page_icon="🚀",
    layout="wide",
)

NAVY = "#0B1F3A"
TEAL = "#2EC4B6"
GOLD = "#F2A63D"
RED = "#E0473A"
BLUE = "#6F9DFF"
GRAY = "#8B98AD"

st.markdown(
    """
    <style>
    .block-container { padding-top: 1.6rem; }
    div[data-testid="stMetricValue"] { font-size: 1.35rem; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Presets: (mass kg, radius m, drag coefficient)
# ---------------------------------------------------------------------------
PRESETS = {
    "Baseball": {"m": 0.145, "r": 0.0369, "Cd": 0.30},
    "Golf Ball": {"m": 0.0459, "r": 0.02135, "Cd": 0.25},
    "Cannonball": {"m": 5.44, "r": 0.0600, "Cd": 0.47},
    "Table Tennis Ball": {"m": 0.0027, "r": 0.0200, "Cd": 0.50},
}


def apply_preset():
    choice = st.session_state.preset_choice
    if choice in PRESETS:
        p = PRESETS[choice]
        st.session_state.mass = p["m"]
        st.session_state.radius = p["r"]
        st.session_state.cd = p["Cd"]


# ---------------------------------------------------------------------------
# Sidebar controls
# ---------------------------------------------------------------------------
with st.sidebar:
    st.title("🚀 Simulation Controls")

    st.selectbox(
        "Preset Projectile",
        ["Custom", *PRESETS.keys()],
        key="preset_choice",
        on_change=apply_preset,
    )

    st.markdown("**Launch Parameters**")
    v0 = st.slider("Initial Velocity v₀ (m/s)", 5.0, 100.0, 25.0, step=0.5)
    theta = st.slider("Launch Angle θ (degrees)", 0.0, 90.0, 45.0, step=1.0)
    y0 = st.slider("Launch Height y₀ (m)", 0.0, 100.0, 0.0, step=0.5)

    st.markdown("**Projectile Specs**")
    m = st.slider("Mass m (kg)", 0.001, 10.0, 0.145, step=0.001, format="%.3f", key="mass")
    r = st.slider("Radius r (m)", 0.001, 0.500, 0.0369, step=0.0001, format="%.4f", key="radius")
    Cd = st.slider("Drag Coefficient Cd", 0.0, 1.5, 0.30, step=0.01, key="cd")

    st.markdown("**Environment**")
    rho = st.slider("Air Density ρ (kg/m³)", 0.0, 2.0, 1.225, step=0.005, format="%.3f")
    g = st.slider("Gravity g (m/s²)", 1.0, 25.0, 9.81, step=0.01, format="%.2f")

    st.caption("Set ρ = 0 to make the drag trajectory coincide exactly with the ideal curve.")

# ---------------------------------------------------------------------------
# Physics (core logic lives in physics.py — pure, unit-tested functions;
# this wrapper just adapts/caches results for the dashboard's display needs)
# ---------------------------------------------------------------------------

@st.cache_data(show_spinner=False)
def simulate(v0, theta_deg, y0, m, r, Cd, rho, g):
    ideal = calculate_vacuum_analytical(v0, theta_deg, y0, g)
    drag = solve_trajectory(v0, theta_deg, y0, m, r, Cd, rho, g)

    apex_idx_drag = int(np.argmax(drag["y"]))

    impact_vy_ideal = ideal["vy"][-1]
    impact_speed_ideal = float(np.hypot(ideal["vx0"], impact_vy_ideal))
    impact_angle_ideal = float(np.degrees(np.arctan2(-impact_vy_ideal, ideal["vx0"])))

    # --- Energy (drag case) ---
    KE_drag = 0.5 * m * drag["v"] ** 2
    PE_drag = m * g * drag["y"]
    E_drag = KE_drag + PE_drag
    E0 = 0.5 * m * v0 ** 2 + m * g * y0
    E_lost = E0 - E_drag

    return {
        "k": drag["k"], "landed": drag["landed"],
        "t_drag": drag["t"], "x_drag": drag["x"], "y_drag": drag["y"],
        "vx_drag": drag["vx"], "vy_drag": drag["vy"], "v_drag": drag["v"],
        "t_ideal": ideal["t"], "x_ideal": ideal["x"], "y_ideal": ideal["y"],
        "vx_ideal": ideal["vx"], "vy_ideal": ideal["vy"], "v_ideal": ideal["v"],
        "t_land_drag": drag["T"], "t_land_ideal": ideal["T"],
        "R_drag": drag["R"], "R_ideal": ideal["R"],
        "H_drag": drag["H"], "H_ideal": ideal["H"],
        "apex_idx_drag": apex_idx_drag,
        "impact_speed_drag": drag["impact_speed"], "impact_angle_drag": drag["impact_angle"],
        "impact_speed_ideal": impact_speed_ideal, "impact_angle_ideal": impact_angle_ideal,
        "KE_drag": KE_drag, "PE_drag": PE_drag, "E_drag": E_drag, "E0": E0, "E_lost": E_lost,
    }


res = simulate(v0, theta, y0, m, r, Cd, rho, g)

if not res["landed"]:
    st.warning(
        "The drag trajectory did not reach the ground within the extended integration window. "
        "Results below reflect the longest simulated segment; try adjusting parameters."
    )

# ---------------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------------
st.title("2D Projectile Motion — Ideal vs. Quadratic Air Resistance")
st.caption(
    f"v₀ = {v0:.1f} m/s · θ = {theta:.0f}° · y₀ = {y0:.1f} m · m = {m:.3f} kg · "
    f"r = {r:.4f} m · Cd = {Cd:.2f} · ρ = {rho:.3f} kg/m³ · g = {g:.2f} m/s² · k = {res['k']:.5f}"
)

# ---------------------------------------------------------------------------
# KPI row
# ---------------------------------------------------------------------------
c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric("Range — Ideal", f"{res['R_ideal']:.2f} m")
    pct_loss = (res["R_ideal"] - res["R_drag"]) / res["R_ideal"] * 100 if res["R_ideal"] > 0 else 0.0
    st.metric("Range — Drag", f"{res['R_drag']:.2f} m", delta=f"-{pct_loss:.1f}% vs ideal", delta_color="normal")

with c2:
    st.metric("Max Height — Ideal", f"{res['H_ideal']:.2f} m")
    st.metric("Max Height — Drag", f"{res['H_drag']:.2f} m",
              delta=f"{res['H_drag'] - res['H_ideal']:.2f} m", delta_color="normal")

with c3:
    st.metric("Flight Duration — Ideal", f"{res['t_land_ideal']:.2f} s")
    st.metric("Flight Duration — Drag", f"{res['t_land_drag']:.2f} s",
              delta=f"{res['t_land_drag'] - res['t_land_ideal']:.2f} s", delta_color="off")

with c4:
    st.metric("Impact — Ideal", f"{res['impact_speed_ideal']:.1f} m/s @ {res['impact_angle_ideal']:.0f}°")
    st.metric("Impact — Drag", f"{res['impact_speed_drag']:.1f} m/s @ {res['impact_angle_drag']:.0f}°",
              delta=f"{res['impact_speed_drag'] - res['impact_speed_ideal']:.1f} m/s", delta_color="normal")

st.divider()

# ---------------------------------------------------------------------------
# Tabs
# ---------------------------------------------------------------------------
tab1, tab2, tab3 = st.tabs(["📈 Trajectory Curve", "⏱️ Kinematics over Time", "🔋 Energy Dissipation"])

# ---- Tab 1: trajectory ----
with tab1:
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=res["x_ideal"], y=res["y_ideal"], mode="lines", name="Ideal (vacuum)",
        line={"color": RED, "width": 2.5, "dash": "dash"},
        customdata=np.stack([res["t_ideal"], res["v_ideal"]], axis=-1),
        hovertemplate="t=%{customdata[0]:.2f}s<br>x=%{x:.2f}m  y=%{y:.2f}m<br>v=%{customdata[1]:.2f}m/s<extra>Ideal</extra>",
    ))
    fig.add_trace(go.Scatter(
        x=res["x_drag"], y=res["y_drag"], mode="lines", name="With Drag",
        line={"color": BLUE, "width": 3},
        customdata=np.stack([res["t_drag"], res["v_drag"]], axis=-1),
        hovertemplate="t=%{customdata[0]:.2f}s<br>x=%{x:.2f}m  y=%{y:.2f}m<br>v=%{customdata[1]:.2f}m/s<extra>Drag</extra>",
    ))

    apex_i = res["apex_idx_drag"]
    ideal_apex_i = int(np.argmax(res["y_ideal"]))
    fig.add_trace(go.Scatter(
        x=[res["x_ideal"][ideal_apex_i]], y=[res["y_ideal"][ideal_apex_i]], mode="markers",
        marker={"symbol": "star", "size": 13, "color": RED, "line": {"color": "white", "width": 1}},
        name="Max Height (Ideal)",
        hovertemplate=f"Apex (Ideal)<br>H={res['H_ideal']:.2f} m<extra></extra>",
    ))
    fig.add_trace(go.Scatter(
        x=[res["x_drag"][apex_i]], y=[res["y_drag"][apex_i]], mode="markers",
        marker={"symbol": "star", "size": 13, "color": BLUE, "line": {"color": "white", "width": 1}},
        name="Max Height (Drag)",
        hovertemplate=f"Apex (Drag)<br>H={res['H_drag']:.2f} m<extra></extra>",
    ))
    fig.add_trace(go.Scatter(
        x=[res["x_ideal"][-1]], y=[res["y_ideal"][-1]], mode="markers",
        marker={"symbol": "x", "size": 12, "color": RED, "line": {"width": 2}},
        name="Impact (Ideal)",
        hovertemplate=f"Impact (Ideal)<br>R={res['R_ideal']:.2f} m<extra></extra>",
    ))
    fig.add_trace(go.Scatter(
        x=[res["x_drag"][-1]], y=[res["y_drag"][-1]], mode="markers",
        marker={"symbol": "x", "size": 12, "color": BLUE, "line": {"width": 2}},
        name="Impact (Drag)",
        hovertemplate=f"Impact (Drag)<br>R={res['R_drag']:.2f} m<extra></extra>",
    ))

    fig.update_layout(
        template="plotly_white",
        title="Height vs. Horizontal Distance",
        xaxis_title="Horizontal Distance x (m)",
        yaxis_title="Height y (m)",
        height=560,
        legend={"orientation": "h", "yanchor": "bottom", "y": 1.02, "xanchor": "right", "x": 1},
        margin={"l": 10, "r": 10, "t": 60, "b": 10},
    )
    fig.update_yaxes(rangemode="tozero")
    st.plotly_chart(fig, use_container_width=True)

# ---- Tab 2: kinematics over time ----
with tab2:
    fig2 = go.Figure()
    series = [
        ("vx (Ideal)", res["t_ideal"], res["vx_ideal"], GOLD, "dash"),
        ("vy (Ideal)", res["t_ideal"], res["vy_ideal"], BLUE, "dash"),
        ("v total (Ideal)", res["t_ideal"], res["v_ideal"], RED, "dash"),
        ("vx (Drag)", res["t_drag"], res["vx_drag"], GOLD, "solid"),
        ("vy (Drag)", res["t_drag"], res["vy_drag"], BLUE, "solid"),
        ("v total (Drag)", res["t_drag"], res["v_drag"], RED, "solid"),
    ]
    for name, t, y, color, dash in series:
        fig2.add_trace(go.Scatter(
            x=t, y=y, mode="lines", name=name,
            line={"color": color, "width": 2.5 if dash == "solid" else 2, "dash": dash},
            hovertemplate="t=%{x:.2f}s<br>%{y:.2f} m/s<extra>" + name + "</extra>",
        ))
    fig2.add_hline(y=0, line={"color": "#cccccc", "width": 1})
    fig2.update_layout(
        template="plotly_white",
        title="Velocity Components vs. Time",
        xaxis_title="Time t (s)",
        yaxis_title="Velocity (m/s)",
        height=560,
        legend={"orientation": "h", "yanchor": "bottom", "y": 1.02, "xanchor": "right", "x": 1},
        margin={"l": 10, "r": 10, "t": 60, "b": 10},
    )
    st.plotly_chart(fig2, use_container_width=True)
    st.caption("Dashed = ideal (vacuum) reference. Solid = with drag. Click legend entries to isolate a series.")

# ---- Tab 3: energy dissipation ----
with tab3:
    fig3 = go.Figure()
    fig3.add_trace(go.Scatter(
        x=res["t_drag"], y=res["KE_drag"], mode="lines", name="Kinetic Energy",
        stackgroup="energy", line={"width": 0.5, "color": TEAL}, fillcolor="rgba(46,196,182,0.55)",
        hovertemplate="t=%{x:.2f}s<br>KE=%{y:.1f} J<extra></extra>",
    ))
    fig3.add_trace(go.Scatter(
        x=res["t_drag"], y=res["PE_drag"], mode="lines", name="Potential Energy",
        stackgroup="energy", line={"width": 0.5, "color": GOLD}, fillcolor="rgba(242,166,61,0.55)",
        hovertemplate="t=%{x:.2f}s<br>PE=%{y:.1f} J<extra></extra>",
    ))
    fig3.add_trace(go.Scatter(
        x=res["t_drag"], y=res["E_drag"], mode="lines", name="Total Mechanical Energy",
        line={"color": NAVY, "width": 2.5},
        hovertemplate="t=%{x:.2f}s<br>Total=%{y:.1f} J<extra></extra>",
    ))
    fig3.add_trace(go.Scatter(
        x=res["t_drag"], y=res["E_lost"], mode="lines", name="Energy Lost to Drag (cumulative)",
        line={"color": RED, "width": 2.5, "dash": "dot"},
        hovertemplate="t=%{x:.2f}s<br>Lost=%{y:.1f} J<extra></extra>",
    ))
    fig3.update_layout(
        template="plotly_white",
        title="Energy vs. Time (Drag Trajectory)",
        xaxis_title="Time t (s)",
        yaxis_title="Energy (J)",
        height=560,
        legend={"orientation": "h", "yanchor": "bottom", "y": 1.02, "xanchor": "right", "x": 1},
        margin={"l": 10, "r": 10, "t": 60, "b": 10},
    )
    st.plotly_chart(fig3, use_container_width=True)
    st.caption(
        f"Initial mechanical energy E₀ = {res['E0']:.1f} J. "
        f"By impact, {res['E_lost'][-1]:.1f} J ({res['E_lost'][-1] / res['E0'] * 100:.1f}%) "
        "has been dissipated by air resistance."
    )
