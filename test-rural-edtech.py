#!/usr/bin/env python3
"""
Test the Rural EdTech Kits idea specifically
"""
import sys
import os
import asyncio
from datetime import datetime

# Add backend to path
sys.path.append('backend')

async def test_rural_edtech_idea():
    """Test the Rural EdTech Kits idea"""
    try:
        from backend.agents.orchestrator import AnalysisOrchestrator
        from dotenv import load_dotenv
        
        # Load environment variables
        load_dotenv('backend/.env')
        
        print("📚 TESTING RURAL EDTECH KITS IDEA")
        print("=" * 80)
        print(f"⏰ Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 80)
        
        orchestrator = AnalysisOrchestrator()
        
        # Rural EdTech idea
        idea = "Rural EdTech Kits – Offline-first tablets with preloaded learning apps for schools with poor connectivity."
        
        print(f"💡 IDEA: {idea}")
        print("-" * 80)
        
        # Run analysis
        result = await orchestrator.analyze_startup_idea(idea)
        
        # Display detailed results
        print("\n📊 DETAILED ANALYSIS RESULTS:")
        print("=" * 60)
        
        # Market Analysis
        market = result.get('market_analysis', {})
        print(f"\n🏪 MARKET ANALYSIS:")
        print(f"   • TAM (Total Addressable Market): ${market.get('tam', 0):,.0f}B")
        print(f"   • SAM (Serviceable Addressable Market): ${market.get('sam', 0):,.1f}B")
        print(f"   • SOM (Serviceable Obtainable Market): ${market.get('som', 0):,.1f}B")
        print(f"   • Growth Rate: {market.get('growth_rate', 0):.1f}% annually")
        print(f"   • Market Trends:")
        for trend in market.get('market_trends', []):
            print(f"     - {trend}")
        
        # Competition Analysis
        competition = result.get('competition', {})
        print(f"\n🏆 COMPETITIVE LANDSCAPE:")
        print(f"   • Threat Level: {competition.get('threat_level', 'Unknown')}")
        print(f"   • Competitive Advantage: {competition.get('competitive_advantage', 'N/A')}")
        print(f"   • Direct Competitors:")
        for comp in competition.get('direct_competitors', []):
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
        for risk in risks:
            print(f"   • {risk.get('category', 'Unknown')} ({risk.get('level', 'Unknown')} Risk)")
            print(f"     {risk.get('description', 'No description')}")
        
        # Overall Recommendation
        recommendation = result.get('recommendation', {})
        print(f"\n🎯 OVERALL RECOMMENDATION:")
        print(f"   • Viability Score: {recommendation.get('score', 0)}/100")
        print(f"   • Verdict: {recommendation.get('verdict', 'Unknown')}")
        print(f"   • Key Insights:")
        for insight in recommendation.get('key_insights', []):
            print(f"     - {insight}")
        
        print("\n" + "=" * 80)
        print("✅ Rural EdTech analysis completed successfully!")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_rural_edtech_idea())
    sys.exit(0 if success else 1)