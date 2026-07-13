import streamlit as st

from models.session import initialize_state

initialize_state()

st.title(
    "Requirements Validation"
)

# ==========================================================
# VERIFY METRICS EXIST
# ==========================================================

metrics = st.session_state.get(
    "metrics",
    {}
)

required_keys = [
    "Overshoot",
    "Rise Time",
    "Settling Time",
    "Steady State Error",
    "Peak Value"
]

if not all(
    key in metrics
    for key in required_keys
):

    st.warning(
        "No simulation results available.\n\n"
        "Run a simulation first."
    )

    st.stop()

# ==========================================================
# DISPLAY CURRENT METRICS
# ==========================================================

st.subheader(
    "Current Simulation Metrics"
)

c1, c2, c3, c4, c5 = st.columns(5)

c1.metric(
    "Overshoot %",
    metrics["Overshoot"]
)

c2.metric(
    "Rise Time",
    (
        metrics["Rise Time"]
        if metrics["Rise Time"]
        is not None
        else "N/A"
    )
)

c3.metric(
    "Settling Time",
    (
        metrics["Settling Time"]
        if metrics["Settling Time"]
        is not None
        else "N/A"
    )
)

c4.metric(
    "SS Error",
    metrics[
        "Steady State Error"
    ]
)

c5.metric(
    "Peak Value",
    metrics["Peak Value"]
)

st.markdown("---")

# ==========================================================
# REQUIREMENTS
# ==========================================================

st.subheader(
    "Requirements"
)

max_overshoot = st.number_input(
    "Maximum Overshoot (%)",
    value=10.0
)

max_settling = st.number_input(
    "Maximum Settling Time (s)",
    value=5.0
)

max_error = st.number_input(
    "Maximum Steady State Error",
    value=1.0
)

# ==========================================================
# EVALUATE
# ==========================================================

if st.button(
    "Validate Requirements"
):

    results = []

    passed = 0

    if (
        metrics["Overshoot"]
        <= max_overshoot
    ):

        results.append(
            "✅ PASS: Overshoot Requirement"
        )

        passed += 1

    else:

        results.append(
            "❌ FAIL: Overshoot Requirement"
        )

    settling_time = metrics[
        "Settling Time"
    ]

    if (
        settling_time is not None
        and settling_time
        <= max_settling
    ):

        results.append(
            "✅ PASS: Settling Time Requirement"
        )

        passed += 1

    else:

        results.append(
            "❌ FAIL: Settling Time Requirement"
        )

    if (
        abs(
            metrics[
                "Steady State Error"
            ]
        )
        <= max_error
    ):

        results.append(
            "✅ PASS: Steady State Error Requirement"
        )

        passed += 1

    else:

        results.append(
            "❌ FAIL: Steady State Error Requirement"
        )

    score = (
        passed / 3
    ) * 100

    st.subheader(
        "Validation Results"
    )

    for result in results:

        st.write(result)

    st.metric(
        "Requirements Score",
        f"{score:.1f}%"
    )

    if score == 100:

        st.success(
            "All requirements satisfied."
        )

    else:

        st.warning(
            "One or more requirements failed."
        )

# ==========================================================
# SIDEBAR
# ==========================================================

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