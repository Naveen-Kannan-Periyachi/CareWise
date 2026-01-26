"""Answer Generator - Creates grounded answers using LLM and evidence"""

from carewise.intelligence.llm_client import call_llm


def build_grounding_prompt(query, ranked_evidence, top_k=5):
    """
    Build a prompt that grounds the LLM answer in provided evidence.
    
    Args:
        query: The user's original question
        ranked_evidence: List of ranked evidence items
        top_k: Number of top evidence items to include
        
    Returns:
        Formatted prompt string
    """
    # Use top K evidence items
    evidence_items = ranked_evidence[:top_k]
    
    # Build evidence context
    evidence_text = ""
    for i, item in enumerate(evidence_items, 1):
        evidence_text += f"\n[Evidence {i}] Source: {item['source']}\n"
        evidence_text += f"Title: {item['title']}\n"
        evidence_text += f"Content: {item['content'][:500]}...\n"
        evidence_text += f"Relevance Score: {item['score']:.2f}\n"
    
    prompt = f"""You are a biomedical research assistant. Answer the user's question using ONLY the provided evidence below.

CRITICAL RULES:
1. Base your answer ONLY on the evidence provided
2. DO NOT use external knowledge
3. Cite sources using [Source Name] after each claim
4. If evidence is insufficient, say "Based on the available evidence, I cannot fully answer this question"
5. Be concise and accurate

EVIDENCE:
{evidence_text}

USER QUESTION:
{query}

ANSWER (cite sources with [PubMed], [ClinicalTrials], or [FDA]):
"""
    
    return prompt


def generate_grounded_answer(query, ranked_evidence):
    """
    Generate an answer grounded in the provided evidence.
    
    Args:
        query: The user's question
        ranked_evidence: List of ranked evidence items
        
    Returns:
        Dictionary with answer and metadata
    """
    # Build grounding prompt
    prompt = build_grounding_prompt(query, ranked_evidence, top_k=5)
    
    # Call LLM
    try:
        answer = call_llm(prompt)
        
        # Extract sources used
        sources_used = []
        for item in ranked_evidence[:5]:
            if item['source'] in answer:
                sources_used.append({
                    'source': item['source'],
                    'title': item['title'],
                    'id': item['id']
                })
        
        return {
            'answer': answer.strip(),
            'evidence_count': len(ranked_evidence[:5]),
            'sources_used': sources_used,
            'top_evidence': ranked_evidence[:5]
        }
        
    except Exception as e:
        return {
            'answer': f"Error generating answer: {str(e)}",
            'evidence_count': 0,
            'sources_used': [],
            'top_evidence': []
        }
