"""Data Acquisition Module - Biomedical API clients"""

from .router import execute_data_layer
from .ranker import rank_evidence

__all__ = ["execute_data_layer", "rank_evidence"]
