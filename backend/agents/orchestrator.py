import asyncio
from typing import Dict, Any
from .portia_orchestrator import PortiaOrchestrator
from .llm_breakdown_agent import LLMBreakdownAgent

class AnalysisOrchestrator:
    def __init__(self):
        self.breakdown_agent = LLMBreakdownAgent()
        self.portia_orchestrator = PortiaOrchestrator()

    async def analyze_startup_idea(self, idea: str) -> Dict[str, Any]:
        print(f"🚀 Starting comprehensive analysis for idea: {idea[:100]}...")
        
        try:
            # Use our enhanced agent analysis directly (no Portia AI dependency)
            return await self._comprehensive_analysis(idea)
            
        except Exception as e:
            print(f"❌ Comprehensive analysis failed: {e}")
            print("🔄 Falling back to basic analysis...")
            # Fallback to basic analysis if main analysis fails
            return await self._fallback_analysis(idea)
    
    async def _comprehensive_analysis(self, idea: str) -> Dict[str, Any]:
        """Comprehensive analysis using our enhanced agents"""
        print("📊 Running comprehensive multi-agent analysis...")
        
        try:
            # Step 1: LLM Breakdown
            print("🔍 Step 1: Analyzing idea structure and categorization...")
            breakdown = await self.breakdown_agent.analyze(idea)
            print(f"   ✅ Industry identified: {breakdown.get('industry', 'Unknown')}")
            print(f"   ✅ Keywords extracted: {breakdown.get('keywords', [])[:3]}")
            
            # Import agents
            from .market_agent import MarketAnalysisAgent
            from .competitor_agent import CompetitorAgent
            from .financial_agent import FinancialAgent
            from .risk_agent import RiskAgent
            from .insight_agent import InsightAgent
            
            market_agent = MarketAnalysisAgent()
            competitor_agent = CompetitorAgent()
            financial_agent = FinancialAgent()
            risk_agent = RiskAgent()
            insight_agent = InsightAgent()
            
            # Step 2: Parallel Agent Analysis
            print("🔄 Step 2: Running parallel agent analysis...")
            print("   📈 Market analysis agent...")
            print("   🏆 Competitor analysis agent...")
            print("   💰 Financial projections agent...")
            print("   ⚠️  Risk assessment agent...")
            
            tasks = [
                market_agent.analyze(breakdown),
                competitor_agent.analyze(breakdown),
                financial_agent.analyze(breakdown),
                risk_agent.analyze(breakdown)
            ]
            
            market_data, competitor_data, financial_data, risk_data = await asyncio.gather(*tasks)
            
            print("   ✅ All agent analyses completed!")
            
            # Step 3: Generate Final Recommendation
            print("🎯 Step 3: Generating final recommendation and insights...")
            combined_data = {
                "breakdown": breakdown,
                "market_analysis": market_data,
                "competition": competitor_data,
                "financial_projections": financial_data,
                "risks": risk_data
            }
            
            recommendation = await insight_agent.generate_recommendation(combined_data)
            print(f"   ✅ Final score: {recommendation.get('score', 0)}/100")
            print(f"   ✅ Verdict: {recommendation.get('verdict', 'Unknown')}")
            
            return {
                "market_analysis": market_data,
                "competition": competitor_data,
                "financial_projections": financial_data,
                "risks": risk_data,
                "recommendation": recommendation
            }
            
        except Exception as e:
            print(f"❌ Comprehensive analysis failed: {e}")
            import traceback
            traceback.print_exc()
            raise e

    async def _fallback_analysis(self, idea: str) -> Dict[str, Any]:
        """Simple fallback analysis if comprehensive analysis fails"""
        try:
            breakdown = await self.breakdown_agent.analyze(idea)
            
            # Use the original simple agents as fallback
            from .market_agent import MarketAnalysisAgent
            from .competitor_agent import CompetitorAgent
            from .financial_agent import FinancialAgent
            from .risk_agent import RiskAgent
            from .insight_agent import InsightAgent
            
            market_agent = MarketAnalysisAgent()
            competitor_agent = CompetitorAgent()
            financial_agent = FinancialAgent()
            risk_agent = RiskAgent()
            insight_agent = InsightAgent()
            
            # Run agents in parallel
            tasks = [
                market_agent.analyze(breakdown),
                competitor_agent.analyze(breakdown),
                financial_agent.analyze(breakdown),
                risk_agent.analyze(breakdown)
            ]
            
            market_data, competitor_data, financial_data, risk_data = await asyncio.gather(*tasks)
            
            # Generate insights
            combined_data = {
                "breakdown": breakdown,
                "market_analysis": market_data,
                "competition": competitor_data,
                "financial_projections": financial_data,
                "risks": risk_data
            }
            
            recommendation = await insight_agent.generate_recommendation(combined_data)
            
            return {
                "market_analysis": market_data,
                "competition": competitor_data,
                "financial_projections": financial_data,
                "risks": risk_data,
                "recommendation": recommendation
            }
            
        except Exception as e:
            print(f"Fallback analysis also failed: {e}")
            return self._get_minimal_fallback()   
 
    def _get_minimal_fallback(self) -> Dict[str, Any]:
        """Minimal fallback if all analysis fails"""
        return {
            "market_analysis": {
                "tam": 1000.0,
                "sam": 100.0,
                "som": 10.0,
                "growth_rate": 5.0,
                "market_trends": ["Market analysis unavailable", "Please try again later"]
            },
            "competition": {
                "direct_competitors": [{"name": "Analysis unavailable", "funding": 0, "market_share": 0}],
                "competitive_advantage": "Analysis unavailable",
                "threat_level": "Unknown"
            },
            "financial_projections": {
                "revenue_potential": 50.0,
                "break_even_timeline": 24,
                "funding_required": 10.0,
                "roi_projection": 20
            },
            "risks": [
                {"category": "Analysis Risk", "level": "High", "description": "Unable to complete risk analysis"}
            ],
            "recommendation": {
                "score": 50,
                "verdict": "Analysis Incomplete",
                "key_insights": ["Please try the analysis again", "System temporarily unavailable"]
            }
        }