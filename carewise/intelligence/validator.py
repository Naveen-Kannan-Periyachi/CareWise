"""Validator for execution plans"""

from .schema import ALLOWED_INTENTS, ALLOWED_SOURCES

# Define intent groups and their allowed sources
BIOMEDICAL_INTENTS = {
    "LITERATURE_REVIEW",
    "CLINICAL_TRIALS",
    "DRUG_SAFETY",
    "COMPARATIVE_RESEARCH",
    "DATA_ANALYSIS"
}

GENERAL_HEALTH_INTENTS = {
    "SYMPTOMS_RELATED",
    "INFORMATIONAL",
    "GENERAL_HEALTH"
}

BIOMEDICAL_SOURCES = {"PubMed", "ClinicalTrials", "FDA"}
GENERAL_HEALTH_SOURCES = {"MedlinePlus", "CDC", "WHO"}


def validate_execution_plan(plan: dict) -> tuple[bool, str]:
    """Validate an execution plan against the unified schema with strict source separation"""
    if not isinstance(plan, dict):
        return False, "Plan is not a JSON object"

    if "intent" not in plan or plan["intent"] not in ALLOWED_INTENTS:
        return False, f"Invalid or missing intent. Must be one of: {ALLOWED_INTENTS}"

    if "entities" not in plan or not isinstance(plan["entities"], dict):
        return False, "Missing or invalid entities"

    # Check all entity fields
    for key in ["diseases", "drugs", "therapies", "symptoms", "topics"]:
        if key not in plan["entities"] or not isinstance(plan["entities"][key], list):
            return False, f"Invalid entities field: {key}"

    if "sources" not in plan or not isinstance(plan["sources"], list):
        return False, "Missing or invalid sources"

    for src in plan["sources"]:
        if src not in ALLOWED_SOURCES:
            return False, f"Invalid source: {src}. Must be one of: {ALLOWED_SOURCES}"

    # CRITICAL: Enforce strict source separation based on intent
    intent = plan["intent"]
    sources = set(plan["sources"])
    
    if intent in BIOMEDICAL_INTENTS:
        # Biomedical intents can ONLY use biomedical sources
        if not sources.issubset(BIOMEDICAL_SOURCES):
            invalid = sources - BIOMEDICAL_SOURCES
            return False, f"Biomedical intent '{intent}' cannot use general health sources: {invalid}. Use only: {BIOMEDICAL_SOURCES}"
    
    elif intent in GENERAL_HEALTH_INTENTS:
        # General health intents can ONLY use general health sources
        if not sources.issubset(GENERAL_HEALTH_SOURCES):
            invalid = sources - GENERAL_HEALTH_SOURCES
            return False, f"General health intent '{intent}' cannot use biomedical sources: {invalid}. Use only: {GENERAL_HEALTH_SOURCES}"

    if "analysis_required" not in plan or not isinstance(plan["analysis_required"], bool):
        return False, "Invalid analysis_required flag"

    return True, ""

