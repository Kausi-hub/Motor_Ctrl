# pages/4_Requirements_Validation.py

import streamlit as st

from models.session import initialize_state

from models.metrics import (
    calculate_requirement_score
)

# ==========================================================
# INITIALIZATION
# ==========================================================

initialize_state()

# ==========================================================
# PAGE
# ==========================================================

st.title(
    "Requirements Validation"
)

st.write(
    """
    Validate simulation performance against
    engineering requirements.
    """
)

# ==========================================================
# CHECK SIMULATION DATA
# ==========================================================

metrics = st.session_state.metrics

if not metrics:

    st.warning(
        "No simulation data available.\n\n"
        "Please run a simulation first."
    )

    st.stop()

# ==========================================================
# CURRENT METRICS
# ==========================================================

st.subheader(
    "Current Simulation Metrics"
)

c1, c2, c3 = st.columns(3)

c1.metric(
    "Overshoot (%)",
    metrics.get(
        "Overshoot",
        "N/A"
    )
)

c2.metric(
    "Rise Time (s)",
    metrics.get(
        "Rise Time",
        "N/A"
    )
)

c3.metric(
    "Settling Time (s)",
    metrics.get(
        "Settling Time",
        "N/A"
    )
)

c4, c5, c6 = st.columns(3)

c4.metric(
    "Steady State Error",
    metrics.get(
        "Steady State Error",
        "N/A"
    )
)

c5.metric(
    "Peak Value",
    metrics.get(
        "Peak Value",
        "N/A"
    )
)

c6.metric(
    "RMSE",
    metrics.get(
        "RMSE",
        "N/A"
    )
)

# ==========================================================
# REQUIREMENTS
# ==========================================================

st.markdown("---")

st.subheader(
    "Requirements"
)

max_overshoot = st.number_input(
    "Maximum Overshoot (%)",
    min_value=0.0,
    value=10.0
)

max_settling_time = st.number_input(
    "Maximum Settling Time (s)",
    min_value=0.0,
    value=5.0
)

max_ss_error = st.number_input(
    "Maximum Steady-State Error",
    min_value=0.0,
    value=1.0
)

# ==========================================================
# VALIDATE
# ==========================================================

if st.button(
    "Validate Requirements"
):

    result = calculate_requirement_score(
        metrics,
        max_overshoot,
        max_settling_time,
        max_ss_error
    )

    score = result["score"]

    results = result["results"]

    st.session_state.validation_results = (
        results
    )

    st.session_state.requirement_score = (
        score
    )

    # ======================================================
    # PASS / FAIL RESULTS
    # ======================================================

    st.subheader(
        "Validation Results"
    )

    for item in results:

        if item.startswith("PASS"):

            st.success(item)

        else:

            st.error(item)

    # ======================================================
    # SCORE
    # ======================================================

    st.subheader(
        "Requirements Score"
    )

    st.metric(
        "Compliance Score",
        f"{score:.1f}%"
    )

    if score >= 100:

        st.success(
            "All requirements satisfied."
        )

    elif score >= 66:

        st.warning(
            "Most requirements satisfied."
        )

    else:

        st.error(
            "Requirements not satisfied."
        )

    # ======================================================
    # AUTOMATIC RECOMMENDATIONS
    # ======================================================

    st.subheader(
        "Engineering Recommendations"
    )

    recommendations = []

    overshoot = metrics.get(
        "Overshoot",
        0
    )

    settling_time = metrics.get(
        "Settling Time"
    )

    steady_state_error = abs(
        metrics.get(
            "Steady State Error",
            0
        )
    )

    if overshoot > max_overshoot:

        recommendations.append(
            "Reduce overshoot by decreasing Kp or increasing Kd."
        )

    if (
        settling_time is not None
        and settling_time > max_settling_time
    ):

        recommendations.append(
            "Reduce settling time by increasing Kp."
        )

    if steady_state_error > max_ss_error:

        recommendations.append(
            "Reduce steady-state error by increasing Ki."
        )

    if not recommendations:

        recommendations.append(
            "Controller performance satisfies all current requirements."
        )

    for recommendation in recommendations:

        st.info(recommendation)

    st.session_state.recommendations = (
        recommendations
    )

# ==========================================================
# CURRENT SESSION RESULTS
# ==========================================================

if st.session_state.validation_results:

    st.markdown("---")

    st.subheader(
        "Saved Validation Results"
    )

    for item in st.session_state.validation_results:

        st.write(item)

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