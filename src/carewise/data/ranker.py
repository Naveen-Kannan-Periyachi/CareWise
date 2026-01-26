"""Evidence Ranker - Scores and ranks evidence by relevance"""

from datetime import datetime


def calculate_relevance_score(evidence, query_entities):
    """
    Calculate how relevant the evidence is to the query.
    Checks if query entities appear in title or content.
    Returns score normalized to 0-1 range.
    """
    matches = 0
    text = (evidence['title'] + " " + evidence['content']).lower()
    
    # Count total entities
    total_entities = sum(len(entity_list) for entity_list in query_entities.values())
    
    if total_entities == 0:
        return 0.5  # Neutral score if no entities
    
    # Check each entity type
    for entity_list in query_entities.values():
        for entity in entity_list:
            if entity.lower() in text:
                matches += 1
    
    # Normalize: 0.0 for no matches, 1.0 for all entities matched
    return min(matches / total_entities, 1.0)


def calculate_recency_score(evidence):
    """
    Score based on recency (newer is better).
    Only applicable to PubMed articles with year.
    """
    metadata = evidence.get('metadata', {})
    year = metadata.get('year')
    
    if not year:
        return 0.5  # Neutral score for no date
    
    try:
        year = int(year)
        current_year = datetime.now().year
        
        # Recent papers get higher score
        age = current_year - year
        if age <= 1:
            return 1.0
        elif age <= 3:
            return 0.8
        elif age <= 5:
            return 0.6
        else:
            return 0.4
    except:
        return 0.5


def calculate_completeness_score(evidence):
    """
    Score based on content completeness.
    More content generally means more information.
    """
    content = evidence.get('content', '')
    
    if not content or content == "No abstract available" or content == "No content":
        return 0.3
    
    length = len(content)
    
    if length > 500:
        return 1.0
    elif length > 200:
        return 0.8
    elif length > 50:
        return 0.6
    else:
        return 0.4


def calculate_source_priority(evidence, intent):
    """
    Score based on source relevance to query intent.
    Some sources are more relevant for certain intents.
    """
    source = evidence['source']
    
    priority_map = {
        'CLINICAL_TRIALS': {
            'ClinicalTrials': 1.0,
            'PubMed': 0.8,
            'FDA': 0.3
        },
        'DRUG_SAFETY': {
            'FDA': 1.0,
            'PubMed': 0.6,
            'ClinicalTrials': 0.4
        },
        'LITERATURE_REVIEW': {
            'PubMed': 1.0,
            'ClinicalTrials': 0.5,
            'FDA': 0.3
        },
        'COMPARATIVE_RESEARCH': {
            'PubMed': 1.0,
            'ClinicalTrials': 0.8,
            'FDA': 0.6
        },
        'DATA_ANALYSIS': {
            'PubMed': 1.0,
            'ClinicalTrials': 0.7,
            'FDA': 0.5
        }
    }
    
    return priority_map.get(intent, {}).get(source, 0.5)


def rank_evidence(evidence_list, query_plan):
    """
    Rank evidence items by relevance to the query.
    
    Args:
        evidence_list: List of normalized evidence items
        query_plan: The execution plan from query intelligence
        
    Returns:
        List of evidence items sorted by score (highest first)
    """
    entities = query_plan['entities']
    intent = query_plan['intent']
    
    # Calculate composite score for each evidence item
    for evidence in evidence_list:
        scores = {
            'relevance': calculate_relevance_score(evidence, entities),
            'recency': calculate_recency_score(evidence),
            'completeness': calculate_completeness_score(evidence),
            'source_priority': calculate_source_priority(evidence, intent)
        }
        
        # Weighted combination
        evidence['score'] = (
            scores['relevance'] * 0.4 +         # Relevance is most important
            scores['source_priority'] * 0.3 +   # Source type matters
            scores['completeness'] * 0.2 +      # Content quality
            scores['recency'] * 0.1             # Recency is least important
        )
        
        # Store individual scores for transparency
        evidence['scores_breakdown'] = scores
    
    # Sort by score (highest first)
    ranked = sorted(evidence_list, key=lambda x: x['score'], reverse=True)
    
    return ranked
