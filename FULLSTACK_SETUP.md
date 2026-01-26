# CareWise Bio - Full Stack Setup Guide

Complete setup instructions for the CareWise Bio biomedical research assistant with React frontend and Python backend.

## 🚀 Quick Start (3 Steps)

### Step 1: Backend Setup

```bash
# Install Python dependencies
pip install -r requirements.txt

# Install Ollama and pull the model
# Download from https://ollama.com/download
ollama pull llama3.1:8b

# Start Ollama service
ollama serve
```

### Step 2: Start Backend API

```bash
# In a new terminal
python backend_api.py
```

The API will start on http://localhost:8000

### Step 3: Start Frontend

```bash
# In a new terminal
cd frontend
npm install
npm start
```

The app will open at http://localhost:3000

---

## 📁 Complete Project Structure

```
carewise-bio/
├── frontend/                        # React Frontend
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── components/
│   │   │   ├── QueryInput.js       # Search interface
│   │   │   ├── ExecutionPlan.js    # Plan visualization
│   │   │   ├── AnswerDisplay.js    # LLM answer
│   │   │   ├── EvidenceList.js     # Evidence grid
│   │   │   ├── EvidenceCard.js     # Individual cards
│   │   │   └── LoadingSpinner.js   # Loading animation
│   │   ├── App.js
│   │   └── index.js
│   ├── package.json
│   └── README.md
│
├── src/carewise/                    # Python Backend
│   ├── intelligence/               # Query planning
│   ├── data/                       # Data acquisition
│   └── config/                     # Configuration
│
├── backend_api.py                  # FastAPI server
├── main.py                         # CLI interface
├── requirements.txt
└── FULLSTACK_SETUP.md             # This file
```

---

## 🔧 Detailed Setup

### Prerequisites

- **Python 3.12+**
- **Node.js 16+** and npm
- **Ollama** (for local LLM)
- **Internet connection** (for API calls)

### Backend Installation

1. **Clone or navigate to project:**

   ```bash
   cd carewise-bio
   ```

2. **Create virtual environment (optional but recommended):**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Python dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Install and configure Ollama:**

   ```bash
   # Download from https://ollama.com/download
   # After installation:
   ollama pull llama3.1:8b
   ```

5. **Verify installation:**
   ```bash
   python -c "import carewise; print('✅ Backend installed')"
   ```

### Frontend Installation

1. **Navigate to frontend directory:**

   ```bash
   cd frontend
   ```

2. **Install Node dependencies:**

   ```bash
   npm install
   ```

3. **Verify installation:**
   ```bash
   npm run build
   ```

---

## 🎮 Running the Application

### Option 1: Full Stack (Recommended)

**Terminal 1 - Ollama:**

```bash
ollama serve
```

**Terminal 2 - Backend API:**

```bash
python backend_api.py
```

**Terminal 3 - Frontend:**

```bash
cd frontend
npm start
```

Access the app at: **http://localhost:3000**

### Option 2: CLI Only (No Frontend)

```bash
ollama serve  # In one terminal
python main.py  # In another terminal
```

---

## 🧪 Testing the Setup

### Test Backend API

```bash
# Check API health
curl http://localhost:8000/

# Test query endpoint
curl -X POST http://localhost:8000/api/query \
  -H "Content-Type: application/json" \
  -d '{"query": "CAR-T trials for melanoma"}'
```

### Test Frontend

1. Open http://localhost:3000
2. Click an example query
3. Verify results display correctly

---

## 🎯 Features

### Frontend Features

✅ Modern gradient UI with animations  
✅ Mobile-responsive design  
✅ 5 pre-loaded example queries  
✅ Real-time loading animations  
✅ Expandable evidence cards  
✅ Color-coded source badges  
✅ Relevance score visualization  
✅ Inline citation rendering

### Backend Features

✅ LLM-powered query planning  
✅ Multi-source data fetching (PubMed, ClinicalTrials, FDA)  
✅ Evidence normalization & ranking  
✅ Grounded answer generation  
✅ REST API with CORS support  
✅ Automatic error handling  
✅ FastAPI documentation

---

## 📊 API Documentation

Once the backend is running, visit:

- **Interactive API docs**: http://localhost:8000/docs
- **Alternative docs**: http://localhost:8000/redoc

### Main Endpoint

**POST** `/api/query`

Request:

```json
{
  "query": "Any ongoing CAR-T trials for melanoma?"
}
```

Response:

```json
{
  "execution_plan": { ... },
  "answer": { ... },
  "evidence": [ ... ]
}
```

---

## 🛠️ Configuration

### Backend Configuration

Edit `src/carewise/config/settings.py`:

```python
PUBMED_API_KEY = "your-key-here"
FDA_API_KEY = "your-key-here"
```

⚠️ **Security Note**: Use environment variables in production!

### Frontend Configuration

Edit `frontend/package.json`:

```json
"proxy": "http://localhost:8000"
```

Change if backend runs on different port.

---

## 📦 Production Deployment

### Backend

```bash
# Install production dependencies
pip install gunicorn

# Run with Gunicorn
gunicorn backend_api:app -w 4 -k uvicorn.workers.UvicornWorker
```

### Frontend

```bash
cd frontend
npm run build

# Serve static files
npm install -g serve
serve -s build -p 3000
```

Or deploy `frontend/build/` to:

- Netlify
- Vercel
- AWS S3 + CloudFront
- Any static hosting service

---

## 🐛 Troubleshooting

### "Ollama connection refused"

```bash
# Make sure Ollama is running:
ollama serve

# Test Ollama:
ollama run llama3.1:8b "Hello"
```

### "Module not found: carewise"

```bash
# Install in development mode:
pip install -e .
```

### Frontend can't connect to backend

- Verify backend is running on port 8000
- Check CORS settings in `backend_api.py`
- Check proxy in `frontend/package.json`

### API returns 500 errors

- Check Ollama is running
- Check API keys are valid
- Check internet connection
- View logs in terminal

---

## 🔍 Example Queries

1. "Any ongoing CAR-T trials for melanoma?"
2. "What are the side effects of Pembrolizumab?"
3. "Latest research on CRISPR gene therapy for sickle cell disease"
4. "Clinical trials for Alzheimer's disease treatment"
5. "Compare chemotherapy and immunotherapy for lung cancer"

---

## 📈 Performance Notes

- **First query**: 10-20 seconds (LLM planning + API calls)
- **Subsequent queries**: 5-15 seconds
- **Evidence items**: Top 5 displayed, expandable to all
- **LLM latency**: 2-5 seconds (Ollama local)

---

## 🎓 Tech Stack Summary

### Frontend

- React 18.2
- Axios (HTTP client)
- Lucide React (Icons)
- CSS3 (Animations & Grid)

### Backend

- Python 3.12+
- FastAPI (REST API)
- Ollama + llama3.1:8b (LLM)
- Requests (HTTP)
- PubMed, ClinicalTrials.gov, FDA APIs

---

## 📝 License

MIT License - Built for hackathons and research

---

## 🤝 Support

For issues or questions:

1. Check terminal logs
2. Visit http://localhost:8000/docs for API testing
3. Review this setup guide

**Happy researching! 🧬**
