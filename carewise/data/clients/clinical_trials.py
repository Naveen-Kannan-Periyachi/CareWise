"""ClinicalTrials.gov API Client"""

import requests
from config.settings import CLINICAL_TRIALS_URL


def query_clinical_trials(query, limit=10):
    """Query ClinicalTrials.gov v2 API"""
    params = {
        "query.term": query,
        "pageSize": limit,
        "format": "json"
    }
    r = requests.get(CLINICAL_TRIALS_URL, params=params, timeout=30)
    r.raise_for_status()

    studies = r.json().get("studies", [])
    results = []

    for study in studies:
        protocol = study.get("protocolSection", {})
        id_module = protocol.get("identificationModule", {})
        status_module = protocol.get("statusModule", {})
        conditions_module = protocol.get("conditionsModule", {})
        design_module = protocol.get("designModule", {})
        
        results.append({
            "id": id_module.get("nctId", ""),
            "title": id_module.get("briefTitle", ""),
            "condition": conditions_module.get("conditions", []),
            "phase": design_module.get("phases", []),
            "status": status_module.get("overallStatus", ""),
            "source": "ClinicalTrials"
        })

    return results
