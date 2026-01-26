"""
CareWise Bio - Biomedical Research Assistant
Clean, production-ready implementation
"""

__version__ = "1.0.0"

from .intelligence.planner import build_execution_plan
from .data.router import execute_data_layer
from .answer_generator import generate_grounded_answer

__all__ = ["build_execution_plan", "execute_data_layer", "generate_grounded_answer"]
