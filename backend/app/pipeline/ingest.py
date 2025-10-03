from backend.app.pipeline.connectors.x_api import fetch_recent_tweets

def ingest_maritime_news():
    query = "maritime OR shipping OR tanker OR LNG"
    tweets = fetch_recent_tweets(query=query, max_results=50)
    return tweets
