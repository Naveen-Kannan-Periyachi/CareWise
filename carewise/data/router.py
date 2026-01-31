"""Unified Data Router - Routes to all 6 data sources based on query plan"""

from .clients import (
    query_pubmed, query_clinical_trials, query_fda_drug,
    query_medlineplus, query_cdc, query_who
)
from .normalizer import normalize_results


def build_search_term(entities):
    """Build search term from extracted entities"""
    parts = []
    # Combine all entity types
    parts.extend(entities.get("diseases", []))
    parts.extend(entities.get("drugs", []))
    parts.extend(entities.get("therapies", []))
    parts.extend(entities.get("symptoms", []))
    parts.extend(entities.get("topics", []))
    return " ".join(parts) if parts else ""


def execute_data_layer(plan: dict):
    """
    Execute unified data layer based on plan from query intelligence.
    Handles both biomedical research and general health sources.
    """
    results = {}
    search_term = build_search_term(plan["entities"])
    entities = plan["entities"]

    for source in plan["sources"]:
        
        # Biomedical Research Sources
        if source == "PubMed":
            try:
                print(f"  📚 Fetching from PubMed...")
                results["pubmed"] = query_pubmed(search_term)
                print(f"     ✅ Found {len(results['pubmed'])} articles")
            except Exception as e:
                print(f"     ⚠️ PubMed failed: {str(e)[:100]}")
                results["pubmed"] = []

        elif source == "ClinicalTrials":
            try:
                print(f"  🏥 Fetching from ClinicalTrials...")
                results["clinical_trials"] = query_clinical_trials(search_term)
                print(f"     ✅ Found {len(results['clinical_trials'])} trials")
            except Exception as e:
                print(f"     ⚠️ ClinicalTrials failed: {str(e)[:100]}")
                results["clinical_trials"] = []

        elif source == "FDA":
            drugs = entities.get("drugs", [])
            if drugs:
                try:
                    print(f"  💊 Fetching from FDA for drug: {drugs[0]}...")
                    results["fda"] = query_fda_drug(drugs[0])
                    print(f"     ✅ Found {len(results['fda'])} FDA records")
                except Exception as e:
                    print(f"     ⚠️ FDA failed: {str(e)[:100]}")
                    results["fda"] = []
            else:
                print(f"  💊 Skipping FDA (no drugs specified in query)")
                results["fda"] = []
        
        # General Health Sources
        elif source == "MedlinePlus":
            try:
                print(f"  📖 Fetching from MedlinePlus...")
                results["medlineplus"] = query_medlineplus(search_term)
                print(f"     ✅ Found {len(results['medlineplus'])} health topics")
            except Exception as e:
                print(f"     ⚠️ MedlinePlus failed: {str(e)[:100]}")
                results["medlineplus"] = []

        elif source == "CDC":
            try:
                print(f"  🏛️ Fetching from CDC...")
                results["cdc"] = query_cdc(search_term)
                print(f"     ✅ Found {len(results['cdc'])} CDC records")
            except Exception as e:
                print(f"     ⚠️ CDC failed: {str(e)[:100]}")
                results["cdc"] = []

        elif source == "WHO":
            # WHO needs specific topics for indicator mapping
            topics = entities.get("topics", []) + entities.get("diseases", [])
            who_results = []
            for topic in topics:
                try:
                    print(f"  🌍 Fetching from WHO for topic: {topic}...")
                    topic_results = query_who(topic)
                    who_results.extend(topic_results)
                    if topic_results:
                        print(f"     ✅ Found {len(topic_results)} WHO data points")
                except Exception as e:
                    print(f"     ⚠️ WHO failed for '{topic}': {str(e)[:100]}")
            
            results["who"] = who_results

    return normalize_results(results)
