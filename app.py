import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import json

from datetime import datetime

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="PID Control Engineering Workbench",
    layout="wide"
)

# ==========================================================
# PID CONTROLLER
# ==========================================================

class PIDController:

    def __init__(self, kp, ki, kd):

        self.kp = kp
        self.ki = ki
        self.kd = kd

        self.prev_error = 0.0
        self.integral = 0.0

    def compute(
        self,
        setpoint,
        measured_value
    ):

        error = setpoint - measured_value
        self.integral += error
        derivative = error - self.prev_error

        output = (
            self.kp * error
            + self.ki * self.integral
            + self.kd * derivative
        )

        self.prev_error = error
        return output

# ==========================================================
# MOTOR MODEL
# ==========================================================

class Motor:

    def __init__(self):

        self.position = 0.0
        self.speed = 0.0

        self.positions = []
        self.speeds = []
        self.times = []

        self.errors = []

        self.position_commands = []
        self.speed_commands = []

    def update_position(self,speed,time_step,target_position):

        self.position += speed * time_step

        if not self.times:
            current_time = time_step
        else:
            current_time = self.times[-1] + time_step

        self.times.append(current_time)
        self.positions.append(self.position)
        self.speeds.append(speed)
        self.errors.append(
            target_position - self.position
        )

# ==========================================================
# PERFORMANCE METRICS
# ==========================================================

def compute_metrics(times,positions,target):

    if len(positions) == 0:

        return {
            "Rise Time": None,
            "Settling Time": None,
            "Overshoot (%)": 0,
            "Steady State Error": target,
            "Peak Position": 0
        }

    final_value = positions[-1]
    steady_state_error = target - final_value
    peak_position = max(positions)

    if target != 0:
        overshoot = max(0,((peak_position - target) / target) * 100)
    else:
        overshoot = 0

    rise_time = None

    for t, p in zip(times,positions):
        if p >= 0.9 * target:
            rise_time = t
            break

    settling_time = None
    settling_band = abs(target) * 0.02

    for i in range(len(positions)):

        remaining = positions[i:]

        if all(abs(p - target) <= settling_band for p in remaining):
            settling_time = times[i]
            break

    return {
        "Rise Time": rise_time,
        "Settling Time": settling_time,
        "Overshoot (%)": overshoot,
        "Steady State Error": steady_state_error,
        "Peak Position": peak_position
    }

# ==========================================================
# SIMULATION
# ==========================================================

def run_simulation(target_position,pos_kp,pos_ki,pos_kd,speed_kp,speed_ki,speed_kd,time_step,max_iterations):

    position_pid = PIDController(pos_kp,pos_ki,pos_kd)
    speed_pid = PIDController(speed_kp,speed_ki,speed_kd)
    motor = Motor()
    reached_target = False

    for _ in range(max_iterations):

        position_error = (
            target_position
            - motor.position
        )

        if abs(position_error) < 0.5:
            reached_target = True

        speed_command = position_pid.compute(target_position,motor.position)

        for _ in range(10):

            speed_adjustment = speed_pid.compute(speed_command,motor.speed)
            motor.position_commands.append(speed_command)
            motor.speed_commands.append(speed_adjustment)
            motor.speed += speed_adjustment
            motor.update_position(motor.speed,time_step,target_position)

    return motor, reached_target

# ==========================================================
# TITLE
# ==========================================================

st.title("PID Control Engineering Workbench")

st.write(
    """
    Simulate cascaded PID position control,
    evaluate system performance,
    validate requirements,
    and generate engineering reports.
    """
)

# ==========================================================
# CONTROL PARAMETERS
# ==========================================================

col1, col2 = st.columns(2)

with col1:

    st.subheader("Position PID Controller")
    pos_kp = st.number_input("Position Kp",value=1.0)
    pos_ki = st.number_input("Position Ki",value=0.1)
    pos_kd = st.number_input("Position Kd",value=0.05)

with col2:

    st.subheader("Speed PID Controller")
    speed_kp = st.number_input("Speed Kp",value=0.5)
    speed_ki = st.number_input("Speed Ki",value=0.05)
    speed_kd = st.number_input("Speed Kd",value=0.02)

st.markdown("---")

# ==========================================================
# SIMULATION SETTINGS
# ==========================================================

st.subheader("Simulation Settings")

target_position = st.number_input("Target Position",value=100.0)
time_step = st.slider("Time Step (s)",0.01,1.0,0.1,0.01)
max_iterations = st.slider("Max Iterations",50,1000,200)

# ==========================================================
# REQUIREMENTS
# ==========================================================

st.subheader("Control Requirements")

r1, r2, r3 = st.columns(3)

with r1:

    required_overshoot = st.number_input("Max Overshoot (%)",value=10.0)

