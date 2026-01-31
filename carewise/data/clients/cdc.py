"""CDC API Client"""

import requests
from config.settings import CDC_URL


def query_cdc(topic, limit=10):
    """Query CDC public health database"""
    params = {
        "$limit": limit
    }

    try:
        res = requests.get(CDC_URL, params=params, timeout=10)
        res.raise_for_status()

        data = res.json()
        
        # Filter by topic if available
        filtered = [item for item in data if topic.lower() in str(item).lower()]

        results = [
            {
                "source": "CDC",
                "title": item.get("title", "No title"),
                "description": item.get("short_description", "No description")
            }
            for item in (filtered if filtered else data)
        ]
        
        return results
    except Exception as e:
        print(f"CDC API error: {e}")
        return []
