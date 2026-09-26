import requests

def fetch_data_page(
    languages: list[str],
    articles: list[str],
    start_date: str,
    end_date: str,
    granularity: str = "daily",
    access_token: str = "all-access",
)-> dict:
    url = "https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/"
    results = {}
    for lang in languages:
        for article in articles:
            url += (
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
            response = requests.get(url)
            if response.status_code == 200:
                results[f"{lang}_{article}"] = response.json()
            else:
                results[f"{lang}_{article}"] = {"error": response.status_code, "message": response.text}
    return results

def analyze_data(data:dict) -> dict:
    analyzed_results = {}
    
    return analyzed_results

if __name__ == "__main__":
    languages = ["en"]
    articles = ["Python_(programming_language)", "Artificial_intelligence"]
    start_date = "20220101"
    end_date = "20220131"
    
    data = fetch_data_page(languages, articles, start_date, end_date)
    print(data)