# 🏥 CareWise - Unified Health Research Assistant

> **Note**: This project has been unified! The old `src/carewise-bio` and `src/carewise-suggest` projects have been merged into the new `carewise/` directory.

A comprehensive AI-powered health research assistant that combines **biomedical research** and **general health information** capabilities. Converts natural language queries into structured execution plans and fetches real data from 6 trusted sources.

## 🚀 Quick Start

```bash
# Navigate to the unified project
cd carewise

# Install dependencies
pip install -r requirements.txt

# Run the CLI
python main.py

# Or start the API server
python backend_api.py
```

## 🌟 Dual-Mode Operation

### Biomedical Research Mode (carewise-bio)

- 📚 **PubMed** - Scientific literature and research papers
- 🏥 **ClinicalTrials.gov** - Clinical trial data
- 💊 **FDA** - Drug safety information

### General Health Mode (carewise-suggest)

- 📖 **MedlinePlus** - Consumer health information
- 🏛️ **CDC** - Public health data
- 🌍 **WHO** - Global health statistics

## 🏗️ Unified Architecture

```
User Query → Intelligence Layer → Unified Router → 6 Data Sources
                                                   ↓
                                              Normalizer
                                                   ↓
                                                 Ranker
                                                   ↓
                                          Answer Generator
                                                   ↓
                                          Grounded Answer
```

## 📁 New Project Structure

**Main Project**: `carewise/` (use this)

- All 6 data sources integrated
- Unified intelligence layer
- Single entry point for all queries

**Old Projects** (deprecated):

- `src/carewise-bio/` - Old biomedical project
- `src/carewise-suggest/` - Old general health project

Run `.\cleanup.ps1` to remove old projects after closing all terminals.

## 📊 Example Queries

**Biomedical Research:**

```
- Any ongoing CAR-T trials for melanoma?
- What are the side effects of Pembrolizumab?
- Latest research on CRISPR gene therapy
```

**General Health:**

```
- What causes headaches and how to treat them?
- Information about diabetes prevention
- Global statistics on tuberculosis
```

## 📖 Full Documentation

See `carewise/README.md` for complete documentation of the unified system.

---

## Legacy Architecture (Old)

│ ┌────────────────────────────────────────────────────┐ │
│ │ Normalizer │ │
│ │ - Converts different API formats │ │
│ │ - Creates unified Evidence objects │ │
│ │ - Cleans and standardizes data │ │
│ └────────────────────────────────────────────────────┘ │
└──────────────────────┬──────────────────────────────────────┘
↓
Unified Evidence List
↓
┌─────────────────────────────────────────────────────────────┐
│ RESULTS │
│ [ │
│ { │
│ "type": "clinical_trial", │
│ "title": "CAR-T Cell Therapy for Melanoma", │
│ "nct_id": "NCT12345678", │
│ "status": "RECRUITING", │
│ "url": "https://clinicaltrials.gov/study/NCT12345678" │
│ }, │
│ ... │
│ ] │
└─────────────────────────────────────────────────────────────┘

```

## 📁 Project Structure

```

carewise-bio/
│
├── backend/
│ ├── main.py # 🎮 Main entry point
│ │
│ ├── query_intelligence/ # 🧠 Layer 1: Query Intelligence
│ │ ├── **init**.py
│ │ ├── planner.py # Main orchestrator with self-healing
│ │ ├── prompt.py # LLM prompt engineering
│ │ ├── schema.py # Allowed intents & sources
│ │ ├── validator.py # Plan validation logic
│ │ └── llm_planner.py # Ollama LLM interface
│ │
│ ├── biomedical_data/ # 📚 Layer 2: Data Acquisition
│ │ ├── **init**.py
│ │ ├── pubmed_client.py # PubMed API client
│ │ ├── clinical_trials_client.py # ClinicalTrials.gov client
│ │ ├── fda_client.py # openFDA client
│ │ ├── data_router.py # Routes plans to data sources
│ │ └── normalizer.py # Converts raw data to Evidence
│ │
│ ├── config/ # ⚙️ Configuration
│ │ ├── **init**.py
│ │ └── settings.py # API keys, URLs, constants
│ │
│ ├── models/ # 📋 Data Models
│ │ ├── **init**.py
│ │ └── evidence.py # Unified Evidence object
│ │
│ └── utils/ # 🛠️ Utilities
│ └── helpers.py # Helper functions
│
├── query_intelligence/ # (Root level - legacy)
│ └── ... # Original implementation
│
├── tests/ # 🧪 Tests
│ ├── test_query_intelligence.py
│ ├── test_pubmed.py
│ ├── test_clinical_trials.py
│ └── test_fda.py
│
├── requirements.txt
└── README.md

````

## 🚀 Quick Start

### 1. Prerequisites

- **Python 3.12+**
- **Ollama** (for local LLM)

### 2. Install Ollama

```bash
# Download from https://ollama.com/download
# Then pull the model
ollama pull llama3.1:8b
````

### 3. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Application

```bash
# Make sure Ollama is running
ollama serve

# In another terminal, run the app
cd carewise-bio/backend
python main.py
```

## 📖 Usage Examples

### Command Line Interface

```bash
python backend/main.py
```

### Programmatic Usage

```python
from backend.main import process_query

# Run a query
results = process_query("Any ongoing CAR-T trials for melanoma?")

# Access results
print(f"Found {results['summary']['total_evidence']} evidence items")

