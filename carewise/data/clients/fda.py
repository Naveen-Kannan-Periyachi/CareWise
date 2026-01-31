"""FDA openFDA API Client"""

import requests
from config.settings import FDA_API_KEY, FDA_LABEL_URL


def query_fda_drug(drug_name, limit=5):
    """Query FDA drug label database"""
    # Try brand name first
    params = {
        "search": f'openfda.brand_name:"{drug_name}"',
        "limit": limit,
        "api_key": FDA_API_KEY
    }
    r = requests.get(FDA_LABEL_URL, params=params, timeout=30)
    
    # If brand name fails, try generic name
    if r.status_code == 404:
        params["search"] = f'openfda.generic_name:"{drug_name}"'
        r = requests.get(FDA_LABEL_URL, params=params, timeout=30)
    
    r.raise_for_status()
    results = r.json().get("results", [])

    formatted = []
    for item in results:
        formatted.append({
            "drug": drug_name,
            "purpose": item.get("purpose", [""])[0] if item.get("purpose") else "N/A",
            "warnings": item.get("warnings", [""])[0] if item.get("warnings") else "N/A",
            "adverse_reactions": item.get("adverse_reactions", [""])[0] if item.get("adverse_reactions") else "N/A",
            "source": "FDA"
        })

    return formatted
