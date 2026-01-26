"""
Validator for execution plans.
"""

from .schema import ALLOWED_INTENTS, ALLOWED_SOURCES


def validate_execution_plan(plan: dict) -> tuple[bool, str]:
    """Validate an execution plan against the schema."""
    if not isinstance(plan, dict):
        return False, "Plan is not a JSON object"

    if "intent" not in plan or plan["intent"] not in ALLOWED_INTENTS:
        return False, "Invalid or missing intent"

    if "entities" not in plan or not isinstance(plan["entities"], dict):
        return False, "Missing or invalid entities"

    for key in ["diseases", "drugs", "therapies"]:
        if key not in plan["entities"] or not isinstance(plan["entities"][key], list):
            return False, f"Invalid entities field: {key}"

    if "sources" not in plan or not isinstance(plan["sources"], list):
        return False, "Missing or invalid sources"

    for src in plan["sources"]:
        if src not in ALLOWED_SOURCES:
            return False, f"Invalid source: {src}"

    if "analysis_required" not in plan or not isinstance(plan["analysis_required"], bool):
        return False, "Invalid analysis_required flag"

    return True, ""
