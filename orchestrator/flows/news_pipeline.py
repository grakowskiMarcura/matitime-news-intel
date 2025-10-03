# orchestrator/flows/news_pipeline.py
from prefect import flow, task
from backend.app.pipeline.ingest import ingest_maritime_news
from backend.app.pipeline.preprocess import preprocess_documents
from backend.app.pipeline.classify import classify_documents
from backend.app.pipeline.rank import rank_documents
from backend.app.pipeline.store import store_documents

@flow(name="Maritime News Pipeline")
def news_pipeline_flow():
    docs = ingest_maritime_news()
    docs = preprocess_documents(docs)
    docs = classify_documents(docs)
    docs = rank_documents(docs)
    store_documents(docs)

if __name__ == "__main__":
    news_pipeline_flow()
