"""
Prompt builder for the LLM planner.
"""

def build_planner_prompt(query: str) -> str:
    """Build a strict prompt that forces the LLM to act as a query planning engine."""
    return f"""You are a biomedical query planning engine.

Convert the user query into a structured execution plan in JSON.
Do NOT answer the query.
Do NOT explain.

INTENTS:

LITERATURE_REVIEW:
Research papers, latest studies, scientific findings.

CLINICAL_TRIALS:
Ongoing, completed, or recruiting clinical trials.

DRUG_SAFETY:
Side effects, warnings, adverse reactions.

COMPARATIVE_RESEARCH:
Comparison between treatments, drugs, or approaches.

DATA_ANALYSIS:
Requests involving calculations, datasets, or statistics.

JSON FORMAT:
{{
  "intent": "",
  "entities": {{
    "diseases": [],
    "drugs": [],
    "therapies": []
  }},
  "sources": [],
  "analysis_required": false
}}

EXAMPLES:

Query: Any ongoing CAR-T trials for melanoma?
Output:
{{
  "intent": "CLINICAL_TRIALS",
  "entities": {{
    "diseases": ["melanoma"],
    "drugs": [],
    "therapies": ["CAR-T"]
  }},
  "sources": ["ClinicalTrials", "PubMed"],
  "analysis_required": false
}}

Query: What are the side effects of pembrolizumab?
Output:
{{
  "intent": "DRUG_SAFETY",
  "entities": {{
    "diseases": [],
    "drugs": ["pembrolizumab"],
    "therapies": []
  }},
  "sources": ["FDA"],
  "analysis_required": false
}}

Query: Latest research on CRISPR gene therapy
Output:
{{
  "intent": "LITERATURE_REVIEW",
  "entities": {{
    "diseases": [],
    "drugs": [],
    "therapies": ["CRISPR gene therapy"]
  }},
  "sources": ["PubMed"],
  "analysis_required": false
}}

Now process this query:
"{query}"

Return ONLY JSON.
"""
