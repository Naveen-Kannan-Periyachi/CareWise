"""Unified Result Normalizer - Transforms all 6 data sources into unified format"""

import re


def strip_html_tags(text):
    """Remove HTML tags and clean up text"""
    if not text:
        return text
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    # Clean up extra whitespace
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def normalize_pubmed(item):
    """Normalize PubMed article to unified format"""
    raw_title = item.get("title") or "No title"
    raw_content = item.get("summary") or "No abstract available"
    
    clean_title = strip_html_tags(raw_title)
    clean_content = strip_html_tags(raw_content)
    
    return {
        "id": f"PMID-{clean_title[:20]}",
        "title": clean_title,
        "content": clean_content,
        "source": "PubMed",
        "metadata": {
            "year": item.get("year"),
            "type": "research_article"
        }
    }


def normalize_clinical_trial(item):
    """Normalize ClinicalTrials record to unified format"""
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


def normalize_medlineplus(item):
    """Normalize MedlinePlus health topic to unified format"""
    raw_title = item.get("title") or "No title"
    raw_content = item.get("summary") or "No summary available"
    
    # Clean HTML tags from title and content
    clean_title = strip_html_tags(raw_title)
    clean_content = strip_html_tags(raw_content)
    
    return {
        "id": f"MLP-{clean_title[:20]}",
        "title": clean_title,
        "content": clean_content,
        "source": "MedlinePlus",
        "metadata": {
            "type": "health_topic"
        }
    }


def normalize_cdc(item):
    """Normalize CDC record to unified format"""
    raw_title = item.get("title") or "No title"
    raw_content = item.get("description") or "No description available"
    
    clean_title = strip_html_tags(raw_title)
    clean_content = strip_html_tags(raw_content)
    
    return {
        "id": f"CDC-{clean_title[:20]}",
        "title": clean_title,
        "content": clean_content,
        "source": "CDC",
        "metadata": {
            "type": "public_health"
        }
    }


def normalize_who(item):
    """Normalize WHO data to unified format"""
    indicator = item.get("indicator", "Unknown")
    topic = item.get("topic", "Unknown")
    country = item.get("country", "Global")
    year = item.get("year", "N/A")
    value = item.get("value", "N/A")
    
    title = f"{topic.title()} - {country} ({year})"
    content = f"Indicator: {indicator}\nCountry: {country}\nYear: {year}\nValue: {value}"
    
    return {
        "id": f"WHO-{indicator}-{country}-{year}",
        "title": title,
        "content": content,
        "source": "WHO",
        "metadata": {
            "indicator": indicator,
            "country": country,
            "year": year,
            "value": value,
            "type": "health_statistic"
        }
    }


def normalize_results(raw_results):
    """
    Normalize results from all sources into unified format.
    
    Args:
        raw_results: Dict with keys for each source
        
    Returns:
        List of normalized evidence items
    """
    normalized = []
    
    # Biomedical sources
    for item in raw_results.get("pubmed", []):
        normalized.append(normalize_pubmed(item))
    
    for item in raw_results.get("clinical_trials", []):
        normalized.append(normalize_clinical_trial(item))
    
    for item in raw_results.get("fda", []):
        normalized.append(normalize_fda(item))
    
    # General health sources
    for item in raw_results.get("medlineplus", []):
        normalized.append(normalize_medlineplus(item))
    
    for item in raw_results.get("cdc", []):
        normalized.append(normalize_cdc(item))
    
    for item in raw_results.get("who", []):
        normalized.append(normalize_who(item))
    
    return normalized
