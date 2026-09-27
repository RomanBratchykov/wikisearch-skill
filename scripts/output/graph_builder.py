from flask import json
import matplotlib.pyplot as plt
import argparse

def build_graph(data: dict, title: str, xlabel: str, ylabel: str, output_file: str) -> None:
    """
    Builds a graph from the given data and saves it to a file.

    Args:
        data (dict): The data to be plotted.
        title (str): The title of the graph.
        xlabel (str): The label for the x-axis.
        ylabel (str): The label for the y-axis.
        output_file (str): The path to the output file where the graph will be saved.
    """

    dates = [entry["date"] for entry in data["time_series"]]
    views = [entry["views"] for entry in data["time_series"]]

    plt.figure(figsize=(10, 5))
    plt.plot(dates, views, marker='o', linestyle='-', color='b')
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xticks(rotation=45)
    plt.tight_layout()

    plt.savefig(output_file)
    plt.close()
    
def main():
    parser = argparse.ArgumentParser(description="Graph Builder")
    parser.add_argument("--input", required=True, help="Input JSON file containing data")
    parser.add_argument("--output", required=True, help="Output file for the graph (e.g., graph.png)")
    parser.add_argument("--title", default="Wikipedia Pageviews Over Time", help="Title of the graph")
    parser.add_argument("--xlabel", default="Date", help="Label for the x-axis")
    parser.add_argument("--ylabel", default="Views", help="Label for the y-axis")

    args = parser.parse_args()

    with open(args.input, "r") as f:
        data = json.load(f)

    build_graph(data, args.title, args.xlabel, args.ylabel, args.output)
    print(f"Graph saved to {args.output}")
    
if __name__ == "__main__":
    main()
    