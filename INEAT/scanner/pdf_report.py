from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)
from reportlab.lib.units import inch

from scanner.services import get_service
from scanner.recommendation_engine import get_recommendations


def generate_pdf(
        target,
        open_ports,
        exposure_score,
        risk_level,
        security_grade
):

    filename = f"{target}_Report.pdf"

    doc = SimpleDocTemplate(
        filename,
        rightMargin=30,
        leftMargin=30,
        topMargin=30,
        bottomMargin=30
    )

    styles = getSampleStyleSheet()

    elements = []

    # ==========================================================
    # REPORT TITLE
    # ==========================================================

    title = styles["Title"]
    title.alignment = TA_CENTER

    elements.append(
        Paragraph(
            "Intelligent Network Exposure Assessment Tool (INEAT)",
            title
        )
    )

    elements.append(Spacer(1, 0.25 * inch))

    # ==========================================================
    # SCAN SUMMARY
    # ==========================================================

    summary_data = [

        ["Target", target],

        [
            "Open Ports",
            ", ".join(map(str, open_ports))
            if open_ports else "None"
        ],

        [
            "Exposure Score",
            f"{exposure_score}/100"
        ],

        [
            "Overall Risk",
            risk_level
        ],

        [
            "Security Grade",
            security_grade
        ]

    ]

    summary_table = Table(

        summary_data,

        colWidths=[2.2 * inch, 4.2 * inch]

    )

    summary_table.setStyle(TableStyle([

        ("BACKGROUND", (0, 0), (0, -1), colors.lightgrey),

        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),

        ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),

        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),

        ("TOPPADDING", (0, 0), (-1, -1), 8),

        ("VALIGN", (0, 0), (-1, -1), "MIDDLE")

    ]))

    elements.append(summary_table)

    elements.append(Spacer(1, 0.30 * inch))

    # ==========================================================
    # OPEN PORTS SUMMARY
    # ==========================================================

    elements.append(

        Paragraph(

            "<b>Open Ports Summary</b>",

            styles["Heading2"]

        )

    )

    table_data = [[

        "Port",

        "Service",

        "Protocol",

        "Category",

        "Risk"

    ]]

    for port in open_ports:

        info = get_service(port)

        table_data.append([

            str(port),

            info["service"],

            info["protocol"],

            info["category"],

            info["risk"]

        ])

    ports_table = Table(

        table_data,

        colWidths=[

            0.7 * inch,

            1.8 * inch,

            0.9 * inch,

            2.2 * inch,

            0.8 * inch

        ]

    )

    ports_table.setStyle(TableStyle([

        ("BACKGROUND", (0, 0), (-1, 0), colors.darkblue),

        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),

        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),

        ("BACKGROUND", (0, 1), (-1, -1), colors.beige),

        ("ALIGN", (0, 0), (-1, -1), "CENTER"),

        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),

        ("BOTTOMPADDING", (0, 0), (-1, 0), 8),

        ("TOPPADDING", (0, 1), (-1, -1), 6)

    ]))

    elements.append(ports_table)

    elements.append(Spacer(1, 0.30 * inch))

    # ==========================================================
    # PORT DETAILS
    # ==========================================================
    elements.append(
        Paragraph(
            "<b>Port Details</b>",
            styles["Heading2"]
        )
    )

    for port in open_ports:

        info = get_service(port)

        elements.append(
            Paragraph(
                f"<b>Port {port}</b>",
                styles["Heading3"]
            )
        )

        details = [

            ["Service", info["service"]],

            ["Protocol", info["protocol"]],

            ["Category", info["category"]],

            ["Risk", info["risk"]],

            ["Description", info["description"]]

        ]

        details_table = Table(
            details,
            colWidths=[1.7 * inch, 4.6 * inch]
        )

        details_table.setStyle(TableStyle([

            ("BACKGROUND", (0, 0), (0, -1), colors.lightgrey),

            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),

            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),

            ("TOPPADDING", (0, 0), (-1, -1), 6),

            ("VALIGN", (0, 0), (-1, -1), "TOP")

        ]))

        elements.append(details_table)

        elements.append(Spacer(1, 0.12 * inch))

        elements.append(
            Paragraph(
                "<b>Recommendations</b>",
                styles["Heading4"]
            )
        )

        recommendations = get_recommendations(port)

        if recommendations:

            for recommendation in recommendations:

                elements.append(
                    Paragraph(
                        f"• {recommendation}",
                        styles["BodyText"]
                    )
                )

        else:

            elements.append(
                Paragraph(
                    "No recommendations available.",
                    styles["BodyText"]
                )
            )

        elements.append(Spacer(1, 0.20 * inch))

    # ==========================================================
    # SECURITY SUMMARY
    # ==========================================================

    elements.append(
        Paragraph(
            "<b>Security Summary</b>",
            styles["Heading2"]
        )
    )

    summary = f"""
    <b>Overall Exposure Score:</b> {exposure_score}/100<br/><br/>

    <b>Overall Risk Level:</b> {risk_level}<br/><br/>

    <b>Security Grade:</b> {security_grade}<br/><br/>

    <b>Total Open Ports:</b> {len(open_ports)}<br/><br/>

    This report was generated by the
    <b>Intelligent Network Exposure Assessment Tool (INEAT)</b>.

    Review all HIGH and CRITICAL risk services immediately.
    Close unnecessary ports and keep all exposed services updated.
    """

    elements.append(
        Paragraph(
            summary,
            styles["BodyText"]
        )
    )

    elements.append(Spacer(1, 0.25 * inch))

    doc.build(elements)

    print(f"\nPDF Report Generated : {filename}")
