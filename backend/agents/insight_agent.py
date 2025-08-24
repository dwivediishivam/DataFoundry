import google.generativeai as genai
import os
from typing import Dict, Any
import json

class InsightAgent:
    def __init__(self):
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        self.model = genai.GenerativeModel('gemini-1.5-flash')

    async def generate_recommendation(self, combined_data: Dict[str, Any]) -> Dict[str, Any]:
        # Calculate overall score based on multiple factors
        score = self._calculate_viability_score(combined_data)
        
        # Generate verdict based on score
        verdict = self._get_verdict(score)
        
        # Generate key insights
        insights = await self._generate_insights(combined_data, score)
        
        return {
            "score": score,
            "verdict": verdict,
            "key_insights": insights
        }

    def _calculate_viability_score(self, data: Dict[str, Any]) -> int:
        score = 50  # Base score
        
        # Market factors (30% weight)
        market = data.get("market_analysis", {})
        growth_rate = market.get("growth_rate", 0)
        tam = market.get("tam", 0)
        
        if growth_rate > 10:
            score += 15
        elif growth_rate > 5:
            score += 10
        elif growth_rate > 0:
            score += 5
        
        if tam > 1000:
            score += 10
        elif tam > 500:
            score += 5
        
        # Competition factors (25% weight)
        competition = data.get("competition", {})
        threat_level = competition.get("threat_level", "").lower()
        
        if "low" in threat_level:
            score += 15
        elif "medium" in threat_level:
            score += 8
        elif "high" in threat_level:
            score -= 5
        
        # Financial factors (25% weight)
        financial = data.get("financial_projections", {})
        roi = financial.get("roi_projection", 0)
        break_even = financial.get("break_even_timeline", 24)
        
        if roi > 30:
            score += 12
        elif roi > 20:
            score += 8
        elif roi > 10:
            score += 4
        
        if break_even < 18:
            score += 8
        elif break_even < 24:
            score += 4
        
        # Risk factors (20% weight)
        risks = data.get("risks", [])
        high_risks = sum(1 for risk in risks if risk.get("level") == "High")
        
        if high_risks == 0:
            score += 10
        elif high_risks == 1:
            score += 5
        elif high_risks >= 3:
            score -= 10
        
        return max(0, min(100, score))

    def _get_verdict(self, score: int) -> str:
        if score >= 75:
            return "Highly Recommended"
        elif score >= 60:
            return "Recommended with Caution"
        elif score >= 40:
            return "Requires Significant Improvements"
        else:
            return "Not Recommended"

    async def _generate_insights(self, data: Dict[str, Any], score: int) -> list:
        market = data.get("market_analysis", {})
        competition = data.get("competition", {})
        financial = data.get("financial_projections", {})
        risks = data.get("risks", [])
        
        insights = []
        
        # Market insights
        if market.get("growth_rate", 0) > 8:
            insights.append(f"Strong market growth of {market.get('growth_rate')}% annually indicates favorable timing")
        
        tam = market.get("tam", 0)
        som = market.get("som", 0)
        if som > 10:
            insights.append(f"Serviceable obtainable market of ${som}B represents significant revenue opportunity")
        
        # Competition insights
        threat_level = competition.get("threat_level", "").lower()
        if "low" in threat_level:
            insights.append("Low competitive threat provides opportunity for market entry and growth")
        elif "high" in threat_level:
            insights.append("High competitive threat requires strong differentiation strategy")
        
        # Financial insights
        roi = financial.get("roi_projection", 0)
        if roi > 25:
            insights.append(f"Projected ROI of {roi}% exceeds industry benchmarks")
        
        break_even = financial.get("break_even_timeline", 24)
        if break_even < 18:
            insights.append(f"Fast break-even timeline of {break_even} months reduces investment risk")
        
        # Risk insights
        high_risks = [risk for risk in risks if risk.get("level") == "High"]
        if len(high_risks) > 2:
            insights.append("Multiple high-risk factors require careful mitigation planning")
        elif len(high_risks) == 0:
            insights.append("Low risk profile makes this an attractive investment opportunity")
        
        # Overall recommendation insight
        if score >= 70:
            insights.append("Strong fundamentals across market, competition, and financial metrics")
        elif score < 50:
            insights.append("Significant challenges in multiple areas require strategic pivots")
        
        return insights[:6]  # Limit to 6 key insights