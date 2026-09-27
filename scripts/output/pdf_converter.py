import argparse

import json
import reportlab as rl
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
    
def convert_to_pdf(data: dict, output_file: str) -> None:
    """
    Converts the given data to a PDF file.

    Args:
        data (dict): The data to be converted to PDF.
        output_file (str): The path to the output PDF file.
    """

    c = canvas.Canvas(output_file, pagesize=letter)
    width, height = letter

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

    data = json.load(open(args.input, "r"))

    convert_to_pdf(data, args.output)
if __name__ == "__main__":
    main()