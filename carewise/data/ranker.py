"""Evidence Ranker - Scores and ranks evidence by relevance for all sources"""

from datetime import datetime


def calculate_relevance_score(evidence, query_entities):
    """Calculate how relevant the evidence is to the query"""
    matches = 0
    text = (evidence['title'] + " " + evidence['content']).lower()
    
    # Count total entities
    total_entities = sum(len(entity_list) for entity_list in query_entities.values())
    
    if total_entities == 0:
        return 0.5
    
    # Check each entity type
    for entity_list in query_entities.values():
        for entity in entity_list:
            if entity.lower() in text:
                matches += 1
    
    return min(matches / total_entities, 1.0)


def calculate_recency_score(evidence):
    """Score based on recency (newer is better)"""
    metadata = evidence.get('metadata', {})
    year = metadata.get('year')
    
    if not year:
        return 0.5
    
    try:
        year = int(year)
        current_year = datetime.now().year
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
    """Score based on content completeness"""
    content = evidence.get('content', '')
    
    if not content or content in ["No abstract available", "No content", "No summary available", "No description available"]:
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
    """Score based on source relevance to query intent"""
    source = evidence['source']
    
    priority_map = {
        # Biomedical research intents
        'CLINICAL_TRIALS': {
            'ClinicalTrials': 1.0,
            'PubMed': 0.8,
            'FDA': 0.3,
            'MedlinePlus': 0.5,
            'CDC': 0.4,
            'WHO': 0.3
        },
        'DRUG_SAFETY': {
            'FDA': 1.0,
            'PubMed': 0.6,
            'MedlinePlus': 0.8,
            'ClinicalTrials': 0.4,
            'CDC': 0.5,
            'WHO': 0.3
        },
        'LITERATURE_REVIEW': {
            'PubMed': 1.0,
            'ClinicalTrials': 0.5,
            'FDA': 0.3,
            'MedlinePlus': 0.4,
            'CDC': 0.4,
            'WHO': 0.5
        },
        'COMPARATIVE_RESEARCH': {
            'PubMed': 1.0,
            'ClinicalTrials': 0.8,
            'FDA': 0.6,
            'MedlinePlus': 0.5,
            'CDC': 0.5,
            'WHO': 0.6
        },
        'DATA_ANALYSIS': {
            'PubMed': 1.0,
            'WHO': 0.9,
            'CDC': 0.8,
            'ClinicalTrials': 0.7,
            'FDA': 0.5,
            'MedlinePlus': 0.4
        },
        # General health intents
        'SYMPTOMS_RELATED': {
            'MedlinePlus': 1.0,
            'CDC': 0.8,
            'PubMed': 0.6,
            'WHO': 0.5,
            'FDA': 0.4,
            'ClinicalTrials': 0.3
        },
        'INFORMATIONAL': {
            'MedlinePlus': 1.0,
            'CDC': 0.9,
            'WHO': 0.8,
            'PubMed': 0.7,
            'FDA': 0.5,
            'ClinicalTrials': 0.4
        },
        'GENERAL_HEALTH': {
            'CDC': 1.0,
            'WHO': 0.9,
            'MedlinePlus': 0.8,
            'PubMed': 0.5,
            'FDA': 0.3,
            'ClinicalTrials': 0.3
        }
    }
    
    return priority_map.get(intent, {}).get(source, 0.5)


def rank_evidence(evidence_list, query_plan):
    """
    Rank evidence items by relevance to the query.
    Works for both biomedical and general health sources.
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
            scores['relevance'] * 0.4 +
            scores['source_priority'] * 0.3 +
            scores['completeness'] * 0.2 +
            scores['recency'] * 0.1
        )
        
        evidence['scores_breakdown'] = scores
    
    # Sort by score (highest first)
    ranked = sorted(evidence_list, key=lambda x: x['score'], reverse=True)
    
    return ranked
