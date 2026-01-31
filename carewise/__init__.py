"""
CareWise - Unified Health Research Assistant
Combines biomedical research and general health information
"""

__version__ = "2.0.0"

from intelligence.planner import build_execution_plan
from data.router import execute_data_layer
from data.ranker import rank_evidence
from answer_engine.answer_generator import generate_grounded_answer

__all__ = [
    "build_execution_plan",
    "execute_data_layer",
    "rank_evidence",
    "generate_grounded_answer"
]
