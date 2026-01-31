"""
Test script to verify backend API is working
"""

import requests
import json

API_URL = "http://localhost:8000"

def test_root():
    """Test root endpoint"""
    print("🧪 Testing root endpoint...")
    response = requests.get(f"{API_URL}/")
    print(f"✅ Status: {response.status_code}")
    print(f"📄 Response: {json.dumps(response.json(), indent=2)}")
    print()

def test_health():
    """Test health check endpoint"""
    print("🧪 Testing health endpoint...")
    response = requests.get(f"{API_URL}/health")
    print(f"✅ Status: {response.status_code}")
    print(f"📄 Response: {json.dumps(response.json(), indent=2)}")
    print()

def test_query():
    """Test query endpoint with a simple health query"""
    print("🧪 Testing query endpoint...")
    print("Query: 'What is diabetes?'")
    
    response = requests.post(
        f"{API_URL}/query",
        json={"query": "What is diabetes?"},
        headers={"Content-Type": "application/json"}
    )
    
    print(f"✅ Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"\n📊 Response Structure:")
        print(f"  - Query: {data.get('query')}")
        print(f"  - Intent: {data.get('execution_plan', {}).get('intent')}")
        print(f"  - Sources: {data.get('execution_plan', {}).get('sources')}")
        print(f"  - Evidence count: {len(data.get('evidence', []))}")
        print(f"  - Answer length: {len(data.get('answer', {}).get('answer', ''))} chars")
        print(f"  - Sources cited: {len(data.get('answer', {}).get('sources_used', []))}")
        print(f"\n💬 Answer Preview:")
        print(f"  {data.get('answer', {}).get('answer', '')[:200]}...")
    else:
        print(f"❌ Error: {response.text}")
    print()

if __name__ == "__main__":
    print("="*60)
    print("🏥 CAREWISE BACKEND API TEST")
    print("="*60)
    print()
    
    try:
        test_root()
        test_health()
        test_query()
        
        print("="*60)
        print("✅ All tests completed!")
        print("="*60)
        
    except requests.exceptions.ConnectionError:
        print("❌ ERROR: Could not connect to backend API")
        print("Make sure the backend is running on http://localhost:8000")
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
