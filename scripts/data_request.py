import requests

def fetch_data_page(
    languages: list[str],
    articles: list[str],
    start_date: str,
    end_date: str,
    granularity: str = "daily",
    access_token: str = "all_access",
)-> dict:
    url = "https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article"
    results = {}
    for lang in languages:
        for article in articles:
            params = {
                "project": f"{lang}.wikipedia.org",
                "access": access_token,
                "agent": "user",
                "article": article,
                "granularity": granularity,
                "start": start_date,
                "end": end_date
            }
            response = requests.get(url, params=params)
            if response.status_code == 200:
                results[f"{lang}_{article}"] = response.json()
            else:
                results[f"{lang}_{article}"] = {"error": response.status_code, "message": response.text}
    return results

def analyze_data(data:dict) -> dict:
    analyzed_results = {}
    
    return analyzed_results