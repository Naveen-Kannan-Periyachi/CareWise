"""Entity extractor using LLM for both biomedical and general health queries"""

import json
import requests
from config.settings import OLLAMA_URL, LLM_MODEL, LLM_TIMEOUT


class EntityExtractor:
    """Extracts entities from health and biomedical queries"""
    
    def __init__(self):
        self.url = OLLAMA_URL
        self.model = LLM_MODEL

    def extract(self, query: str) -> dict:
        """
        Extract entities from query for both biomedical and general health contexts.
        
        Returns:
            Dict with diseases, drugs, therapies, symptoms, and topics
        """
        prompt = f"""You are a medical text analyzer.

Extract medical entities from the query.

Return STRICT JSON only:

{{
  "diseases": [],
  "drugs": [],
  "therapies": [],
  "symptoms": [],
  "topics": []
}}

Rules:
- diseases: Medical conditions, illnesses
- drugs: Medication names
- therapies: Treatments like CAR-T, CRISPR
- symptoms: Physical feelings, pains
- topics: General health topics

Do NOT explain. Do NOT add extra text.

Query:
"{query}"
"""

        try:
            response = requests.post(
                self.url,
                json={"model": self.model, "prompt": prompt, "stream": False},
                timeout=LLM_TIMEOUT
            )
            response.raise_for_status()
            
            output = response.json()["response"].strip()

            # Extract JSON from response
            start = output.find("{")
            end = output.rfind("}") + 1
            
            if start != -1 and end > 0:
                json_text = output[start:end]
                data = json.loads(json_text)
                
                # Ensure all required fields exist
                default = {
                    "diseases": [],
                    "drugs": [],
                    "therapies": [],
                    "symptoms": [],
                    "topics": []
                }
                default.update(data)
                return default
            else:
                return {
                    "diseases": [],
                    "drugs": [],
                    "therapies": [],
                    "symptoms": [],
                    "topics": []
                }
        except Exception as e:
            print(f"Entity extraction error: {e}")
            return {
                "diseases": [],
                "drugs": [],
                "therapies": [],
                "symptoms": [],
                "topics": []
            }
