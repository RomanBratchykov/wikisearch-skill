import json

import requests
import pandas as pd
from urllib.parse import quote

import argparse

def get_language_articles(
    title: str,
    languages: list[str],
) -> dict[str, str]:
    encoded_title = quote(title, safe="")
    
    url = (
        f"https://en.wikipedia.org/w/rest.php/v1/"
        f"page/{encoded_title}/links/language"
    )
    
    headers = {
        "User-Agent": (
            "wikisearch-skill/1.0 "
            "(https://github.com/RomanBratchykov/wikisearch-skill)"
        )
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()

    data = response.json()

    articles = {}

    for item in data:
        if item["code"] in languages:
            articles[item["code"]] = item["title"]

    return articles

def fetch_data_page(
    languages: list[str],
    article: str,
    start_date: str,
    end_date: str,
    granularity: str = "monthly",
    access_token: str = "all-access",
)-> dict:
    results = {}
    articles = get_language_articles(article, languages)
    headers = {"User-Agent": "wikisearch-skill/1.0 (https://github.com/RomanBratchykov/wikisearch-skill)"}
    for lang in languages:
        for article in articles:
            url = ""
            url += (
                f"https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/"
                #project
                f"{lang}.wikipedia.org"
                #access token
                f"/{access_token}/"
                #agent
                f"user/"
                #article
                f"{article}/"
                #granularity
                f"{granularity}/"
                #start date
                f"{start_date}/"
                #end date
                f"{end_date}"
            )     
            print(url)      
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                results[f"{lang}_{article}"] = response.json()
            else:
                results[f"{lang}_{article}"] = {"error": response.status_code, "message": response.text}
    save_to_json(results, "pageviews.json")
    return results

def prepare_data(data: dict) -> dict:
    analyzed_results = pd.DataFrame(data["items"])
    analyzed_results["date"] = pd.to_datetime(analyzed_results["timestamp"], format="%Y%m%d%H")
    return analyzed_results

def calculate_statistics(dataframe: pd.DataFrame) -> dict:
    views = dataframe["views"]

    first_period = views.iloc[:24].mean()
    last_period = views.iloc[-24:].mean()

    return {
        "observations": len(dataframe),
        "total_views": int(views.sum()),
        "average_views": float(views.mean()),
        "median_views": float(views.median()),
        "min_views": int(views.min()),
        "max_views": int(views.max()),
        "std_views": float(views.std()),
        "volatility": float(views.std() / views.mean()),
        "growth_percent": float(
            (last_period - first_period) / first_period * 100
        ),
        "peak": {
            "date": dataframe.loc[views.idxmax(), "date"].isoformat(),
            "views": int(views.max()),
        },
        "missing_values": int(dataframe["views"].isna().sum()),
    }
    
def detect_anomalies(dataframe: pd.DataFrame) -> list[dict]:
    views = dataframe["views"]

    z_score = (views - views.mean()) / views.std()

    anomalies = dataframe[z_score.abs() > 3]

    return [
        {
            "date": row["date"].isoformat(),
            "views": int(row["views"]),
        }
        for _, row in anomalies.iterrows()
    ]
    
def analyze_data(data: dict) -> None:
    results = {}
    for key, article_data in data.items():
        dataframe = prepare_data(article_data)
        
        results[key] = {
        "statistics": calculate_statistics(dataframe),
        "anomalies": detect_anomalies(dataframe),
        "time_series": dataframe[["date", "views"]].to_dict("records"),
        }
    save_to_json(results, "analysis.json")
    
def save_to_json(data: dict, output_file: str = "output.json") -> None:
    with open(output_file, "w") as f:
        json.dump(data, f, indent=4)

def main():
    parser = argparse.ArgumentParser(
        description="Wikipedia pageview analysis"
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    resolve_parser = subparsers.add_parser("resolve")
    resolve_parser.add_argument("--title", required=True)
    resolve_parser.add_argument("--languages", nargs="+", required=True)

    fetch_parser = subparsers.add_parser("fetch")
    fetch_parser.add_argument("--languages", nargs="+", required=True)
    fetch_parser.add_argument("--articles", nargs="+", required=True)
    fetch_parser.add_argument("--start", required=True)
    fetch_parser.add_argument("--end", required=True)
    fetch_parser.add_argument("--granularity", default="monthly")
    fetch_parser.add_argument("--output", default="pageviews.json")
    
    analyze_parser = subparsers.add_parser("analyze")
    analyze_parser.add_argument("--input", required=True)
    analyze_parser.add_argument("--output", default="analysis.json")
    args = parser.parse_args()

    if args.command == "resolve":
        result = get_language_articles(
            args.title,
            args.languages,
        )
        print(json.dumps(result, indent=4, ensure_ascii=False))

    elif args.command == "fetch":
        result = fetch_data_page(
            args.languages,
            args.articles,
            args.start,
            args.end, 
            args.granularity,
        )
        save_to_json(result, args.output)
        print(f"Saved to {args.output}")
    elif args.command == "analyze":
        with open(args.input, "r") as f:
            data = json.load(f)
        result = analyze_data(data)
        save_to_json(result, args.output)
        print(f"Saved to {args.output}")


if __name__ == "__main__":
    main()