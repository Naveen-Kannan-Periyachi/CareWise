# CareWise Bio - React Frontend

Modern, responsive React frontend for the CareWise Bio biomedical research assistant.

## 🚀 Quick Start

### Prerequisites

- Node.js 16+ and npm
- CareWise Bio backend running on `http://localhost:8000`

### Installation

```bash
cd frontend
npm install
```

### Development

```bash
npm start
```

The app will open at [http://localhost:3000](http://localhost:3000)

### Production Build

```bash
npm run build
```

The optimized production build will be in the `build/` folder.

## 🏗️ Project Structure

```
frontend/
├── public/
│   └── index.html
├── src/
│   ├── components/
│   │   ├── QueryInput.js          # Search bar with example queries
│   │   ├── ExecutionPlan.js       # Display query planning results
│   │   ├── AnswerDisplay.js       # Show LLM-grounded answer
│   │   ├── EvidenceList.js        # Grid of evidence items
│   │   ├── EvidenceCard.js        # Individual evidence card
│   │   └── LoadingSpinner.js      # Loading animation
│   ├── App.js                     # Main application component
│   ├── App.css                    # App-level styles
│   ├── index.js                   # Entry point
│   └── index.css                  # Global styles
├── package.json
└── README.md
```

## 🎨 Features

### ✅ Modern UI/UX

- Gradient backgrounds and smooth animations
- Responsive design (mobile, tablet, desktop)
- Card-based layout for easy scanning
- Color-coded source badges (PubMed, ClinicalTrials, FDA)

### ✅ Interactive Components

- **QueryInput**: Searchbar with 5 example queries
- **ExecutionPlan**: Visual display of query intent, entities, and sources
- **AnswerDisplay**: LLM-generated answer with inline citations
- **EvidenceCard**: Expandable cards with relevance scores and metadata
- **LoadingSpinner**: Multi-step loading animation

### ✅ Evidence Display

- Ranked evidence items with scores (0-100%)
- Color-coded relevance (green > 80%, orange > 60%, gray < 60%)
- Expandable cards showing full content and score breakdown
- Metadata display (year, status, phase, etc.)

### ✅ Responsive Design

- Mobile-first approach
- Adapts to all screen sizes
- Touch-friendly interfaces

## 🔌 Backend Integration

The frontend expects a backend API at `http://localhost:8000` with the following endpoint:

### POST `/api/query`

**Request:**

```json
{
  "query": "Any ongoing CAR-T trials for melanoma?"
}
```

**Response:**

```json
{
  "execution_plan": {
    "intent": "CLINICAL_TRIALS",
    "entities": {
      "diseases": ["melanoma"],
      "drugs": [],
      "therapies": ["CAR-T"]
    },
    "sources": ["ClinicalTrials", "PubMed"],
    "analysis_required": false
  },
  "answer": {
    "answer": "Based on the evidence, there are several ongoing CAR-T trials for melanoma [ClinicalTrials]...",
    "evidence_count": 5,
    "sources_used": [
      {
        "source": "ClinicalTrials",
        "title": "CAR-T Cell Therapy for Advanced Melanoma",
        "id": "NCT12345678"
      }
    ]
  },
  "evidence": [
    {
      "id": "NCT12345678",
      "title": "CAR-T Cell Therapy for Advanced Melanoma",
      "content": "This study evaluates...",
      "source": "ClinicalTrials",
      "score": 0.94,
      "metadata": {
        "nct_id": "NCT12345678",
        "status": "RECRUITING",
        "phase": "PHASE2"
      },
      "scores_breakdown": {
        "relevance": 1.0,
        "source_priority": 1.0,
        "completeness": 0.8,
        "recency": 0.9
      }
    }
  ]
}
```

## 🎨 Color Scheme

- Primary gradient: `#667eea` → `#764ba2`
- PubMed: `#3b82f6` (blue)
- ClinicalTrials: `#10b981` (green)
- FDA: `#f59e0b` (orange)

## 📦 Dependencies

- **react**: ^18.2.0
- **react-dom**: ^18.2.0
- **axios**: ^1.6.0 (HTTP client)
- **lucide-react**: ^0.263.1 (Icons)
- **react-scripts**: 5.0.1 (Build tooling)

## 🔧 Configuration

The backend API URL is configured via proxy in `package.json`:

```json
"proxy": "http://localhost:8000"
```

Change this if your backend runs on a different port.

## 🚀 Deployment

### Build for Production

```bash
npm run build
```

### Serve Static Build

```bash
npm install -g serve
serve -s build -p 3000
```

### Deploy to Netlify/Vercel

The `build/` folder can be deployed directly to static hosting services.

## 📝 License

MIT License - Same as the main CareWise Bio project
