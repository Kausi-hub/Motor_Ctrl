# pages/3_Frequency_Domain.py

import os
import math

import streamlit as st
import matplotlib.pyplot as plt
import control as ctl
import numpy as np

from models.session import initialize_state

initialize_state()

# ==========================================================
# PAGE
# ==========================================================

st.title("Frequency Domain Analysis")

st.write(
    """
    Analyze plant stability using:

    • Transfer Functions

    • Bode Plot

    • Nyquist Plot

    • Gain Margin

    • Phase Margin

    • Pole/Zero Analysis

    • Step Response
    """
)

# ==========================================================
# SETUP
# ==========================================================

os.makedirs(
    "reports",
    exist_ok=True
)

# ==========================================================
# PLANT
# ==========================================================

plant_type = st.session_state.get(
    "plant_type",
    "First Order"
)

st.subheader("Selected Plant")

st.info(plant_type)

# ==========================================================
# TRANSFER FUNCTION MODELS
# ==========================================================

def get_transfer_function(
    plant_type
):

    if plant_type == "Ideal Motor":

        # Double integrator
        return ctl.TransferFunction(
            [1],
            [1, 0, 0]
        )

    elif plant_type == "First Order":

        return ctl.TransferFunction(
            [1],
            [1, 1]
        )

    elif plant_type == "Second Order":

        wn = 5
        zeta = 0.7

        return ctl.TransferFunction(
            [wn**2],
            [1,
             2*zeta*wn,
             wn**2]
        )

    elif plant_type == "DC Motor":

        return ctl.TransferFunction(
            [1],
            [0.005, 0.06, 0.1]
        )

    return ctl.TransferFunction(
        [1],
        [1, 1]
    )

# ==========================================================
# MODEL
# ==========================================================

G = get_transfer_function(
    plant_type
)

st.session_state.transfer_function = str(
    G
)

# ==========================================================
# TRANSFER FUNCTION DISPLAY
# ==========================================================

st.subheader(
    "Transfer Function"
)

st.code(str(G))

# ==========================================================
# STABILITY MARGINS
# ==========================================================

st.subheader(
    "Stability Margins"
)

gm = None
pm = None
wg = None
wp = None

try:

    gm, pm, wg, wp = ctl.margin(G)

    st.session_state.gain_margin = gm
    st.session_state.phase_margin = pm

    if gm is None:
        gm_display = "N/A"

    elif math.isinf(gm):
        gm_display = "∞"

    else:
        gm_display = f"{gm:.3f}"

    if pm is None or np.isnan(pm):
        pm_display = "N/A"
    else:
        pm_display = f"{pm:.3f}"

    c1, c2 = st.columns(2)

    c1.metric(
        "Gain Margin",
        gm_display
    )

    c2.metric(
        "Phase Margin (°)",
        pm_display
    )

except Exception as ex:

    st.error(
        f"Unable to calculate margins: {ex}"
    )

# ==========================================================
# BODE PLOT
# ==========================================================

st.subheader(
    "Bode Plot"
)

try:

    plt.close("all")

    ctl.bode_plot(
        G,
        dB=True,
        deg=True
    )

    fig_bode = plt.gcf()

    bode_plot_file = (
        "reports/bode_plot.png"
    )

    fig_bode.savefig(
        bode_plot_file,
        bbox_inches="tight"
    )

    st.session_state.bode_plot = (
        bode_plot_file
    )

    st.pyplot(fig_bode)

    plt.close(fig_bode)

except Exception as ex:

    st.error(
        f"Bode Plot Error: {ex}"
    )

# ==========================================================
# NYQUIST PLOT
# ==========================================================

st.subheader(
    "Nyquist Plot"
)

