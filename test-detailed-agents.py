#!/usr/bin/env python3
"""
Detailed test script to show console logs for each agent's output
"""
import sys
import os
import asyncio
import json
from datetime import datetime

# Add backend to path
sys.path.append('backend')

async def test_detailed_agents():
    """Test agents with detailed console logging"""
    try:
        from backend.agents.orchestrator import AnalysisOrchestrator
        from dotenv import load_dotenv
        
        # Load environment variables
        load_dotenv('backend/.env')
        
        print("🧪 DETAILED AGENT TESTING")
        print("=" * 80)
        print(f"⏰ Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 80)
        
        orchestrator = AnalysisOrchestrator()
        
        # Test different startup ideas
        test_ideas = [
            {
                "name": "AI Social Media Manager",
                "description": "A SaaS platform that uses advanced AI to automatically generate, schedule, and optimize social media content for small businesses, including hashtag optimization, audience targeting, and performance analytics."
            },
            {
                "name": "Telemedicine Platform", 
                "description": "A comprehensive healthcare telemedicine platform connecting patients with doctors for remote consultations, including AI-powered symptom assessment, prescription management, and integration with wearable health devices."
            },
            {
                "name": "Fintech Payment Solution",
                "description": "A mobile payment app specifically designed for small businesses with integrated accounting, inventory management, customer loyalty programs, and AI-powered financial insights and cash flow predictions."
            },
            {
                "name": "Drone Medical Delivery",
                "description": "An autonomous drone delivery service specializing in urgent medical supply delivery to hospitals, clinics, and remote areas, with real-time tracking, temperature-controlled cargo, and regulatory compliance systems."
            }
        ]
        
        results = []
        
        for i, idea in enumerate(test_ideas):
            print(f"\n🚀 ANALYZING IDEA {i+1}/4: {idea['name']}")
            print("=" * 60)
            print(f"📝 Description: {idea['description']}")
            print("-" * 60)
            
            # Run analysis
            result = await orchestrator.analyze_startup_idea(idea['description'])
            
            # Log detailed results
            print("\n📊 DETAILED ANALYSIS RESULTS:")
            print("-" * 40)
            
            # Market Analysis
            market = result.get('market_analysis', {})
            print(f"🏪 MARKET ANALYSIS:")
            print(f"   • TAM (Total Addressable Market): ${market.get('tam', 0):,.0f}B")
            print(f"   • SAM (Serviceable Addressable Market): ${market.get('sam', 0):,.1f}B")
            print(f"   • SOM (Serviceable Obtainable Market): ${market.get('som', 0):,.1f}B")
            print(f"   • Growth Rate: {market.get('growth_rate', 0):.1f}% annually")
            print(f"   • Market Trends:")
            for trend in market.get('market_trends', [])[:3]:
                print(f"     - {trend}")
            
            # Competition Analysis
            competition = result.get('competition', {})
            print(f"\n🏆 COMPETITIVE LANDSCAPE:")
            print(f"   • Threat Level: {competition.get('threat_level', 'Unknown')}")
            print(f"   • Competitive Advantage: {competition.get('competitive_advantage', 'N/A')}")
            print(f"   • Direct Competitors:")
            for comp in competition.get('direct_competitors', [])[:3]:
                print(f"     - {comp.get('name', 'Unknown')}: ${comp.get('funding', 0)}M funding, {comp.get('market_share', 0)}% market share")
            
            # Financial Projections
            financial = result.get('financial_projections', {})
            print(f"\n💰 FINANCIAL PROJECTIONS:")
            print(f"   • Revenue Potential: ${financial.get('revenue_potential', 0):,.1f}M")
            print(f"   • Funding Required: ${financial.get('funding_required', 0):,.1f}M")
            print(f"   • Break-even Timeline: {financial.get('break_even_timeline', 0)} months")
            print(f"   • ROI Projection: {financial.get('roi_projection', 0)}%")
            
            # Risk Analysis
            risks = result.get('risks', [])
            print(f"\n⚠️  RISK ANALYSIS ({len(risks)} risks identified):")
            for risk in risks[:4]:
                print(f"   • {risk.get('category', 'Unknown')} ({risk.get('level', 'Unknown')} Risk)")
                print(f"     {risk.get('description', 'No description')}")
            
            # Overall Recommendation
            recommendation = result.get('recommendation', {})
            print(f"\n🎯 OVERALL RECOMMENDATION:")
            print(f"   • Viability Score: {recommendation.get('score', 0)}/100")
            print(f"   • Verdict: {recommendation.get('verdict', 'Unknown')}")
            print(f"   • Key Insights:")
            for insight in recommendation.get('key_insights', [])[:3]:
                print(f"     - {insight}")
            
            print("\n" + "=" * 60)
            
            # Store results for comparison
            results.append({
                "name": idea['name'],
                "tam": market.get('tam', 0),
                "growth_rate": market.get('growth_rate', 0),
                "score": recommendation.get('score', 0),
                "verdict": recommendation.get('verdict', 'Unknown'),
                "revenue": financial.get('revenue_potential', 0),
                "funding": financial.get('funding_required', 0),
                "threat_level": competition.get('threat_level', 'Unknown'),
                "risks_count": len(risks)
            })
        
        # Final comparison
        print("\n🔍 COMPARATIVE ANALYSIS SUMMARY")
        print("=" * 80)
        print(f"{'Idea':<25} | {'TAM':<8} | {'Growth':<7} | {'Score':<6} | {'Revenue':<9} | {'Funding':<8} | {'Risks':<6}")
        print("-" * 80)
        
        for result in results:
            print(f"{result['name']:<25} | ${result['tam']:<7.0f}B | {result['growth_rate']:<6.1f}% | {result['score']:<6}/100 | ${result['revenue']:<8.1f}M | ${result['funding']:<7.1f}M | {result['risks_count']:<6}")
        
        # Check for variety in results
        tams = [r['tam'] for r in results]
        scores = [r['score'] for r in results]
        revenues = [r['revenue'] for r in results]
        
        print("\n📈 ANALYSIS QUALITY CHECK:")
        print(f"   • TAM Range: ${min(tams):.0f}B - ${max(tams):.0f}B (Variation: {max(tams) - min(tams):.0f}B)")
        print(f"   • Score Range: {min(scores)} - {max(scores)} (Variation: {max(scores) - min(scores)})")
        print(f"   • Revenue Range: ${min(revenues):.1f}M - ${max(revenues):.1f}M (Variation: ${max(revenues) - min(revenues):.1f}M)")
        
        if len(set(tams)) > 1 and len(set(scores)) > 1 and len(set(revenues)) > 1:
            print("   ✅ SUCCESS: Analysis shows good variation across different ideas!")
        else:
            print("   ❌ ISSUE: Analysis results are too similar - needs improvement!")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_detailed_agents())
    sys.exit(0 if success else 1)