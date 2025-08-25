#!/usr/bin/env python3
"""
Test script for Portia AI integration
"""

import sys
import os
import asyncio

# Add backend to path
sys.path.append('backend')

async def test_portia_ai():
    """Test the Portia AI orchestrator"""
    try:
        from backend.agents.orchestrator import AnalysisOrchestrator
        
        print("🧪 Testing Portia AI Integration...")
        print(f"🔑 Using API Key: {os.getenv('PORTIA_API_KEY', 'Not found')[:20]}...")
        
        orchestrator = AnalysisOrchestrator()
        
        test_idea = """
        A SaaS platform that uses AI to automatically generate and optimize social media content 
        for small businesses. The platform analyzes brand voice, target audience, and trending topics 
        to create personalized posts across multiple platforms, with built-in scheduling and performance analytics.
        """
        
        print("🔄 Running Portia AI analysis...")
        result = await orchestrator.analyze_startup_idea(test_idea)
        
        print("✅ Analysis completed!")
        print(f"Overall Score: {result['recommendation']['score']}/100")
        print(f"Verdict: {result['recommendation']['verdict']}")
        print(f"Market Size (TAM): ${result['market_analysis']['tam']}B")
        print(f"Growth Rate: {result['market_analysis']['growth_rate']}%")
        print(f"Revenue Potential: ${result['financial_projections']['revenue_potential']}M")
        
        print("\n🔍 Key Insights:")
        for insight in result['recommendation']['key_insights'][:3]:
            print(f"  • {insight}")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Make sure to install dependencies: pip install -r backend/requirements.txt")
        return False
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv('backend/.env')
    
    success = asyncio.run(test_portia_ai())
    sys.exit(0 if success else 1)