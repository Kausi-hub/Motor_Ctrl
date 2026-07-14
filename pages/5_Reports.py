# pages/5_Reports.py

import os
import tempfile
import streamlit as st
from datetime import datetime
from reportlab.platypus import (SimpleDocTemplate,Paragraph,Spacer,Image,Table,TableStyle,PageBreak)
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from models.session import initialize_state

initialize_state()

st.title("Engineering Report Generator")
st.write(
    """
    Generate a comprehensive control systems
    engineering report containing:
    - Simulation metrics
    - Requirement validation
    - Stability analysis
    - Response plots
    - Frequency-domain plots
    """
)

# DATA AVAILABILITY CHECK
metrics = st.session_state.get("metrics",{})
if not metrics:
    st.warning("No simulation results found.\n\n""Run a simulation before generating a report.")
    st.stop()

# PREVIEW
st.subheader("Report Contents")
st.write(f"Plant Type: {st.session_state.plant_type}")
st.write(f"Target: {st.session_state.target}")
st.json(metrics)

# PDF GENERATION
if st.button("Generate PDF Report"):
    temp_pdf = tempfile.NamedTemporaryFile(delete=False,suffix=".pdf")
    doc = SimpleDocTemplate(temp_pdf.name)
    styles = getSampleStyleSheet()
    content = []
    # TITLE PAGE
    content.append(Paragraph("Control Systems Engineering Report",styles["Title"]))
    content.append(Spacer(1, 20))
    content.append(Paragraph(f"Generated: {datetime.now()}",styles["BodyText"]))
    content.append(Paragraph(f"Plant Type: {st.session_state.plant_type}",styles["BodyText"]))
    content.append(Paragraph(f"Target Setpoint: {st.session_state.target}",styles["BodyText"]))
    content.append(Paragraph(f"Kp: {st.session_state.kp}",styles["BodyText"]))
    content.append(Paragraph(f"Ki: {st.session_state.ki}",styles["BodyText"]))
    content.append(Paragraph(f"Kd: {st.session_state.kd}",styles["BodyText"]))
    content.append(Spacer(1, 20))
    # PERFORMANCE METRICS
    content.append(Paragraph("Performance Metrics",styles["Heading1"]))
    table_data = [["Metric", "Value"]]
    for key, value in metrics.items():
        table_data.append([str(key),str(value)])
    metrics_table = Table(table_data,colWidths=[250, 180])
    metrics_table.setStyle(
        TableStyle([("BACKGROUND",(0, 0),(-1, 0),colors.lightblue),("FONTNAME",(0, 0),(-1, 0),"Helvetica-Bold"),("GRID",(0, 0),(-1, -1),1,colors.black),
            ("BACKGROUND",(0, 1),(-1, -1),colors.whitesmoke)]))
    content.append(metrics_table)
    content.append(Spacer(1, 20))
    # REQUIREMENT VALIDATION
    validation_results = st.session_state.get("validation_results",[])
    if validation_results:
        content.append(Paragraph("Requirement Validation",styles["Heading1"]))
        content.append(Spacer(1, 10))
        for result in validation_results:
            content.append(Paragraph(result,styles["BodyText"]))
        if ("requirement_score" in st.session_state):
            content.append(Spacer(1, 10))
            content.append(Paragraph(f"Compliance Score: "f"{st.session_state.requirement_score:.1f}%",styles["BodyText"]))
            content.append(Spacer(1, 10))
    # RECOMMENDATIONS
    recommendations = st.session_state.get("recommendations",[])
    if recommendations:
        content.append(Paragraph("Engineering Recommendations",styles["Heading1"]))
        content.append(Spacer(1, 10))
        for rec in recommendations:
            content.append(Paragraph(f"• {rec}",styles["BodyText"]))
        content.append(Spacer(1, 20))
    # FREQUENCY DOMAIN
    gm = st.session_state.get("gain_margin")
    pm = st.session_state.get("phase_margin")
    if (gm is not None or pm is not None):
        content.append(Paragraph("Frequency Domain Analysis",styles["Heading1"]))
        content.append(Spacer(1, 10))
        content.append(Paragraph(f"Gain Margin: {gm}",styles["BodyText"]))
        content.append(Paragraph(f"Phase Margin: {pm}",styles["BodyText"]))
        content.append(Spacer(1, 20))
    # PLOTS PAGE
    content.append(PageBreak())
    # RESPONSE PLOT
    response_plot = st.session_state.get("response_plot")
    if (response_plot and os.path.exists(response_plot)):
        content.append(Paragraph("System Response",styles["Heading1"]))
        content.append(Spacer(1, 10))
        content.append(Image(response_plot,width=500,height=250))
        content.append(Spacer(1, 20))
    # CONTROL EFFORT
    control_plot = st.session_state.get("control_plot")
    if (control_plot and os.path.exists(control_plot)):
        content.append(Paragraph("Control Effort",styles["Heading1"]))
        content.append(Spacer(1, 10))
        content.append(Image(control_plot,width=500,height=250))
        content.append(Spacer(1, 20))
    # BODE PLOT
    bode_plot = st.session_state.get("bode_plot")
    if (bode_plot and os.path.exists(bode_plot)):
        content.append(Paragraph("Bode Plot",styles["Heading1"]))
        content.append(Spacer(1, 10))
        content.append(Image(bode_plot,width=500,height=300))
        content.append(Spacer(1, 20))
    # NYQUIST PLOT
    nyquist_plot = st.session_state.get("nyquist_plot")
    if (nyquist_plot and os.path.exists(nyquist_plot)):
        content.append(Paragraph("Nyquist Plot",styles["Heading1"]))
        content.append(Spacer(1, 10))
        content.append(Image(nyquist_plot,width=450,height=450))
        content.append(Spacer(1, 20))
    # BUILD PDF
    doc.build(content)
    st.success("Engineering report generated successfully.")
    st.session_state.report_generated = True
    # DOWNLOAD
    with open(temp_pdf.name,"rb") as pdf:
        st.download_button(
            label="Download PDF Report",data=pdf,file_name=(f"Control_Report_"f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"),mime="application/pdf")
# ==========================================================
# SIDEBAR
# ==========================================================
st.sidebar.title("Navigation")
st.sidebar.info(
    """
    1. Simulation
    2. Auto Tuning
    3. Frequency Domain
    4. Requirements Validation
    5. Reports
    """
)