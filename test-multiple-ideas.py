#!/usr/bin/env python3
"""
Test multiple different ideas to check for data variation
"""
import sys
import os
import asyncio
from datetime import datetime

# Add backend to path
sys.path.append('backend')

async def test_multiple_ideas():
    """Test multiple different startup ideas"""
    try:
        from backend.agents.orchestrator import AnalysisOrchestrator
        from dotenv import load_dotenv
        
        # Load environment variables
        load_dotenv('backend/.env')
        
        print("🚀 TESTING MULTIPLE STARTUP IDEAS FOR DATA VARIATION")
        print("=" * 80)
        print(f"⏰ Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 80)
        
        orchestrator = AnalysisOrchestrator()
        
        # Different startup ideas
        ideas = [
            "AI-powered social media content creation tool for small businesses",
            "Drone delivery service for medical supplies in rural areas",
            "Blockchain-based supply chain tracking for food safety",
            "Virtual reality fitness platform for home workouts",
            "Peer-to-peer car sharing app for urban areas"
        ]
        
        results = []
        
        for i, idea in enumerate(ideas, 1):
            print(f"\n🔍 TESTING IDEA {i}/5: {idea}")
            print("-" * 60)
            
            # Run analysis
            result = await orchestrator.analyze_startup_idea(idea)
            results.append((idea, result))
            
            # Display key metrics
            market = result.get('market_analysis', {})
            competition = result.get('competition', {})
            financial = result.get('financial_projections', {})
            recommendation = result.get('recommendation', {})
            
            print(f"   📊 TAM: ${market.get('tam', 0):,.0f}B | Growth: {market.get('growth_rate', 0):.1f}%")
            print(f"   🏆 Competitors: {len(competition.get('direct_competitors', []))} | Threat: {competition.get('threat_level', 'Unknown')}")
            print(f"   💰 Revenue: ${financial.get('revenue_potential', 0):,.1f}M | ROI: {financial.get('roi_projection', 0)}%")
            print(f"   🎯 Score: {recommendation.get('score', 0)}/100 | Verdict: {recommendation.get('verdict', 'Unknown')}")
        
        # Summary comparison
        print("\n" + "=" * 80)
        print("📈 COMPARISON SUMMARY")
        print("=" * 80)
        
        for i, (idea, result) in enumerate(results, 1):
            market = result.get('market_analysis', {})
            recommendation = result.get('recommendation', {})
            
            print(f"{i}. {idea[:50]}...")
            print(f"   TAM: ${market.get('tam', 0):,.0f}B | Score: {recommendation.get('score', 0)}/100")
        
        # Check for variation
        tams = [result[1].get('market_analysis', {}).get('tam', 0) for result in results]
        scores = [result[1].get('recommendation', {}).get('score', 0) for result in results]
        
        tam_variation = max(tams) - min(tams)
        score_variation = max(scores) - min(scores)
        
        print(f"\n📊 DATA VARIATION ANALYSIS:")
        print(f"   TAM Range: ${min(tams):,.0f}B - ${max(tams):,.0f}B (Variation: ${tam_variation:,.0f}B)")
        print(f"   Score Range: {min(scores)} - {max(scores)} (Variation: {score_variation})")
        
        if tam_variation > 1000 and score_variation > 20:
            print("   ✅ Good variation detected across different ideas")
        else:
            print("   ⚠️  Limited variation - may need improvement")
        
        print("\n" + "=" * 80)
        print("✅ Multiple idea analysis completed!")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_multiple_ideas())
    sys.exit(0 if success else 1)