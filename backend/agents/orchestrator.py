import asyncio
from typing import Dict, Any
from .market_agent import MarketAnalysisAgent
from .competitor_agent import CompetitorAgent
from .financial_agent import FinancialAgent
from .risk_agent import RiskAgent
from .llm_breakdown_agent import LLMBreakdownAgent
from .insight_agent import InsightAgent

class AnalysisOrchestrator:
    def __init__(self):
        self.breakdown_agent = LLMBreakdownAgent()
        self.market_agent = MarketAnalysisAgent()
        self.competitor_agent = CompetitorAgent()
        self.financial_agent = FinancialAgent()
        self.risk_agent = RiskAgent()
        self.insight_agent = InsightAgent()

    async def analyze_startup_idea(self, idea: str) -> Dict[str, Any]:
        # Step 1: Break down the idea into structured categories
        breakdown = await self.breakdown_agent.analyze(idea)
        
        # Step 2: Run specialized agents in parallel
        tasks = [
            self.market_agent.analyze(breakdown),
            self.competitor_agent.analyze(breakdown),
            self.financial_agent.analyze(breakdown),
            self.risk_agent.analyze(breakdown)
        ]
        
        market_data, competitor_data, financial_data, risk_data = await asyncio.gather(*tasks)
        
        # Step 3: Generate insights and recommendations
        combined_data = {
            "breakdown": breakdown,
            "market_analysis": market_data,
            "competition": competitor_data,
            "financial_projections": financial_data,
            "risks": risk_data
        }
        
        recommendation = await self.insight_agent.generate_recommendation(combined_data)
        
        return {
            "market_analysis": market_data,
            "competition": competitor_data,
            "financial_projections": financial_data,
            "risks": risk_data,
            "recommendation": recommendation
        }