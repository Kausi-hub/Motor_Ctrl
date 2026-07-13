import streamlit as st
from models.session import initialize_state
initialize_state()

st.title(
    "Ziegler-Nichols PID Tuning"
)

Ku = st.number_input(
    "Ultimate Gain (Ku)",
    value=10.0
)

Pu = st.number_input(
    "Oscillation Period (Pu)",
    value=2.0
)

if st.button(
    "Calculate"
):

    kp = 0.6*Ku

    ki = 1.2*Ku/Pu

    kd = 0.075*Ku*Pu

    st.success(

        f"""
        Kp = {kp:.3f}

        Ki = {ki:.3f}

        Kd = {kd:.3f}
        """
    )

    if st.button(
        "Apply to Simulation"
    ):

        st.session_state.kp = kp

        st.session_state.ki = ki

        st.session_state.kd = kd

st.sidebar.title(
    "Navigation"
)

st.sidebar.info(
    """
    1. Run Simulation

    2. Auto Tune PID

    3. Analyze Stability

    4. Validate Requirements

    5. Generate Reports
    """
)