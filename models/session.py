import streamlit as st

def initialize_state():

    defaults = {

        "time_data": [],
        "response_data": [],
        "control_data": [],
        "metrics": {"Overshoot": 0.0, "Settling Time": 0.0, "Steady State Error": 0.0, "Rise Time": 0.0, "Peak Value": 0.0, "Peak Time": 0.0},
        "plant_type": "Ideal Motor",
        "target": 100
    }

    for key, value in defaults.items():

        if key not in st.session_state:
            st.session_state[key] = value