"""
Unified planner with self-healing logic for both biomedical and general health queries
"""

import json
from .llm_client import call_llm
from .prompt import build_planner_prompt
from .validator import validate_execution_plan

MAX_RETRIES = 3


def build_execution_plan(query: str) -> dict:
    """
    Build a validated execution plan from a user query.
    Handles both biomedical research and general health queries.
    Uses self-healing loop to automatically correct invalid LLM outputs.
    """
    prompt = build_planner_prompt(query)

    for attempt in range(1, MAX_RETRIES + 1):
        raw_output = call_llm(prompt)

        try:
            plan = json.loads(raw_output)
        except json.JSONDecodeError:
            prompt += "\n\nYour previous output was INVALID JSON. Fix it."
            continue

        valid, error = validate_execution_plan(plan)
        if valid:
            return plan

        prompt += f"\n\nERROR: {error}\nFix the JSON. Output ONLY valid JSON."

    raise RuntimeError("Failed to generate valid execution plan after retries")
