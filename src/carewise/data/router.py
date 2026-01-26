"""Data Router - Routes execution plans to appropriate APIs"""

from .clients import query_pubmed, query_clinical_trials, query_fda_drug
from .normalizer import normalize_results


def build_search_term(entities):
    """Build search term from extracted entities"""
    parts = []
    parts.extend(entities.get("diseases", []))
    parts.extend(entities.get("drugs", []))
    parts.extend(entities.get("therapies", []))
    return " ".join(parts)


def execute_data_layer(plan: dict):
    """Execute data layer based on plan from query intelligence"""
    results = {}
    search_term = build_search_term(plan["entities"])

    for source in plan["sources"]:
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
            drugs = plan["entities"].get("drugs", [])
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

    return normalize_results(results)
