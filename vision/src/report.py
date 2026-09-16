from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
)
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch


class TrafficReport:

    def generate(self, output_pdf, stats):

        doc = SimpleDocTemplate(output_pdf)

        styles = getSampleStyleSheet()

        elements = []

        elements.append(
            Paragraph(
                "<b>ORBITAL AI — Traffic Intelligence Report</b>",
                styles["Title"]
            )
        )

        elements.append(
            Paragraph(
                "Generated automatically after mission completion.",
                styles["Normal"]
            )
        )

        elements.append(Paragraph("<br/>", styles["Normal"]))

        data = [
            ["Metric", "Value"],
            ["Total Vehicles", str(stats["total"])],
            ["Average Speed", f"{stats['avg_speed']} km/h"],
            ["Visible Vehicles", str(stats["visible"])],
            ["Congestion", stats["congestion"]],
            ["Lane 1", str(stats["lanes"][1])],
            ["Lane 2", str(stats["lanes"][2])],
            ["Lane 3", str(stats["lanes"][3])],
            ["Lane 4", str(stats["lanes"][4])],
        ]

        table = Table(data, colWidths=[2.8 * inch, 2.2 * inch])

        table.setStyle(
            TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0F172A")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#F8FAFC")),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 10),
            ])
        )

        elements.append(table)

        elements.append(Paragraph("<br/>", styles["Normal"]))

        elements.append(
            Paragraph(
                "<b>Executive Summary</b>",
                styles["Heading2"]
            )
        )

        elements.append(
            Paragraph(
                f"""
                ORBITAL detected <b>{stats['total']}</b> vehicles with an
                estimated average speed of <b>{stats['avg_speed']} km/h</b>.
                Congestion level during the mission was
                <b>{stats['congestion']}</b>.
                """,
                styles["BodyText"]
            )
        )

        doc.build(elements)