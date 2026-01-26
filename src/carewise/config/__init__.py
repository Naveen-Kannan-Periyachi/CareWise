"""Configuration Module"""

from .settings import (
    PUBMED_API_KEY,
    FDA_API_KEY,
    PUBMED_ESEARCH_URL,
    PUBMED_EFETCH_URL,
    CLINICAL_TRIALS_URL,
    FDA_LABEL_URL
)

__all__ = [
    "PUBMED_API_KEY",
    "FDA_API_KEY",
    "PUBMED_ESEARCH_URL",
    "PUBMED_EFETCH_URL",
    "CLINICAL_TRIALS_URL",
    "FDA_LABEL_URL"
]
