
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.barcharts import VerticalBarChart

def generate_report(filename="sales_report.pdf", title="Monthly Sales Report", data=None):
    """
    Generates a professional PDF sales report using ReportLab.

    Args:
        filename (str): The name of the output PDF file.
        title (str): The main title of the report.
        data (list of dict): A list of dictionaries, each representing a sales record.
                              Example: [{'month': 'Jan', 'sales': 1000, 'profit': 200}]
    """
    doc = SimpleDocTemplate(filename, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    # Custom styles
    h1_style = styles['h1']
    h1_style.alignment = 1  # Center alignment
    h1_style.spaceAfter = 0.2 * inch

    h2_style = styles['h2']
    h2_style.alignment = 0  # Left alignment
    h2_style.spaceBefore = 0.3 * inch
    h2_style.spaceAfter = 0.1 * inch

    normal_style = styles['Normal']
    normal_style.spaceAfter = 0.1 * inch

    # --- Title Page ---
    story.append(Paragraph(title, h1_style))
    story.append(Spacer(1, 0.5 * inch))
    story.append(Paragraph("Prepared by: Manus AI", normal_style))
    story.append(Paragraph("Date: March 11, 2026", normal_style))
    story.append(Spacer(1, 1 * inch))

    # Add a placeholder image (replace with actual logo if available)
    # try:
    #     logo = Image("logo.png")
    #     logo.width = 2 * inch
    #     logo.height = 1 * inch
    #     story.append(logo)
    #     story.append(Spacer(1, 0.5 * inch))
    # except FileNotFoundError:
    #     story.append(Paragraph("<i>[Company Logo Placeholder]</i>", normal_style))

    story.append(PageBreak())

    # --- Introduction ---
    story.append(Paragraph("1. Introduction", h2_style))
    story.append(Paragraph(
        "This report provides an overview of the monthly sales performance. "
        "It includes key metrics, a summary of sales data, and a visual representation of trends.",
        normal_style
    ))
    story.append(Spacer(1, 0.2 * inch))

    # --- Data Summary ---
    story.append(Paragraph("2. Sales Data Summary", h2_style))
    if data:
        total_sales = sum(item['sales'] for item in data)
        total_profit = sum(item['profit'] for item in data)
        story.append(Paragraph(f"Total Sales for the period: ${total_sales:,.2f}", normal_style))
        story.append(Paragraph(f"Total Profit for the period: ${total_profit:,.2f}", normal_style))
        story.append(Spacer(1, 0.2 * inch))

        story.append(Paragraph("Monthly Breakdown:", normal_style))
        for item in data:
            story.append(Paragraph(
                f"- {item['month']}: Sales = ${item['sales']:,.2f}, Profit = ${item['profit']:,.2f}",
                normal_style
            ))
    else:
        story.append(Paragraph("No sales data provided for this report.", normal_style))
    story.append(Spacer(1, 0.3 * inch))

    # --- Sales Chart ---
    story.append(Paragraph("3. Sales Performance Chart", h2_style))
    if data:
        drawing = Drawing(400, 200)
        chart = VerticalBarChart()
        chart.x = 50
        chart.y = 50
        chart.height = 125
        chart.width = 300
        chart.data = [tuple(item['sales'] for item in data)]
        chart.categoryAxis.labels.boxAnchor = 'ne'
        chart.categoryAxis.labels.dx = 8
        chart.categoryAxis.labels.dy = -2
        chart.categoryAxis.labels.angle = 30
        chart.categoryAxis.categoryNames = [item['month'] for item in data]
        chart.valueAxis.valueMin = 0
        chart.valueAxis.valueMax = max(item['sales'] for item in data) * 1.2
        chart.valueAxis.valueStep = max(item['sales'] for item in data) / 5
        chart.bars[0].fillColor = colors.blue
        drawing.add(chart)
        story.append(drawing)
    else:
        story.append(Paragraph("Cannot generate chart without sales data.", normal_style))
    story.append(Spacer(1, 0.3 * inch))

    # --- Conclusion ---
    story.append(Paragraph("4. Conclusion", h2_style))
    story.append(Paragraph(
        "The sales performance for the period has been analyzed. "
        "Further detailed analysis can be performed based on specific business requirements.",
        normal_style
    ))
    story.append(Spacer(1, 0.2 * inch))

    doc.build(story)

if __name__ == "__main__":
    sample_data = [
        {'month': 'January', 'sales': 1200, 'profit': 250},
        {'month': 'February', 'sales': 1500, 'profit': 300},
        {'month': 'March', 'sales': 1300, 'profit': 280},
        {'month': 'April', 'sales': 1800, 'profit': 350},
        {'month': 'May', 'sales': 1600, 'profit': 320},
    ]
    generate_report(data=sample_data)
    print("Report 'sales_report.pdf' generated successfully.")
