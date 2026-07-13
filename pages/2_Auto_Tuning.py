# pages/2_Auto_Tuning.py

import streamlit as st

from models.session import (
    initialize_state
)

initialize_state()

# ==========================================================
# ZIEGLER-NICHOLS
# ==========================================================

def ziegler_nichols_pid(
    Ku,
    Pu
):
    """
    Classic Ziegler-Nichols PID tuning.

    Kp = 0.6 Ku
    Ki = 1.2 Ku / Pu
    Kd = 0.075 Ku Pu
    """

    kp = 0.6 * Ku

    ki = (
        1.2 * Ku / Pu
        if Pu > 0
        else 0
    )

    kd = 0.075 * Ku * Pu

    return kp, ki, kd


# ==========================================================
# PAGE
# ==========================================================

st.title(
    "PID Auto Tuning"
)

st.write(
    """
    Automatically calculate PID gains using
    the Ziegler-Nichols tuning method.
    """
)

# ==========================================================
# CURRENT VALUES
# ==========================================================

st.subheader(
    "Current Controller Gains"
)

c1, c2, c3 = st.columns(3)

c1.metric(
    "Kp",
    f"{st.session_state.kp:.4f}"
)

c2.metric(
    "Ki",
    f"{st.session_state.ki:.4f}"
)

c3.metric(
    "Kd",
    f"{st.session_state.kd:.4f}"
)

# ==========================================================
# INPUTS
# ==========================================================

st.subheader(
    "Ziegler-Nichols Parameters"
)

col1, col2 = st.columns(2)

with col1:

    Ku = st.number_input(
        "Ultimate Gain (Ku)",
        min_value=0.001,
        value=float(
            st.session_state.ultimate_gain
        ),
        step=0.1
    )

with col2:

    Pu = st.number_input(
        "Oscillation Period (Pu)",
        min_value=0.001,
        value=float(
            st.session_state.ultimate_period
        ),
        step=0.1
    )

# Save user entries

st.session_state.ultimate_gain = Ku
st.session_state.ultimate_period = Pu

# ==========================================================
# CALCULATE
# ==========================================================

if st.button(
    "Calculate PID Gains"
):

    kp, ki, kd = ziegler_nichols_pid(
        Ku,
        Pu
    )

    st.session_state.tuned_kp = kp
    st.session_state.tuned_ki = ki
    st.session_state.tuned_kd = kd

    st.success(
        "PID gains calculated successfully."
    )

# ==========================================================
# RESULTS
# ==========================================================

if all(
    key in st.session_state
    for key in [
        "tuned_kp",
        "tuned_ki",
        "tuned_kd"
    ]
):

    st.subheader(
        "Recommended PID Gains"
    )

    r1, r2, r3 = st.columns(3)

    r1.metric(
        "Recommended Kp",
        f"{st.session_state.tuned_kp:.4f}"
    )

    r2.metric(
        "Recommended Ki",
        f"{st.session_state.tuned_ki:.4f}"
    )

    r3.metric(
        "Recommended Kd",
        f"{st.session_state.tuned_kd:.4f}"
    )

    st.markdown("---")

    if st.button(
        "Apply Tuned Gains to Simulation"
    ):

        st.session_state.kp = (
            st.session_state.tuned_kp
        )

        st.session_state.ki = (
            st.session_state.tuned_ki
        )

        st.session_state.kd = (
            st.session_state.tuned_kd
        )

        st.success(
            "Tuned gains applied successfully."
        )

# ==========================================================
# TUNING GUIDE
# ==========================================================

with st.expander(
    "PID Tuning Guidance"
):

    st.markdown(
        """
### Ziegler-Nichols Procedure

1. Set Ki = 0
2. Set Kd = 0
3. Increase Kp until sustained oscillation occurs
4. Record:

   - Ku = Ultimate Gain
   - Pu = Oscillation Period

5. Enter Ku and Pu in this page

The application then computes:

- Kp = 0.6 × Ku
- Ki = 1.2 × Ku / Pu
- Kd = 0.075 × Ku × Pu

### Interpretation

**Too Much Overshoot**

- Reduce Kp
- Increase Kd

**Slow Response**

- Increase Kp

**Steady-State Error**

- Increase Ki

**Noisy Control Signal**

- Reduce Kd
        """
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