"""
FastAPI backend server for CareWise Bio
Provides REST API for the frontend
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from carewise import build_execution_plan, execute_data_layer, generate_grounded_answer
from carewise.data import rank_evidence

app = FastAPI(
    title="CareWise Bio API",
    description="Biomedical Research Assistant API",
    version="1.0.0"
)

# CORS configuration for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class QueryRequest(BaseModel):
    query: str


class QueryResponse(BaseModel):
    execution_plan: dict
    answer: dict
    evidence: list


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "online",
        "service": "CareWise Bio API",
        "version": "1.0.0"
    }


@app.post("/api/query", response_model=QueryResponse)
async def process_query(request: QueryRequest):
    """
    Process a biomedical research query
    
    Returns execution plan, grounded answer, and ranked evidence
    """
    try:
        # Step 1: Query Intelligence - Build execution plan
        print(f"\n📝 Processing query: {request.query}")
        plan = build_execution_plan(request.query)
        print(f"✅ Plan: {plan['intent']} | Sources: {plan['sources']}")
        
        # Step 2: Data Acquisition - Fetch from APIs
        print("📚 Fetching data from sources...")
        results = execute_data_layer(plan)
        print(f"✅ Found {len(results)} raw results")
        
        # Step 3: Evidence Ranking
        print("📊 Ranking evidence...")
        ranked_results = rank_evidence(results, plan)
        print(f"✅ Ranked {len(ranked_results)} evidence items")
        
        # Step 4: Generate grounded answer
        print("💡 Generating LLM answer...")
        answer_result = generate_grounded_answer(request.query, ranked_results)
        print("✅ Answer generated")
        
        return {
            "execution_plan": plan,
            "answer": answer_result,
            "evidence": ranked_results
        }
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "components": {
            "api": "online",
            "llm": "ollama",
            "data_sources": ["PubMed", "ClinicalTrials", "FDA"]
        }
    }


if __name__ == "__main__":
    import uvicorn
    print("="*80)
    print("🧬 CAREWISE BIO API SERVER")
    print("="*80)
    print("\n📡 Starting server on http://localhost:8000")
    print("📖 API docs available at http://localhost:8000/docs")
    print("\n⚠️  Make sure Ollama is running: ollama serve")
    print("="*80)
    print()
    
    uvicorn.run(app, host="0.0.0.0", port=8000)
