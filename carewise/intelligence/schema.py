"""Schema definitions for unified query intelligence module"""

# All supported intents (biomedical + general health)
ALLOWED_INTENTS = {
    # Biomedical research intents
    "LITERATURE_REVIEW",
    "CLINICAL_TRIALS",
    "DRUG_SAFETY",
    "COMPARATIVE_RESEARCH",
    "DATA_ANALYSIS",
    # General health intents
    "SYMPTOMS_RELATED",
    "INFORMATIONAL",
    "GENERAL_HEALTH"
}

# All supported data sources
ALLOWED_SOURCES = {
    # Biomedical sources
    "PubMed",
    "ClinicalTrials",
    "FDA",
    # General health sources
    "MedlinePlus",
    "CDC",
    "WHO"
}
