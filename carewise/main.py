"""
CareWise - Unified Health Research Assistant
Main Pipeline - Handles both biomedical research and general health queries
"""

from datetime import datetime
from intelligence.planner import build_execution_plan
from data.router import execute_data_layer
from data.ranker import rank_evidence
from answer_engine.answer_generator import generate_grounded_answer


def run_pipeline(user_query: str, save_to_file=True):
    """Run the complete unified CareWise pipeline"""
    output_lines = []
    
    def log(message):
        """Print and save to output buffer"""
        print(message)
        output_lines.append(message)
    
    log("="*80)
    log("🏥 CAREWISE - UNIFIED HEALTH RESEARCH ASSISTANT")
    log("="*80)
    log(f"\n📝 Query: {user_query}\n")
    
    # Step 1: Query Intelligence
    log("─"*80)
    log("🧠 STEP 1: QUERY INTELLIGENCE")
    log("─"*80)
    
    try:
        plan = build_execution_plan(user_query)
        log(f"\n✅ Intent: {plan['intent']}")
        log(f"✅ Entities: {plan['entities']}")
        log(f"✅ Sources: {plan['sources']}")
    except Exception as e:
        log(f"❌ Step 1 Failed: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # Step 2: Data Acquisition
    log("\n" + "─"*80)
    log("📚 STEP 2: DATA ACQUISITION & NORMALIZATION")
    log("─"*80)
    
    try:
        results = execute_data_layer(plan)
        log(f"\n✅ Found {len(results)} normalized results")
    except Exception as e:
        log(f"❌ Step 2 Failed: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # Step 3: Evidence Ranking
    log("\n" + "─"*80)
    log("📊 STEP 3: EVIDENCE RANKING")
    log("─"*80)
    
    try:
        ranked_results = rank_evidence(results, plan)
        log(f"\n✅ Ranked {len(ranked_results)} evidence items by relevance")
    except Exception as e:
        log(f"❌ Step 3 Failed: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # Step 4: Generate grounded answer
    log("\n" + "─"*80)
    log("📝 STEP 4: LLM GROUNDED ANSWER")
    log("─"*80)
    
    try:
        answer_result = generate_grounded_answer(user_query, ranked_results)
        
        log("\n💡 ANSWER:")
        log("-" * 80)
        log(answer_result['answer'])
        
        log(f"\n📚 EVIDENCE SOURCES:")
        log("-" * 80)
        log(f"Evidence items used: {answer_result['evidence_count']}")
        log(f"Sources cited: {len(answer_result['sources_used'])}")
        
        for i, source in enumerate(answer_result['sources_used'], 1):
            # Clean up title for display
            title = source['title']
            if len(title) > 80:
                title = title[:77] + "..."
            log(f"  [{i}] {source['source']}: {title}")
            
    except Exception as e:
        log(f"❌ Step 4 Failed: {e}")
        import traceback
        traceback.print_exc()
    
    # Display top ranked results
    log("\n" + "="*80)
    log("🏆 TOP 5 RANKED EVIDENCE (for reference)")
    log("="*80)
    
    for i, result in enumerate(ranked_results[:5], 1):
        log(f"\n[{i}] Score: {result['score']:.3f} | Source: {result['source']}")
        log(f"    Title: {result['title']}")
        
        # Show more readable content preview
        content = result['content']
        if len(content) > 300:
            content_preview = content[:300] + "..."
        else:
            content_preview = content
        
        log(f"    Content: {content_preview}")
    
    log("\n" + "="*80)
    log(f"✅ SUCCESS! Complete pipeline executed")
    log("="*80)
    
    # Save detailed evidence to file
    if save_to_file:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"carewise_output_{timestamp}.txt"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("\n".join(output_lines))
        
        print(f"\n💾 Output saved to: {filename}")
    
    return output_lines


if __name__ == "__main__":
    print("="*80)
    print("🏥 CAREWISE - UNIFIED HEALTH RESEARCH ASSISTANT")
    print("="*80)
    print()
    
    print("📋 Example Queries:")
    print("\nBiomedical Research:")
    print("   1. Any ongoing CAR-T trials for melanoma?")
    print("   2. What are the side effects of Pembrolizumab?")
    print("   3. Latest research on CRISPR gene therapy for sickle cell disease")
    print("\nGeneral Health:")
    print("   4. What causes headaches and how to treat them?")
    print("   5. Information about diabetes prevention")
    print("   6. Global statistics on tuberculosis")
    print()
    
    user_query = input("🔍 Enter your query: ").strip()
    
    if not user_query:
        user_query = "What causes diabetes and how to manage it?"
        print(f"   ℹ️  Using default query: {user_query}")
    
    print()
    run_pipeline(user_query)
