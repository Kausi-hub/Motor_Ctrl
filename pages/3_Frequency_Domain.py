import streamlit as st
import matplotlib.pyplot as plt
import control
from models.session import initialize_state
initialize_state()

st.title(
    "Frequency Domain Analysis"
)

plant = control.TransferFunction(

    [1],
    [1,5,6]
)

gm, pm, wg, wp = control.margin(
    plant
)

c1,c2 = st.columns(2)

c1.metric(
    "Gain Margin",
    f"{gm:.2f}"
)

c2.metric(
    "Phase Margin",
    f"{pm:.2f}"
)

st.subheader(
    "Bode Plot"
)

fig = plt.figure()

control.bode_plot(
    plant
)

st.pyplot(fig)

st.subheader(
    "Nyquist Plot"
)

fig2 = plt.figure()

control.nyquist_plot(
    plant
)

st.pyplot(fig2)
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