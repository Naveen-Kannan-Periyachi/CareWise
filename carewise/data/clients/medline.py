"""MedlinePlus API Client"""

import requests
import xml.etree.ElementTree as ET
from config.settings import MEDLINEPLUS_URL


def query_medlineplus(term, limit=10):
    """Query MedlinePlus health topics database"""
    params = {
        "db": "healthTopics",
        "term": term,
        "retmax": limit
    }

    try:
        res = requests.get(MEDLINEPLUS_URL, params=params, timeout=10)
        res.raise_for_status()

        root = ET.fromstring(res.text)
        results = []
        
        for doc in root.findall(".//document"):
            title_elem = doc.find(".//content[@name='title']")
            summary_elem = doc.find(".//content[@name='FullSummary']")
            
            title = title_elem.text if title_elem is not None else "No title"
            summary = summary_elem.text if summary_elem is not None else "No summary"

            results.append({
                "source": "MedlinePlus",
                "title": title,
                "summary": summary
            })

        return results
    except Exception as e:
        print(f"MedlinePlus API error: {e}")
        return []
