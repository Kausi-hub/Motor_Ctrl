import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from models.session import initialize_state

initialize_state()

# ==========================================================
# METRICS
# ==========================================================

def calculate_metrics(time_data,response_data,target):

    if not response_data:
        return {}

    peak_value = max(response_data)
    overshoot = max(0,((peak_value - target) / abs(target)) * 100)
    final_value = response_data[-1]
    steady_state_error = (target - final_value)

    # Rise Time (10%-90%)
    rise_time = None
    t10 = None
    t90 = None

    for t, y in zip(time_data,response_data):

        if t10 is None and y >= 0.1 * target: t10 = t

        if t90 is None and y >= 0.9 * target:
            t90 = t
            break

    if (t10 is not None and t90 is not None):
        rise_time = t90 - t10

    # Settling Time (2%)
    settling_time = None
    band = abs(target) * 0.02

    for i in range(len(response_data)):

        if all(abs(v - target) <= band for v in response_data[i:]):
            settling_time = time_data[i]
            break

    return {

        "Overshoot":round(overshoot, 3),
        "Rise Time":
            round(rise_time, 3)
            if rise_time is not None
            else None,
        "Settling Time":
            round(settling_time, 3)
            if settling_time is not None
            else None,
        "Steady State Error":
            round(steady_state_error,3),
        "Peak Value":
            round(peak_value,3)
    }

# ==========================================================
# PAGE
# ==========================================================

st.title("Simulation")
st.write("Run a PID-based closed-loop simulation.")

# ==========================================================
# INPUTS
# ==========================================================

plant = st.selectbox("Plant",["Ideal Motor","First Order","Second Order","DC Motor"])
target = st.number_input("Target",value=100.0)

kp = st.number_input("Kp",value=1.0)
ki = st.number_input("Ki",value=0.1)
kd = st.number_input("Kd",value=0.05)
duration = st.number_input("Simulation Duration (s)",value=20.0)
dt = st.number_input("Time Step (s)",value=0.1)

# ==========================================================
# SIMULATION
# ==========================================================

if st.button("Run"):

    time_data = []
    response_data = []
    control_data = []
    response = 0.0
    integral = 0.0
    previous_error = 0.0
    t = 0.0

    while t <= duration:

        error = target - response
        integral += error * dt
        derivative = (error - previous_error) / dt
        control_signal = (kp * error + ki * integral + kd * derivative)

        # Simple dynamic model

        if plant == "Ideal Motor":

            response += (control_signal) * dt

        elif plant == "First Order":

            response += (control_signal - response) * dt

        elif plant == "Second Order":

            response += (0.8 * (control_signal - response)) * dt

        elif plant == "DC Motor":

            response += (0.6 * (control_signal - response)) * dt

        previous_error = error
        time_data.append(t)
        response_data.append(response)
        control_data.append(control_signal)
        t += dt

    # ======================================================
    # METRICS
    # ======================================================

    metrics = calculate_metrics(time_data,response_data,target)

    # ======================================================
    # SAVE TO SESSION
    # ======================================================

    st.session_state.plant_type = plant
    st.session_state.time_data = (time_data)
    st.session_state.response_data = (response_data)
    st.session_state.control_data = (control_data)
    st.session_state.metrics = metrics

    st.success("Simulation complete.")

    # ======================================================
    # DISPLAY METRICS
    # ======================================================

    st.subheader("Performance Metrics")

    c1, c2, c3, c4, c5 = st.columns(5)

    c1.metric("Overshoot %",metrics["Overshoot"])

    c2.metric("Rise Time",
        (
            metrics["Rise Time"]
            if metrics["Rise Time"]
            is not None
            else "N/A"
        )
    )
    c3.metric("Settling Time",
        (
            metrics["Settling Time"]
            if metrics["Settling Time"]
            is not None
            else "N/A"
        )
    )
    c4.metric("SS Error",metrics["Steady State Error"])
    c5.metric("Peak Value",metrics["Peak Value"])

    # ======================================================
    # PLOTS
    # ======================================================

    st.subheader("Simulation Response")
    df = pd.DataFrame({"Time": time_data,"Response": response_data,"Control": control_data})
    st.line_chart(df.set_index("Time"))
    st.dataframe(df,use_container_width=True)

    fig_response, ax = plt.subplots(figsize=(10, 5))
    ax.plot(time_data, response_data, label="Response", color="blue")
    ax.axhline(y=target, color="red", linestyle="--", label="Target")
    ax.set_xlabel("Time")
    ax.set_ylabel("Response")
    ax.legend()
    st.pyplot(fig_response)
    response_plot_file = "response_plot.png"
    st.session_state.response_plot = response_plot_file
    fig_control, ax = plt.subplots(figsize=(10,5))
    ax.plot(time_data,control_data,color="green")
    ax.set_title("Control Effort")
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Control Signal")
    ax.grid(True)
    st.pyplot(fig_control)
    control_plot_file = "control_plot.png"
    fig_control.savefig(control_plot_file,bbox_inches="tight")
    plt.close(fig_control)
    st.session_state.control_plot = (control_plot_file)
    st.write(st.session_state.response_plot)
    st.write(st.session_state.control_plot)


# ==========================================================
# SIDEBAR
# ==========================================================

st.sidebar.title("Navigation")
st.sidebar.info(
    """
    1. Run Simulation
    2. Auto Tune PID
    3. Analyze Stability
    4. Validate Requirements
    5. Generate Reports
    """
)