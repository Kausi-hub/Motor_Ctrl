# pages/1_Simulation.py

import os

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from models.session import (
    initialize_state,
    reset_simulation_results
)

from models.pid import PIDController

from models.plants import (
    create_plant
)

from models.metrics import (
    calculate_metrics
)

# ==========================================================
# INITIALIZE
# ==========================================================

initialize_state()

os.makedirs(
    "reports",
    exist_ok=True
)

# ==========================================================
# PAGE
# ==========================================================

st.title(
    "Control System Simulation"
)

st.write(
    """
    Simulate a PID-controlled plant and evaluate
    performance metrics.
    """
)

# ==========================================================
# INPUTS
# ==========================================================

col1, col2 = st.columns(2)

with col1:

    plant_type = st.selectbox(
        "Plant Type",
        [
            "Ideal Motor",
            "First Order",
            "Second Order",
            "DC Motor"
        ],
        index=[
            "Ideal Motor",
            "First Order",
            "Second Order",
            "DC Motor"
        ].index(
            st.session_state.plant_type
        )
    )

    target = st.number_input(
        "Target Setpoint",
        value=float(
            st.session_state.target
        )
    )

with col2:

    duration = st.number_input(
        "Simulation Duration (s)",
        value=20.0,
        step=1.0
    )

    dt = st.number_input(
        "Time Step (s)",
        value=0.01,
        format="%.3f"
    )

# ==========================================================
# PID
# ==========================================================

st.subheader("PID Controller")

c1, c2, c3 = st.columns(3)

with c1:

    kp = st.number_input(
        "Kp",
        value=float(
            st.session_state.kp
        )
    )

with c2:

    ki = st.number_input(
        "Ki",
        value=float(
            st.session_state.ki
        )
    )

with c3:

    kd = st.number_input(
        "Kd",
        value=float(
            st.session_state.kd
        )
    )

# ==========================================================
# RUN
# ==========================================================

if st.button("Run Simulation"):

    reset_simulation_results()

    st.session_state.plant_type = (
        plant_type
    )

    st.session_state.target = (
        target
    )

    st.session_state.kp = kp
    st.session_state.ki = ki
    st.session_state.kd = kd

    plant = create_plant(
        plant_type
    )

    pid = PIDController(
        kp=kp,
        ki=ki,
        kd=kd,
        output_limits=(-10000, 10000)
    )

    # ------------------------------------------------------
    # STORAGE
    # ------------------------------------------------------

    time_data = []
    response_data = []
    control_data = []

    # ------------------------------------------------------
    # LIVE CHART
    # ------------------------------------------------------

    chart_placeholder = st.empty()

    time_now = 0.0
    current_output = 0.0
    while time_now <= duration:

        control_signal = pid.compute(
            setpoint=target,
            measurement=current_output,
            dt=dt
        )

        current_output = plant.update(
            control_signal,
            dt
        )
        response = current_output

        time_data.append(
            time_now
        )

        response_data.append(
            response
        )

        control_data.append(
            control_signal
        )

        time_now += dt

    # ------------------------------------------------------
    # SAVE DATA
    # ------------------------------------------------------

    st.session_state.time_data = (
        time_data
    )

    st.session_state.response_data = (
        response_data
    )

    st.session_state.control_data = (
        control_data
    )

    # ------------------------------------------------------
    # METRICS
    # ------------------------------------------------------

    metrics = calculate_metrics(
        time_data,
        response_data,
        target,
        dt
    )

    st.session_state.metrics = (
        metrics
    )

    # ------------------------------------------------------
    # METRICS DISPLAY
    # ------------------------------------------------------

    st.success(
        "Simulation completed."
    )

    st.subheader(
        "Performance Metrics"
    )

    m1, m2, m3, m4 = st.columns(4)

    m1.metric(
        "Overshoot (%)",
        metrics["Overshoot"]
    )

    m2.metric(
        "Rise Time (s)",
        metrics["Rise Time"]
    )

    m3.metric(
        "Settling Time (s)",
        metrics["Settling Time"]
    )

    m4.metric(
        "Steady State Error",
        metrics[
            "Steady State Error"
        ]
    )

    m5, m6, m7 = st.columns(3)

    m5.metric(
        "Peak Value",
        metrics["Peak Value"]
    )

    m6.metric(
        "RMSE",
        metrics["RMSE"]
    )

    m7.metric(
        "IAE",
        metrics.get(
            "IAE",
            "N/A"
        )
    )

    # ------------------------------------------------------
    # RESPONSE PLOT
    # ------------------------------------------------------

    fig_response, ax = plt.subplots(
        figsize=(10, 5)
    )

    ax.plot(
        time_data,
        response_data,
        label="Response",
        linewidth=2
    )

    ax.axhline(
        target,
        color="red",
        linestyle="--",
        label="Setpoint"
    )

    ax.set_title(
        "System Response"
    )

    ax.set_xlabel(
        "Time (s)"
    )

    ax.set_ylabel(
        "Output"
    )

    ax.grid(True)

    ax.legend()

    response_plot_path = (
        "reports/response_plot.png"
    )

    fig_response.savefig(
        response_plot_path,
        bbox_inches="tight"
    )

    st.session_state.response_plot = (
        response_plot_path
    )

    st.pyplot(
        fig_response
    )

    plt.close(
        fig_response
    )

    # ------------------------------------------------------
    # CONTROL PLOT
    # ------------------------------------------------------

    fig_control, ax = plt.subplots(
        figsize=(10, 5)
    )

    ax.plot(
        time_data,
        control_data,
        color="green",
        linewidth=2
    )

    ax.set_title(
        "Control Effort"
    )

    ax.set_xlabel(
        "Time (s)"
    )

    ax.set_ylabel(
        "Control Signal"
    )

    ax.grid(True)

    control_plot_path = (
        "reports/control_plot.png"
    )

    fig_control.savefig(
        control_plot_path,
        bbox_inches="tight"
    )

    st.session_state.control_plot = (
        control_plot_path
    )

    st.pyplot(
        fig_control
    )

    plt.close(
        fig_control
    )

    # ------------------------------------------------------
    # DATA TABLE
    # ------------------------------------------------------

    st.subheader(
        "Simulation Data"
    )

    df = pd.DataFrame({
        "Time": time_data,
        "Response": response_data,
        "Control Signal": control_data
    })

    st.dataframe(
        df,
        use_container_width=True
    )

    st.download_button(
        label="Download CSV",
        data=df.to_csv(
            index=False
        ),
        file_name="simulation_results.csv",
        mime="text/csv"
    )

# ==========================================================
# EXISTING RESULTS
# ==========================================================

if len(
    st.session_state.response_data
) > 0:

    with st.expander(
        "Current Session Metrics"
    ):

        st.json(
            st.session_state.metrics
        )

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