import argparse
import json
import reportlab as rl
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle

def convert_to_pdf(json_data: str, output_file: str) -> None:
    """
    Converts the given data to a PDF file.

    Args:
        json_data (str): Path to the JSON file containing data.
        output_file (str): The path to the output PDF file.
    """
    with open(json_data, "r") as f:
        data = json.load(f)

    c = canvas.Canvas(output_file, pagesize=letter)
    width, height = letter

    # Check if the data is in our comparison format (has 'languages' key)
    if "languages" in data:
        # Title
        c.setFont("Helvetica-Bold", 16)
        c.drawString(100, height - 50, "Wikipedia Pageviews Analysis for Anthropic")

        # Prepare table data for languages
        table_data = [["Language", "Total Views", "Avg Views", "Growth %", "Peak Views", "Peak Date"]]
        for lang, stats in data["languages"].items():
            table_data.append([
                lang,
                f"{stats['total_views']:,}",
                f"{stats['average_views']:.1f}",
                f"{stats['growth_percent']:.1f}%",
                f"{stats['max_views']:,}",
                stats['peak']['date']
            ])

        # Create table
        table = Table(table_data, colWidths=[60, 80, 80, 60, 80, 80])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))

        # Draw table
        table_width, table_height = table.wrap(0, 0)
        table.drawOn(c, 100, height - 150 - table_height)

        # Comparison metrics
        c.setFont("Helvetica-Bold", 12)
        c.drawString(100, height - 200 - table_height, "Comparison Metrics:")
        c.setFont("Helvetica", 10)
        comp = data["comparison"]
        text = f"Highest Total Views: {comp['highest_total_views']} | Lowest Total Views: {comp['lowest_total_views']} | "
        text += f"Highest Growth: {comp['highest_growth']} | Lowest Growth: {comp['lowest_growth']}"
        c.drawString(100, height - 220 - table_height, text)

        # Insights
        c.setFont("Helvetica-Bold", 12)
        c.drawString(100, height - 250 - table_height, "Insights:")
        c.setFont("Helvetica", 10)
        insight_y = height - 270 - table_height
        for insight in data["insights"]:
            c.drawString(120, insight_y, f"- {insight}")
            insight_y -= 15

    else:
        # Original format (for backward compatibility)
        # Expects keys: statistics and anomalies
        c.setFont("Helvetica-Bold", 16)
        c.drawString(100, height - 50, "Wikipedia Pageviews Analysis")

        c.setFont("Helvetica", 12)
        c.drawString(100, height - 100, f"Total Views: {data['statistics']['total_views']}")
        c.drawString(100, height - 120, f"Average Views: {data['statistics']['average_views']:.2f}")
        c.drawString(100, height - 140, f"Max Views: {data['statistics']['max_views']}")
        c.drawString(100, height - 160, f"Min Views: {data['statistics']['min_views']}")

        c.setFont("Helvetica-Bold", 14)
        c.drawString(100, height - 200, "Anomalies Detected:")

        y_position = height - 220
        for anomaly in data['anomalies']:
            c.setFont("Helvetica", 12)
            c.drawString(120, y_position, f"Date: {anomaly['date']}, Views: {anomaly['views']}")
            y_position -= 20

    c.save()

def main():
    parser = argparse.ArgumentParser(description="Convert Wikipedia pageview data to PDF")
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)

    args = parser.parse_args()

    convert_to_pdf(args.input, args.output)

if __name__ == "__main__":
    main()