for evidence in results['evidence']:
    print(f"{evidence['type']}: {evidence['title']}")
```

## 🧪 Running Tests

```bash
# Test Query Intelligence
python tests/test_query_intelligence.py

# Test PubMed client
python tests/test_pubmed.py

# Test ClinicalTrials client
python tests/test_clinical_trials.py

# Test FDA client
python tests/test_fda.py
```

## 🎯 Supported Query Types

| Intent                   | Description              | Example                                 | Data Sources           |
| ------------------------ | ------------------------ | --------------------------------------- | ---------------------- |
| **LITERATURE_REVIEW**    | Research papers, studies | "Latest research on CRISPR"             | PubMed                 |
| **CLINICAL_TRIALS**      | Ongoing/completed trials | "CAR-T trials for melanoma"             | ClinicalTrials.gov     |
| **DRUG_SAFETY**          | Side effects, warnings   | "Side effects of pembrolizumab"         | FDA                    |
| **COMPARATIVE_RESEARCH** | Treatment comparisons    | "Compare chemotherapy vs immunotherapy" | PubMed, ClinicalTrials |
| **DATA_ANALYSIS**        | Statistical analysis     | "Survival rates for lung cancer"        | All sources            |

## 🔑 API Keys

The project uses the following API keys (already configured in `backend/config/settings.py`):

- **PubMed**: `4466672a0ded684cca401ab6a157aaffa709-PubMed`
- **FDA**: `KKYHGGWJwfnpsfkij7vS0CgXn6WaRaQ1gKbgPXvH-FDA`
- **ClinicalTrials.gov**: No API key required (public API)

## 🏆 Key Features

### ✅ Production-Grade Architecture

- **Separation of concerns**: Each layer has one responsibility
- **Type safety**: Using dataclasses for models
- **Error handling**: Graceful failures with fallbacks
- **Self-healing**: LLM output automatically validated and corrected

### ✅ No External Costs

- **Local LLM** via Ollama (free, private)
- **Free APIs** (PubMed, ClinicalTrials.gov, FDA)
- **No API key requirements** for basic usage

### ✅ Real Data Integration

- **PubMed**: 35M+ biomedical papers
- **ClinicalTrials.gov**: 400K+ clinical trials
- **FDA**: Drug labels and adverse events

### ✅ Extensible Design

- Add new intents in `schema.py`
- Add new data sources as new clients
- Easy to integrate with frontend

## 📊 Example Output

```json
{
  "query": "Any ongoing CAR-T trials for melanoma?",
  "execution_plan": {
    "intent": "CLINICAL_TRIALS",
    "entities": {
      "diseases": ["melanoma"],
      "drugs": [],
      "therapies": ["CAR-T"]
    },
    "sources": ["ClinicalTrials"],
    "analysis_required": false
  },
  "evidence": [
    {
      "type": "clinical_trial",
      "source": "ClinicalTrials.gov",
      "title": "CAR-T Cell Therapy for Advanced Melanoma",
      "nct_id": "NCT05123456",
      "status": "RECRUITING",
      "phase": ["PHASE2"],
      "url": "https://clinicaltrials.gov/study/NCT05123456"
    }
  ],
  "summary": {
    "total_evidence": 1,
    "by_type": { "clinical_trial": 1 },
    "by_source": { "ClinicalTrials.gov": 1 }
  }
}
```

## 🛠️ Technology Stack

- **Python 3.12**
- **Ollama** (llama3.1:8b) for query intelligence
- **Requests** for API calls
- **Dataclasses** for type-safe models
- **XML parsing** for PubMed data
- **JSON APIs** for ClinicalTrials & FDA

## 📝 File Explanations

### Query Intelligence Layer

- **planner.py**: Main loop with self-healing retry logic
- **prompt.py**: Prompt engineering for LLM
- **schema.py**: Allowed intents and data sources
- **validator.py**: Validates LLM output against schema
- **llm_planner.py**: Interface to Ollama

### Data Acquisition Layer

- **pubmed_client.py**: Searches PubMed, fetches articles, parses XML
- **clinical_trials_client.py**: Searches ClinicalTrials.gov API
- **fda_client.py**: Searches FDA drug labels and adverse events
- **data_router.py**: Routes execution plan to appropriate clients
- **normalizer.py**: Converts different API formats to unified Evidence

### Core Components

- **main.py**: Entry point, ties everything together
- **evidence.py**: Unified data model for all evidence types
- **settings.py**: Configuration, API keys, URLs
- **helpers.py**: Utility functions

## 🎓 Design Principles

1. **LLM as untrusted component**: Always validate output
2. **Separation of planning and execution**: Query intelligence separate from data fetching
3. **Fail-safe by default**: Graceful error handling
4. **Extensibility first**: Easy to add new intents, sources, or models
5. **Production-ready**: Real error handling, logging, type safety

## 👨‍💻 Development

### Adding a New Data Source

1. Create new client in `backend/biomedical_data/`
2. Add source name to `schema.py`
3. Update `data_router.py` to route to new client
4. Update `normalizer.py` to handle new data format
5. Add tests in `tests/`

### Adding a New Intent

1. Add intent name to `schema.py`
2. Update prompt in `prompt.py` with examples
3. Test with `test_query_intelligence.py`

## 📜 License

MIT License - Feel free to use for hackathons, research, or production!

## 🤝 Contributing

This is a hackathon/research project. Contributions welcome!

---

**Built with ❤️ for advancing biomedical research**
