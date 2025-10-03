import os
import requests
from datetime import datetime, timedelta
from backend.app.models.document import Document

BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")
BASE_URL = "https://api.twitter.com/2/tweets/search/recent"

def fetch_recent_tweets(query: str, max_results: int = 100):
    headers = {
        "Authorization": f"Bearer {BEARER_TOKEN}",
        "Content-Type": "application/json"
    }

    end_time = datetime.now()
    start_time = end_time - timedelta(days=7)

    params = {
        "query": query,
        "max_results": min(max_results, 100),
        "tweet.fields": "id,text,author_id,created_at,public_metrics",
        "start_time": start_time.isoformat("T") + "Z",
        "end_time": end_time.isoformat("T") + "Z"
    }

    resp = requests.get(BASE_URL, headers=headers, params=params)
    resp.raise_for_status()
    data = resp.json().get("data", [])

    documents = []
    for t in data:
        documents.append(
            Document(
                id=t["id"],
                text=t["text"],
                author=t["author_id"],
                platform="X",
                timestamp=t["created_at"],
                engagement=t.get("public_metrics", {})
            )
        )
    return documents