try:

    plt.close("all")

    ctl.nyquist_plot(
        G
    )

    fig_nyquist = plt.gcf()

    nyquist_plot_file = (
        "reports/nyquist_plot.png"
    )

    fig_nyquist.savefig(
        nyquist_plot_file,
        bbox_inches="tight"
    )

    st.session_state.nyquist_plot = (
        nyquist_plot_file
    )

    st.pyplot(
        fig_nyquist
    )

    plt.close(
        fig_nyquist
    )

except Exception as ex:

    st.error(
        f"Nyquist Plot Error: {ex}"
    )

# ==========================================================
# STEP RESPONSE
# ==========================================================

st.subheader(
    "Open Loop Step Response"
)

try:

    t, y = ctl.step_response(
        G
    )
    t = np.asarray(t)
    y = np.asarray(y)
    fig_step, ax = plt.subplots(
        figsize=(10, 5)
    )

    ax.plot(
        t,
        y,
        linewidth=2
    )

    ax.set_title(
        "Step Response"
    )

    ax.set_xlabel(
        "Time (s)"
    )

    ax.set_ylabel(
        "Response"
    )

    ax.grid(True)

    step_plot_file = (
        "reports/step_response_plot.png"
    )

    fig_step.savefig(
        step_plot_file,
        bbox_inches="tight"
    )

    st.session_state.step_response_plot = (
        step_plot_file
    )

    st.pyplot(
        fig_step
    )

    plt.close(
        fig_step
    )

except Exception as ex:

    st.error(
        f"Step Response Error: {ex}"
    )

# ==========================================================
# POLES & ZEROS
# ==========================================================

st.subheader(
    "Poles and Zeros"
)

try:

    poles = ctl.poles(G)
    zeros = ctl.zeros(G)

    st.session_state.poles = [
        str(p)
        for p in poles
    ]

    st.session_state.zeros = [
        str(z)
        for z in zeros
    ]

    col1, col2 = st.columns(2)

    with col1:

        st.markdown(
            "### Poles"
        )

        st.code(
            "\n".join(
                str(p)
                for p in poles
            )
        )

    with col2:

        st.markdown(
            "### Zeros"
        )

        if len(zeros) > 0:

            st.code(
                "\n".join(
                    str(z)
                    for z in zeros
                )
            )

        else:

            st.write(
                "No finite zeros."
            )

except Exception as ex:

    st.error(
        f"Pole/Zero Analysis Error: {ex}"
    )

# ==========================================================
# INTERPRETATION
# ==========================================================

st.subheader(
    "Engineering Interpretation"
)

gm = st.session_state.get(
    "gain_margin"
)

pm = st.session_state.get(
    "phase_margin"
)

observations = []

if gm is not None:

    if math.isinf(gm):

        observations.append(
            "ℹ Infinite gain margin."
        )

    elif gm > 6:

        observations.append(
            "✅ Acceptable gain margin."
        )

    else:

        observations.append(
            "⚠ Low gain margin detected."
        )

if (
    pm is not None
    and not np.isnan(pm)
):

    if pm > 45:

        observations.append(
            "✅ Good phase margin."
        )

    elif pm > 0:

        observations.append(
            "⚠ Marginal stability."
        )

    else:

        observations.append(
            "❌ Potential instability."
        )

if not observations:

    observations.append(
        "No stability assessment available."
    )

for item in observations:

    st.write(item)

# ==========================================================
# SAVE RESULTS
# ==========================================================

st.session_state.frequency_domain_results = {

    "Plant": plant_type,

    "Transfer Function":
        str(G),

    "Gain Margin":
        gm,

    "Phase Margin":
        pm,

    "Poles":
        st.session_state.get(
            "poles",
            []
        ),

    "Zeros":
        st.session_state.get(
            "zeros",
            []
        )
}

# ==========================================================
# SIDEBAR
# ==========================================================

st.sidebar.title(
    "Navigation"
)

st.sidebar.info(
    """
    1. Simulation

    2. Auto Tuning

    3. Frequency Domain

    4. Requirements Validation

    5. Reports
    """
)