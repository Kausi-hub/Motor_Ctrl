# models/session.py

import streamlit as st


def initialize_state():
    """
    Initialize Streamlit session state variables.
    Call this at the top of every page.
    """

    defaults = {

        # --------------------------------------------------
        # Simulation Inputs
        # --------------------------------------------------

        "plant_type": "Ideal Motor",

        "target": 100.0,

        "kp": 1.0,
        "ki": 0.1,
        "kd": 0.05,

        # --------------------------------------------------
        # Simulation Results
        # --------------------------------------------------

        "time_data": [],
        "response_data": [],
        "control_data": [],

        # --------------------------------------------------
        # Metrics
        # --------------------------------------------------

        "metrics": {
            "Overshoot": 0.0,
            "Rise Time": None,
            "Settling Time": None,
            "Steady State Error": 0.0,
            "Peak Value": 0.0,
        },

        # --------------------------------------------------
        # Validation Results
        # --------------------------------------------------

        "validation_results": [],
        "recommendations": [],
        "requirement_score": None,

        # --------------------------------------------------
        # Plot Files
        # --------------------------------------------------

        "response_plot": None,
        "control_plot": None,
        "bode_plot": None,
        "nyquist_plot": None,

        # --------------------------------------------------
        # Auto-Tuning
        # --------------------------------------------------

        "ultimate_gain": 10.0,
        "ultimate_period": 2.0,

        # --------------------------------------------------
        # Frequency Domain
        # --------------------------------------------------

        "poles": [],
        "zeros": [],
        "transfer_function": "",
        "step_response_plot": None,
        "frequency_domain_results": {},
        "gain_margin": None,
        "phase_margin": None,

        # --------------------------------------------------
        # Report Status
        # --------------------------------------------------

        "report_generated": False
    }

    for key, value in defaults.items():

        if key not in st.session_state:
            st.session_state[key] = value


def reset_simulation_results():
    """
    Clear simulation and analysis results.
    """

    st.session_state.time_data = []
    st.session_state.response_data = []
    st.session_state.control_data = []

    st.session_state.metrics = {
        "Overshoot": 0.0,
        "Rise Time": None,
        "Settling Time": None,
        "Steady State Error": 0.0,
        "Peak Value": 0.0,
    }

    st.session_state.validation_results = []

    st.session_state.response_plot = None
    st.session_state.control_plot = None

    st.session_state.bode_plot = None
    st.session_state.nyquist_plot = None

    st.session_state.gain_margin = None
    st.session_state.phase_margin = None

    st.session_state.report_generated = False