import json
import matplotlib.pyplot as plt
import argparse

def build_graph(json_data: str, title: str, xlabel: str, ylabel: str, output_file: str) -> None:
    """
    Builds a graph from the given data and saves it to a file.

    Args:
        json_data (str): Path to the JSON file containing data.
        title (str): The title of the graph.
        xlabel (str): The label for the x-axis.
        ylabel (str): The label for the y-axis.
        output_file (str): The path to the output file where the graph will be saved.
    """

    with open(json_data, "r") as f:
        data = json.load(f)

    # Check if the data is in our comparison format (has 'languages' key)
    if "languages" in data:
        # Extract languages and total views for a bar chart
        languages = list(data["languages"].keys())
        total_views = [data["languages"][lang]["total_views"] for lang in languages]

        plt.figure(figsize=(10, 6))
        plt.bar(languages, total_views, color='skyblue')
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.tight_layout()
    else:
        # Original time series format
        # Fix the typo: use "time_series" (not "times_series")
        timeseries = data.get("time_series", [])
        if not timeseries:
            # Fallback to the typo key if present (for backward compatibility with buggy data)
            timeseries = data.get("times_series", [])

        dates = [entry["date"] for entry in timeseries]
        views = [entry["views"] for entry in timeseries]

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

    build_graph(args.input, args.title, args.xlabel, args.ylabel, args.output)
    print(f"Graph saved to {args.output}")

if __name__ == "__main__":
    main()