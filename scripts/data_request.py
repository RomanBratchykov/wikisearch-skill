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
    articles: list[str],
    start_date: str,
    end_date: str,
    granularity: str = "monthly",
    access_token: str = "all-access",
)-> dict:
    results = {}
    
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
        "minimum_views": int(views.min()),
        "maximum_views": int(views.max()),
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
    
def analyze_data(data: dict) -> dict:
    dataframe = prepare_data(data)

    return {
        "statistics": calculate_statistics(dataframe),
        "anomalies": detect_anomalies(dataframe),
        "time_series": dataframe[["date", "views"]].to_dict("records"),
    }
    
def save_to_json(data: dict, output_file: str = "output.json") -> None:
    with open(output_file, "w") as f:
        json.dump(data, f, indent=4)

