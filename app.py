import streamlit as st

st.set_page_config(
    page_title="Control Systems Engineering Workbench",
    layout="wide"
)

st.title("Control Systems Engineering Workbench")

st.markdown("""
Welcome to the Control Engineering Workbench.

Use the navigation menu to access:

- Simulation
- PID Auto Tuning
- Frequency Domain Analysis
- Requirements Validation
- Report Generation
""")

st.image(
    "https://images.unsplash.com/photo-1518770660439-4636190af475",
    width=True
)