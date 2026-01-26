"""PubMed API Client"""

import requests
import xml.etree.ElementTree as ET
from carewise.config import PUBMED_API_KEY, PUBMED_ESEARCH_URL, PUBMED_EFETCH_URL


def search_pubmed(query, limit=10):
    """Search PubMed for article IDs"""
    params = {
        "db": "pubmed",
        "term": query,
        "retmax": limit,
        "retmode": "json",
        "api_key": PUBMED_API_KEY
    }
    r = requests.get(PUBMED_ESEARCH_URL, params=params, timeout=30)
    r.raise_for_status()
    return r.json()["esearchresult"]["idlist"]


def fetch_pubmed_details(pmids):
    """Fetch full article details from PubMed"""
    if not pmids:
        return []

    params = {
        "db": "pubmed",
        "id": ",".join(pmids),
        "retmode": "xml",
        "api_key": PUBMED_API_KEY
    }
    r = requests.get(PUBMED_EFETCH_URL, params=params, timeout=30)
    r.raise_for_status()

    root = ET.fromstring(r.text)
    articles = []

    for article in root.findall(".//PubmedArticle"):
        articles.append({
            "title": article.findtext(".//ArticleTitle"),
            "summary": article.findtext(".//Abstract/AbstractText"),
            "year": article.findtext(".//PubDate/Year"),
            "source": "PubMed"
        })

    return articles


def query_pubmed(search_term):
    """Query PubMed: search and fetch details"""
    pmids = search_pubmed(search_term)
    return fetch_pubmed_details(pmids)
