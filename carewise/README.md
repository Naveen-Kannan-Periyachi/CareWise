# 🏥 CareWise - Unified Health Research Assistant

A comprehensive AI-powered health research assistant that combines **biomedical research** capabilities with **general health information**. Converts natural language queries into structured execution plans and fetches real data from 6 trusted sources.

## 🌟 Features

### Dual-Mode Operation

**Biomedical Research Mode:**

- 📚 PubMed - Scientific literature and research papers
- 🏥 ClinicalTrials.gov - Clinical trial data
- 💊 FDA - Drug safety information

**General Health Mode:**

- 📖 MedlinePlus - Consumer health information
- 🏛️ CDC - Public health data
- 🌍 WHO - Global health statistics

### Intelligent Query Processing

- Automatic intent detection (8 intent types)
- Entity extraction (diseases, drugs, therapies, symptoms, topics)
- Smart source routing based on query type
- Self-healing LLM validation

### Evidence-Based Answers

- Relevance-based ranking
- Source prioritization
- LLM-generated grounded answers
- Citation tracking

## 🏗️ Architecture

```
User Query → Intelligence Layer → Data Router → 6 Data Sources
                                              ↓
                                         Normalizer
                                              ↓
                                            Ranker
                                              ↓
                                      Answer Generator
                                              ↓
                                      Grounded Answer
```

## 📁 Project Structure

```
carewise/
├── config/
│   ├── __init__.py
│   └── settings.py          # API keys and configuration
├── intelligence/
│   ├── __init__.py
│   ├── planner.py           # Unified query planner
│   ├── llm_client.py        # LLM interface
│   ├── entity_extraction.py # Entity extractor
│   ├── prompt.py            # Unified prompts
│   ├── validator.py         # Plan validator
│   └── schema.py            # Schema definitions
├── data/
│   ├── __init__.py
│   ├── router.py            # Unified data router
│   ├── normalizer.py        # Result normalizer
│   ├── ranker.py            # Evidence ranker
│   └── clients/
│       ├── __init__.py
│       ├── pubmed.py        # PubMed client
│       ├── clinical_trials.py
│       ├── fda.py           # FDA client
│       ├── medline.py       # MedlinePlus client
│       ├── cdc.py           # CDC client
│       └── who.py           # WHO client
├── answer_engine/
│   ├── __init__.py
│   └── answer_generator.py # Grounded answer generation
├── main.py                  # CLI interface
├── backend_api.py           # REST API
└── requirements.txt
```

## 🚀 Quick Start

### Prerequisites

1. **Python 3.10+**
2. **Ollama** with llama3.1:8b model
   ```bash
   # Install Ollama from https://ollama.ai
   ollama pull llama3.1:8b
   ollama serve
   ```

### Installation

```bash
# Navigate to the carewise directory
cd carewise

# Install dependencies
pip install -r requirements.txt
```

### Usage

#### Command Line Interface

```bash
python main.py
```

Example queries:

```
Biomedical Research:
- Any ongoing CAR-T trials for melanoma?
- What are the side effects of Pembrolizumab?
- Latest research on CRISPR gene therapy

General Health:
- What causes headaches and how to treat them?
- Information about diabetes prevention
- Global statistics on tuberculosis
```

#### REST API

```bash
python backend_api.py
```

API will be available at:

- **Main API**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs

Example API request:

```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What causes diabetes?"}'
```

## 📊 Supported Query Types

### Biomedical Research Intents

1. **LITERATURE_REVIEW** - Research papers, scientific findings
2. **CLINICAL_TRIALS** - Ongoing/completed trials
3. **DRUG_SAFETY** - Side effects, warnings
4. **COMPARATIVE_RESEARCH** - Treatment comparisons
5. **DATA_ANALYSIS** - Statistical analysis

### General Health Intents

6. **SYMPTOMS_RELATED** - Symptom information
7. **INFORMATIONAL** - Disease/condition information
8. **GENERAL_HEALTH** - Lifestyle, prevention, wellness

## 🔑 Configuration

API keys are configured in `config/settings.py`:

- **PUBMED_API_KEY** - PubMed E-utilities API key
- **FDA_API_KEY** - openFDA API key

Public APIs (no key required):

- ClinicalTrials.gov
- MedlinePlus
- CDC
- WHO

## 🎯 Example Workflow

```python
from intelligence.planner import build_execution_plan
from data.router import execute_data_layer
from data.ranker import rank_evidence
from answer_engine.answer_generator import generate_grounded_answer

# 1. Build execution plan
query = "What are the side effects of aspirin?"
plan = build_execution_plan(query)

# 2. Fetch data from sources
evidence = execute_data_layer(plan)

# 3. Rank evidence by relevance
ranked_evidence = rank_evidence(evidence, plan)

# 4. Generate grounded answer
answer = generate_grounded_answer(query, ranked_evidence)

print(answer['answer'])
```

## 🔄 Integration Benefits

This unified system combines the best of both worlds:

✅ **Single codebase** for all health queries  
✅ **Automatic routing** to appropriate sources  
✅ **Consistent API** for biomedical and general health  
✅ **6 data sources** instead of 3  
✅ **Unified evidence ranking** and answer generation  
✅ **One deployment** for all query types

## 🛠️ Development

### Running Tests

```bash
python -m pytest
```

### API Endpoints

- `GET /` - API information
- `GET /health` - Health check
- `GET /sources` - List all data sources
- `POST /query` - Submit query (full pipeline)
- `POST /plan` - Get execution plan only

## 📝 License

This project is part of a hackathon/competition submission.

## 🤝 Contributing

This is an integrated version combining:

- **carewise-bio**: Biomedical research assistant
- **carewise-suggest**: General health information assistant

---

**Version**: 2.0.0  
**Status**: Unified & Production Ready  
**Data Sources**: 6 (PubMed, ClinicalTrials, FDA, MedlinePlus, CDC, WHO)
