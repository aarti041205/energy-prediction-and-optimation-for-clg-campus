from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

def generate_pdf(report, filename="energy_report.pdf"):

    doc = SimpleDocTemplate(filename)
    styles = getSampleStyleSheet()

    story = []

    story.append(
        Paragraph("<b>Campus Energy AI Report</b>", styles["Heading1"])
    )

    story.append(
        Paragraph(report.replace("\n", "<br/>"), styles["BodyText"])
    )

    doc.build(story)

    return filename