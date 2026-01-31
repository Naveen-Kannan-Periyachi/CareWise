"""Configuration settings for unified CareWise system"""

# API Keys
PUBMED_API_KEY = "4466672a0ded684cca401ab6a157aaffa709"
FDA_API_KEY = "KKYHGGWJwfnpsfkij7vS0CgXn6WaRaQ1gKbgPXvH"

# API URLs - Biomedical Research Sources
PUBMED_ESEARCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
PUBMED_EFETCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
CLINICAL_TRIALS_URL = "https://clinicaltrials.gov/api/v2/studies"
FDA_LABEL_URL = "https://api.fda.gov/drug/label.json"

# API URLs - General Health Sources
MEDLINEPLUS_URL = "https://wsearch.nlm.nih.gov/ws/query"
CDC_URL = "https://data.cdc.gov/resource/bi63-dtpu.json"
WHO_URL = "https://ghoapi.azureedge.net/api/"

# LLM Configuration
OLLAMA_URL = "http://localhost:11434/api/generate"
LLM_MODEL = "llama3.1:8b"
LLM_TIMEOUT = 60
