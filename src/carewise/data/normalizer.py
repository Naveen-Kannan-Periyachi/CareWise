"""Result Normalizer - Transforms multi-source data into unified format"""


def normalize_pubmed(item):
    """Normalize PubMed article to unified format"""
    content = item.get("summary") or "No abstract available"
    
    return {
        "id": f"PMID-{item.get('title', 'Unknown')[:20]}",
        "title": item.get("title") or "No title",
        "content": content,
        "source": "PubMed",
        "metadata": {
            "year": item.get("year"),
            "type": "research_article"
        }
    }


def normalize_clinical_trial(item):
    """Normalize ClinicalTrials record to unified format"""
    # Combine conditions and status into readable content
    conditions = ", ".join(item.get("condition", []))
    status = item.get("status", "Unknown")
    phase = ", ".join(item.get("phase", [])) if item.get("phase") else "Not specified"
    
    content = f"Conditions: {conditions}\nStatus: {status}\nPhase: {phase}"
    
    return {
        "id": item.get("id", "Unknown"),
        "title": item.get("title", "No title"),
        "content": content,
        "source": "ClinicalTrials",
        "metadata": {
            "nct_id": item.get("id"),
            "status": status,
            "phase": phase,
            "conditions": item.get("condition", [])
        }
    }


def normalize_fda(item):
    """Normalize FDA drug label to unified format"""
    drug = item.get("drug", "Unknown Drug")
    
    # Combine warnings and adverse reactions into content
    content_parts = []
    
    warnings = item.get("warnings", "N/A")
    if warnings and warnings != "N/A":
        content_parts.append(f"WARNINGS:\n{warnings[:500]}")
    
    adverse = item.get("adverse_reactions", "N/A")
    if adverse and adverse != "N/A":
        content_parts.append(f"ADVERSE REACTIONS:\n{adverse[:500]}")
    
    if not content_parts:
        content = "No safety information available"
    else:
        content = "\n\n".join(content_parts)
    
    return {
        "id": drug,
        "title": f"{drug} - Drug Safety Information",
        "content": content,
        "source": "FDA",
        "metadata": {
            "drug_name": drug,
            "purpose": item.get("purpose", "N/A"),
            "type": "drug_label"
        }
    }


def normalize_results(raw_results):
    """
    Normalize results from all sources into unified format.
    
    Args:
        raw_results: Dict with keys 'pubmed', 'clinical_trials', 'fda'
        
    Returns:
        List of normalized evidence items
    """
    normalized = []
    
    # Normalize PubMed articles
    for item in raw_results.get("pubmed", []):
        normalized.append(normalize_pubmed(item))
    
    # Normalize Clinical Trials
    for item in raw_results.get("clinical_trials", []):
        normalized.append(normalize_clinical_trial(item))
    
    # Normalize FDA records
    for item in raw_results.get("fda", []):
        normalized.append(normalize_fda(item))
    
    return normalized