with r2:

    required_settling_time = st.number_input("Max Settling Time (s)",value=10.0)

with r3:

    required_error = st.number_input("Max Steady-State Error",value=1.0)

# ==========================================================
# RUN BUTTON
# ==========================================================

if st.button("Run Simulation"):

    motor, reached_target = run_simulation(
        target_position, pos_kp, pos_ki, pos_kd, speed_kp, speed_ki, speed_kd, time_step, max_iterations
    )

    metrics = compute_metrics(motor.times, motor.positions, target_position)

    st.markdown("---")
    st.header("Performance Metrics")

    m1, m2, m3, m4, m5 = st.columns(5)
    m1.metric(
        "Rise Time",
        (
            f"{metrics['Rise Time']:.2f}s"
            if metrics['Rise Time']
            else "N/A"
        )
    )

    m2.metric(
        "Settling Time",
        (
            f"{metrics['Settling Time']:.2f}s"
            if metrics['Settling Time']
            else "N/A"
        )
    )

    m3.metric("Overshoot",f"{metrics['Overshoot (%)']:.2f}%")
    m4.metric("SS Error",f"{metrics['Steady State Error']:.2f}")
    m5.metric("Peak Position",f"{metrics['Peak Position']:.2f}")

    # ======================================================
    # REQUIREMENTS VALIDATION
    # ======================================================

    st.header("Requirement Validation")

    results = []

    if (
        metrics["Overshoot (%)"]
        <= required_overshoot
    ):
        results.append("✅ Overshoot requirement satisfied")
    else:
        results.append("❌ Overshoot requirement violated")

    if (
        metrics["Settling Time"] is not None
        and
        metrics["Settling Time"]
        <= required_settling_time
    ):
        results.append("✅ Settling time requirement satisfied")
    else:
        results.append("❌ Settling time requirement violated")

    if (abs(metrics["Steady State Error"]) <= required_error):
        results.append("✅ Steady-state error requirement satisfied")
    else:
        results.append("❌ Steady-state error requirement violated")

    for result in results:
        st.write(result)

    # ======================================================
    # AUTO TUNING RECOMMENDATIONS
    # ======================================================

    st.header("PID Recommendations")

    recommendations = []

    if metrics["Overshoot (%)"] > required_overshoot:
        recommendations.append("Increase Position Kd or reduce Position Kp.")

    if abs(metrics["Steady State Error"]) > required_error:
        recommendations.append("Increase Position Ki.")

    if (
        metrics["Settling Time"] is not None
        and
        metrics["Settling Time"]
        > required_settling_time
    ):
        recommendations.append("Increase Position Kp.")

    if not recommendations:
        recommendations.append("Controller performance meets requirements.")

    for r in recommendations:
        st.info(r)

    # ======================================================
    # PLOTS
    # ======================================================

    st.header("Engineering Plots")

    fig, axs = plt.subplots(2,2,figsize=(14, 10))
    axs[0, 0].plot(motor.times,motor.positions)
    axs[0, 0].axhline(y=target_position,linestyle="--",color="red")
    axs[0, 0].set_title("Position Response")
    axs[0, 1].plot(motor.times,motor.speeds)
    axs[0, 1].set_title("Speed Response")
    axs[1, 0].plot(motor.times,motor.position_commands)
    axs[1, 0].set_title("Position PID Output")
    axs[1, 1].plot(motor.times,motor.speed_commands)
    axs[1, 1].set_title("Speed PID Output")

    for ax in axs.flat:
        ax.grid(True)

    plt.tight_layout()
    st.pyplot(fig)

    # ======================================================
    # DATA TABLE
    # ======================================================

    st.header("Simulation Data")

    df = pd.DataFrame({
        "Time": motor.times,
        "Position": motor.positions,
        "Speed": motor.speeds,
        "Error": motor.errors,
        "Position_PID_Output":
            motor.position_commands,
        "Speed_PID_Output":
            motor.speed_commands
    })

    st.dataframe(df,use_container_width=True)

    # ======================================================
    # EXPORT CSV
    # ======================================================

    csv = df.to_csv(index=False)

    st.download_button(
        "Download CSV Results",
        csv,
        file_name="simulation_results.csv",
        mime="text/csv"
    )

    # ======================================================
    # EXPORT REPORT
    # ======================================================

    report = f"""
# PID Control Analysis Report

Generated:
{datetime.now()}

## Target Position
{target_position}

## Performance Metrics
{json.dumps(metrics, indent=2)}

## Requirement Validation
{chr(10).join(results)}

## Recommendations
{chr(10).join(recommendations)}
"""

    st.download_button(
        "Download Markdown Report",
        report,
        file_name="PID_Control_Report.md",
        mime="text/markdown"
    )