"""Main CareWise Bio Pipeline"""

from datetime import datetime
from carewise import build_execution_plan, execute_data_layer, generate_grounded_answer
from carewise.data import rank_evidence


def run_pipeline(user_query: str, save_to_file=True):
    """Run the complete CareWise Bio pipeline"""
    # Prepare output buffer
    output_lines = []
    
    def log(message):
        """Print and save to output buffer"""
        print(message)
        output_lines.append(message)
    
    log("="*80)
    log("🧬 CAREWISE BIO")
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
            log(f"  [{i}] {source['source']}: {source['title'][:60]}...")
            
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
        log(f"    Title: {result['title'][:70]}...")
        content_preview = result['content'][:150] if result['content'] else "No content"
        log(f"    Content: {content_preview}...")
    
    log("\n" + "="*80)
    log(f"✅ SUCCESS! Complete pipeline executed")
    log("="*80)
    
    # Save detailed evidence to file
    if save_to_file:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"carewise_output_{timestamp}.txt"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("="*80 + "\n")
            f.write("🏆 TOP 5 RANKED EVIDENCE - FULL DETAILS\n")
            f.write("="*80 + "\n\n")
            f.write(f"Query: {user_query}\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("="*80 + "\n\n")
            
            for i, result in enumerate(ranked_results[:5], 1):
                f.write(f"\n{'='*80}\n")
                f.write(f"[{i}] EVIDENCE ITEM - Score: {result['score']:.3f}\n")
                f.write(f"{'='*80}\n\n")
                
                # Source
                f.write(f"Source: {result['source']}\n\n")
                
                # Title
                f.write(f"Title:\n")
                f.write(f"{result['title']}\n\n")
                
                # Content as formatted paragraphs
                f.write(f"Summary:\n")
                content = result['content']
                
                # Format content into readable paragraphs
                # Split by common delimiters and format
                if content:
                    # Handle common formatting issues
                    content = content.replace('. ', '.\n\n')  # New paragraph after sentences
                    content = content.replace('? ', '?\n\n')
                    content = content.replace('! ', '!\n\n')
                    
                    # Remove excessive newlines
                    while '\n\n\n' in content:
                        content = content.replace('\n\n\n', '\n\n')
                    
                    # Write formatted content with indentation
                    for paragraph in content.split('\n\n'):
                        if paragraph.strip():
                            f.write(f"{paragraph.strip()}\n\n")
                else:
                    f.write("No content available.\n\n")
                
                # Add metadata if available
                if 'metadata' in result and result['metadata']:
                    f.write(f"\nMetadata:\n")
                    for key, value in result['metadata'].items():
                        f.write(f"  • {key}: {value}\n")
                    f.write("\n")
                
                # Add score breakdown
                if 'scores_breakdown' in result:
                    f.write(f"Relevance Metrics:\n")
                    for key, value in result['scores_breakdown'].items():
                        f.write(f"  • {key.replace('_', ' ').title()}: {value:.3f}\n")
                    f.write("\n")
        
        print(f"\n💾 Detailed output saved to: {filename}")
    
    return output_lines


if __name__ == "__main__":
    print("="*80)
    print("🧬 CAREWISE BIO - FULL PIPELINE")
    print("="*80)
    print()
    
    # Example queries
    print("📋 Example Queries:")
    print("   1. Any ongoing CAR-T trials for melanoma?")
    print("   2. What are the side effects of Pembrolizumab?")
    print("   3. Latest research on CRISPR gene therapy for sickle cell disease")
    print("   4. Clinical trials for Alzheimer's disease treatment")
    print("   5. Safety information for Metformin")
    print()
    
    user_query = input("🔍 Enter your query: ").strip()
    
    if not user_query:
        user_query = "Any ongoing CAR-T trials for melanoma?"
        print(f"   ℹ️  Using default query: {user_query}")
    
    print()
    run_pipeline(user_query)
