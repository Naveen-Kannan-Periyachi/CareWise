"""
CareWise Unified Backend API
FastAPI server for both biomedical research and general health queries
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, EmailStr
from typing import Optional, List
import json
import asyncio
from contextlib import asynccontextmanager
from intelligence.planner import build_execution_plan
from data.router import execute_data_layer
from data.ranker import rank_evidence
from answer_engine.answer_generator import generate_grounded_answer
from database.mongodb import (
    create_user, authenticate_user, get_user_by_email,
    create_conversation, get_user_conversations, update_conversation_title, delete_conversation,
    create_message, get_conversation_messages, close_database
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    yield
    # Shutdown
    await close_database()

app = FastAPI(
    title="CareWise Unified API",
    description="Unified Health Research Assistant - Biomedical + General Health",
    version="2.0.0",
    lifespan=lifespan
)

# CORS configuration for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request/Response Models
class SignupRequest(BaseModel):
    name: str
    email: EmailStr
    password: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    name: str
    email: str
    created_at: Optional[str] = None

class ConversationRequest(BaseModel):
    user_email: EmailStr
    title: Optional[str] = "New Chat"

class ConversationUpdateRequest(BaseModel):
    title: str

class MessageRequest(BaseModel):
    conversation_id: str
    role: str
    content: str
    evidence: Optional[List[dict]] = None
    metadata: Optional[dict] = None


class QueryRequest(BaseModel):
    query: str


class QueryResponse(BaseModel):
    query: str
    execution_plan: dict
    evidence: list
    answer: dict
    top_sources: list


@app.get("/")
async def root():
    """API root endpoint"""
    return {
        "name": "CareWise Unified API",
        "version": "2.0.0",
        "description": "Unified health research assistant supporting both biomedical research and general health queries",
        "sources": [
            "PubMed (Biomedical Research)",
            "ClinicalTrials.gov (Clinical Trials)",
            "FDA (Drug Safety)",
            "MedlinePlus (Consumer Health)",
            "CDC (Public Health)",
            "WHO (Global Health)"
        ],
        "endpoints": {
            "/query": "Submit a health query",
            "/health": "Health check",
            "/sources": "List available sources"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "carewise-unified"}


@app.get("/sources")
async def get_sources():
    """List all available data sources"""
    return {
        "biomedical": [
            {
                "name": "PubMed",
                "description": "Research articles and scientific literature",
                "use_case": "Latest research, scientific findings"
            },
            {
                "name": "ClinicalTrials",
                "description": "Clinical trial data",
                "use_case": "Ongoing trials, trial status, enrollment"
            },
            {
                "name": "FDA",
                "description": "Drug safety information",
                "use_case": "Side effects, warnings, drug labels"
            }
        ],
        "general_health": [
            {
                "name": "MedlinePlus",
                "description": "Consumer health information",
                "use_case": "Health topics, symptoms, conditions"
            },
            {
                "name": "CDC",
                "description": "Public health data",
                "use_case": "Disease prevention, health statistics"
            },
            {
                "name": "WHO",
                "description": "Global health statistics",
                "use_case": "Global health data, indicators"
            }
        ]
    }


@app.post("/query", response_model=QueryResponse)
async def process_query(request: QueryRequest):
    """
    Process a unified health query
    
    Supports both:
    - Biomedical research queries (papers, trials, drugs)
    - General health queries (symptoms, prevention, information)
    """
    try:
        # Step 1: Build execution plan
        plan = build_execution_plan(request.query)
        
        # Step 2: Execute data layer
        evidence = execute_data_layer(plan)
        
        # Step 3: Rank evidence
        ranked_evidence = rank_evidence(evidence, plan)
        
        # Step 4: Generate answer
        answer = generate_grounded_answer(request.query, ranked_evidence)
        
        # Extract top sources for frontend
        top_sources = []
        for item in ranked_evidence[:5]:
            top_sources.append({
                "source": item["source"],
                "title": item["title"],
                "content": item["content"],  # Full content, not truncated
                "score": item["score"],
                "metadata": item.get("metadata", {})
            })
        
        return QueryResponse(
            query=request.query,
            execution_plan=plan,
            evidence=ranked_evidence[:10],
            answer=answer,
            top_sources=top_sources
        )
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/query-stream")
async def process_query_stream(query: str):
    """
    Process a query with real-time status updates via Server-Sent Events
    """
    async def event_generator():
        try:
            # Step 1: Analyzing intent
            yield f"data: {json.dumps({'status': 'analyzing', 'message': 'Analyzing your question'})}\n\n"
            await asyncio.sleep(0.5)  # Give UI time to show this status
            
            plan = build_execution_plan(query)
            
            # Step 2: Selecting sources
            yield f"data: {json.dumps({'status': 'selecting_sources', 'message': 'Selecting data sources'})}\n\n"
            await asyncio.sleep(0.5)  # Give UI time to show this status
            
            # Step 3: Searching databases
            yield f"data: {json.dumps({'status': 'searching', 'message': 'Searching databases'})}\n\n"
            await asyncio.sleep(0.3)  # Brief pause before actual search
            
            evidence = execute_data_layer(plan)
            ranked_evidence = rank_evidence(evidence, plan)
            
            # Step 4: Generating answer
            yield f"data: {json.dumps({'status': 'generating', 'message': 'Generating answer'})}\n\n"
            await asyncio.sleep(0.3)  # Brief pause before generation
            
            answer = generate_grounded_answer(query, ranked_evidence)
            
            # Extract top sources
            top_sources = []
            for item in ranked_evidence[:5]:
                top_sources.append({
                    "source": item["source"],
                    "title": item["title"],
                    "content": item["content"],
                    "score": item["score"],
                    "metadata": item.get("metadata", {})
                })
            
            # Final result
            result = {
                'status': 'complete',
                'data': {
                    'query': query,
                    'plan': plan,
                    'evidence': ranked_evidence[:10],
                    'answer': answer,
                    'top_sources': top_sources
                }
            }
            yield f"data: {json.dumps(result)}\n\n"
            
        except Exception as e:
            import traceback
            traceback.print_exc()
            yield f"data: {json.dumps({'status': 'error', 'message': str(e)})}\n\n"
    
    return StreamingResponse(event_generator(), media_type="text/event-stream")


@app.post("/plan")
async def create_plan(request: QueryRequest):
    """Create an execution plan without fetching data"""
    try:
        plan = build_execution_plan(request.query)
        return {"query": request.query, "plan": plan}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Authentication Endpoints
@app.post("/auth/signup", response_model=UserResponse)
async def signup(request: SignupRequest):
    """Register a new user"""
    try:
        user = await create_user(request.name, request.email, request.password)
        return UserResponse(
            name=user["name"],
            email=user["email"],
            created_at=str(user.get("created_at", ""))
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/auth/login", response_model=UserResponse)
async def login(request: LoginRequest):
    """Authenticate user"""
    user = await authenticate_user(request.email, request.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    return UserResponse(
        name=user["name"],
        email=user["email"],
        created_at=str(user.get("created_at", ""))
    )


@app.get("/auth/user/{email}", response_model=UserResponse)
async def get_user(email: str):
    """Get user by email"""
    user = await get_user_by_email(email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return UserResponse(
        name=user["name"],
        email=user["email"],
        created_at=str(user.get("created_at", ""))
    )


# Conversation Endpoints
@app.post("/conversations")
async def create_new_conversation(request: ConversationRequest):
    """Create a new conversation"""
    try:
        conv = await create_conversation(request.user_email, request.title)
        return conv
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/conversations/{user_email}")
async def get_conversations(user_email: str):
    """Get all conversations for a user"""
    try:
        convs = await get_user_conversations(user_email)
        return {"conversations": convs}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.put("/conversations/{conversation_id}")
async def update_conversation(conversation_id: str, request: ConversationUpdateRequest):
    """Update conversation title"""
    try:
        success = await update_conversation_title(conversation_id, request.title)
        if not success:
            raise HTTPException(status_code=404, detail="Conversation not found")
        return {"success": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/conversations/{conversation_id}/{user_email}")
async def delete_conv(conversation_id: str, user_email: str):
    """Delete a conversation"""
    try:
        success = await delete_conversation(conversation_id, user_email)
        if not success:
            raise HTTPException(status_code=404, detail="Conversation not found")
        return {"success": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Message Endpoints
@app.post("/messages")
async def create_new_message(request: MessageRequest):
    """Create a new message"""
    try:
        msg = await create_message(
            request.conversation_id,
            request.role,
            request.content,
            request.evidence,
            request.metadata
        )
        return msg
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/messages/{conversation_id}")
async def get_messages(conversation_id: str):
    """Get all messages in a conversation"""
    try:
        msgs = await get_conversation_messages(conversation_id)
        return {"messages": msgs}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    print("🏥 Starting CareWise Unified API...")
    print("📍 API will be available at: http://localhost:8000")
    print("📖 Docs available at: http://localhost:8000/docs")
    print("🗄️  MongoDB connection: Ready")
    uvicorn.run(app, host="0.0.0.0", port=8000)
