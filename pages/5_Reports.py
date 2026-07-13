import streamlit as st
import tempfile
import os

from datetime import datetime

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Image,
    Table,
    TableStyle,
    PageBreak
)

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

from models.session import initialize_state

initialize_state()

# ==========================================================
# PAGE
# ==========================================================

st.title("Report Generation")

st.write(
    "Generate a PDF engineering report "
    "containing simulation results, metrics, "
    "plots, and requirement validation results."
)

# ==========================================================
# VERIFY DATA EXISTS
# ==========================================================

metrics = st.session_state.get("metrics",{})

if not metrics:

    st.warning("No simulation results found.\n\n""Run a simulation first.")
    st.stop()

# ==========================================================
# DISPLAY DATA
# ==========================================================

st.subheader("Report Preview")

st.write(
    f"Plant Type: "
    f"{st.session_state.get('plant_type', 'Unknown')}"
)

st.json(metrics)

# ==========================================================
# GENERATE PDF
# ==========================================================

if st.button("Generate PDF Report"):

    pdf_file = tempfile.NamedTemporaryFile(delete=False,suffix=".pdf")
    doc = SimpleDocTemplate(pdf_file.name)
    styles = getSampleStyleSheet()
    content = []

    # ======================================================
    # TITLE
    # ======================================================

    content.append(
        Paragraph(
            "Control Systems Engineering Report",
            styles["Title"]
        )
    )

    content.append(Spacer(1, 15))
    content.append(Paragraph(f"Generated: {datetime.now()}",styles["BodyText"]))

    content.append(
        Paragraph(
            f"Plant Type: "
            f"{st.session_state.get('plant_type', 'Unknown')}",
            styles["BodyText"]
        )
    )

    content.append(Spacer(1, 20))

    # ======================================================
    # METRICS TABLE
    # ======================================================

    content.append(Paragraph("Performance Metrics",styles["Heading1"]))

    table_data = [
        ["Metric", "Value"],
        ["Overshoot (%)",str(metrics.get("Overshoot"))],
        ["Rise Time (s)",str(metrics.get("Rise Time"))],
        ["Settling Time (s)",str(metrics.get("Settling Time"))],
        ["Steady State Error",str(metrics.get("Steady State Error"))],
        ["Peak Value",str(metrics.get("Peak Value"))]
    ]

    metrics_table = Table(table_data,colWidths=[250, 150])
    metrics_table.setStyle(
        TableStyle([

            (
                "BACKGROUND",
                (0, 0),
                (-1, 0),
                colors.lightblue
            ),

            (
                "TEXTCOLOR",
                (0, 0),
                (-1, 0),
                colors.black
            ),

            (
                "GRID",
                (0, 0),
                (-1, -1),
                1,
                colors.black
            ),

            (
                "FONTNAME",
                (0, 0),
                (-1, 0),
                "Helvetica-Bold"
            ),

            (
                "BACKGROUND",
                (0, 1),
                (-1, -1),
                colors.whitesmoke
            )
        ])
    )

    content.append(
        metrics_table
    )

    content.append(
        Spacer(1, 20)
    )

    # ======================================================
    # REQUIREMENT VALIDATION RESULTS
    # ======================================================

    validation_results = st.session_state.get(
        "validation_results",
        []
    )

    if validation_results:

        content.append(
            Paragraph(
                "Requirement Validation",
                styles["Heading1"]
            )
        )

        content.append(
            Spacer(1, 10)
        )

        for result in validation_results:

            content.append(
                Paragraph(
                    result,
                    styles["BodyText"]
                )
            )

        content.append(
            Spacer(1, 20)
        )

    # ======================================================
    # NEW PAGE FOR PLOTS
    # ======================================================

    content.append(
        PageBreak()
    )

    # ======================================================
    # RESPONSE PLOT
    # ======================================================

    response_plot = st.session_state.get(
        "response_plot"
    )

    if (
        response_plot
        and os.path.exists(response_plot)
    ):

        content.append(
            Paragraph(
                "System Response",
                styles["Heading1"]
            )
        )

        content.append(
            Spacer(1, 10)
        )

        content.append(
            Image(
                response_plot,
                width=500,
                height=250
            )
        )

        content.append(
            Spacer(1, 20)
        )

    # ======================================================
    # CONTROL EFFORT PLOT
    # ======================================================

    control_plot = st.session_state.get(
        "control_plot"
    )

    if (
        control_plot
        and os.path.exists(control_plot)
    ):

        content.append(
            Paragraph(
                "Control Effort",
                styles["Heading1"]
            )
        )

        content.append(
            Spacer(1, 10)
        )

        content.append(
            Image(
                control_plot,
                width=500,
                height=250
            )
        )

        content.append(
            Spacer(1, 20)
        )

    # ======================================================
    # BUILD PDF
    # ======================================================

    doc.build(content)

    st.success(
        "PDF report generated successfully."
    )

    # ======================================================
    # DOWNLOAD BUTTON
    # ======================================================

    with open(
        pdf_file.name,
        "rb"
    ) as file:

        st.download_button(
            label="Download PDF Report",
            data=file,
            file_name="Control_Engineering_Report.pdf",
            mime="application/pdf"
        )

    # ======================================================
    # CLEANUP INFO
    # ======================================================

    st.info(
        "Report includes:\n"
        "- Plant Information\n"
        "- Performance Metrics\n"
        "- Requirement Validation Results\n"
        "- Response Plot\n"
        "- Control Effort Plot"
    )