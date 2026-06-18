from datetime import datetime
from typing import Optional

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch

from reports.report_generator import generate_text_report


def export_pdf_report(
    *,
    out_path: str,
    report_date: Optional[datetime] = None,
    analyst_name: str = "Analyst",
) -> None:
    """Export crisp text report into a PDF.

    NOTE: Current DB schema has no timestamp/date/action columns, so PDF will
    include placeholders for those fields.
    """

    text = generate_text_report(report_date=report_date, analyst_name=analyst_name)

    c = canvas.Canvas(out_path, pagesize=A4)
    width, height = A4

    x = 0.75 * inch
    y = height - 0.75 * inch
    line_height = 12

    for line in text.splitlines():
        if y < 0.75 * inch:
            c.showPage()
            y = height - 0.75 * inch
        c.drawString(x, y, line)
        y -= line_height

    c.setTitle("CyberSentinel EDR Report")
    c.save()


if __name__ == "__main__":
    # Example usage:
    # pip install reportlab
    export_pdf_report(
        out_path="reports/report_today.pdf",
        report_date=datetime.now(),
        analyst_name="Analyst",
    )

