import google.generativeai as genai
import os
from typing import Dict, Any
import json
from dotenv import load_dotenv

class InsightAgent:
    def __init__(self):
        # Load environment variables
        load_dotenv()
        
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
            
        genai.configure(api_key=api_key)
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
        import random
        import hashlib
        
        # Create seed based on idea characteristics for consistent but varied scoring
        idea_characteristics = str(data.get("market_analysis", {}).get("tam", 0)) + str(data.get("competition", {}).get("threat_level", ""))
        score_seed = int(hashlib.md5(idea_characteristics.encode()).hexdigest()[:8], 16)
        random.seed(score_seed)
        
        # More dynamic base score with wider variation
        score = random.randint(35, 65)  # Wider base variation
        
        # Market factors (30% weight) - more nuanced scoring
        market = data.get("market_analysis", {})
        growth_rate = market.get("growth_rate", 0)
        tam = market.get("tam", 0)
        som = market.get("som", 0)
        
        # Growth rate scoring with more granularity
        if growth_rate > 15:
            score += random.randint(18, 22)
        elif growth_rate > 10:
            score += random.randint(12, 18)
        elif growth_rate > 7:
            score += random.randint(8, 14)
        elif growth_rate > 3:
            score += random.randint(4, 10)
        elif growth_rate > 0:
            score += random.randint(1, 6)
        else:
            score -= random.randint(5, 10)
        
        # TAM scoring with more variation
        if tam > 3000:
            score += random.randint(12, 16)
        elif tam > 1500:
            score += random.randint(8, 12)
        elif tam > 800:
            score += random.randint(5, 9)
        elif tam > 300:
            score += random.randint(2, 6)
        else:
            score -= random.randint(2, 5)
        
        # SOM consideration
        if som > 50:
            score += random.randint(3, 7)
        elif som > 20:
            score += random.randint(1, 4)
        
        # Competition factors (25% weight) - more dynamic
        competition = data.get("competition", {})
        threat_level = competition.get("threat_level", "").lower()
        competitors = competition.get("direct_competitors", [])
        
        if "low" in threat_level:
            score += random.randint(12, 18)
        elif "medium" in threat_level:
            score += random.randint(5, 12)
        elif "high" in threat_level:
            score -= random.randint(3, 8)
        
        # Consider competitor funding levels
        if competitors:
            avg_funding = sum(c.get("funding", 0) for c in competitors) / len(competitors)
            if avg_funding > 1000:  # Well-funded competitors
                score -= random.randint(2, 6)
            elif avg_funding < 200:  # Underfunded competitors
                score += random.randint(2, 5)
        
        # Financial factors (25% weight) - more nuanced
        financial = data.get("financial_projections", {})
        roi = financial.get("roi_projection", 0)
        break_even = financial.get("break_even_timeline", 24)
        revenue_potential = financial.get("revenue_potential", 0)
        
        # ROI scoring with more variation
        if roi > 40:
            score += random.randint(15, 20)
        elif roi > 30:
            score += random.randint(10, 15)
        elif roi > 20:
            score += random.randint(6, 12)
        elif roi > 10:
            score += random.randint(2, 8)
        else:
            score -= random.randint(2, 6)
        
        # Break-even timeline scoring
        if break_even < 12:
            score += random.randint(8, 12)
        elif break_even < 18:
            score += random.randint(5, 9)
        elif break_even < 30:
            score += random.randint(1, 5)
        else:
            score -= random.randint(3, 8)
        
        # Revenue potential consideration
        if revenue_potential > 500:
            score += random.randint(3, 7)
        elif revenue_potential > 200:
            score += random.randint(1, 4)
        
        # Risk factors (20% weight) - more detailed
        risks = data.get("risks", [])
        high_risks = sum(1 for risk in risks if risk.get("level") == "High")
        medium_risks = sum(1 for risk in risks if risk.get("level") == "Medium")
        
        if high_risks == 0:
            score += random.randint(8, 12)
        elif high_risks == 1:
            score += random.randint(3, 7)
        elif high_risks == 2:
            score -= random.randint(2, 5)
        elif high_risks >= 3:
            score -= random.randint(8, 15)
        
        # Medium risks also matter
        if medium_risks > 3:
            score -= random.randint(2, 5)
        elif medium_risks == 0:
            score += random.randint(1, 3)
        
        final_score = max(0, min(100, score))
        
        # Reset random seed
        random.seed()
        return final_score

    def _get_verdict(self, score: int) -> str:
        # More varied verdict options
        if score >= 85:
            return "Exceptional Opportunity"
        elif score >= 75:
            return "Highly Recommended"
        elif score >= 65:
            return "Recommended with Strategic Focus"
        elif score >= 55:
            return "Promising with Execution Risks"
        elif score >= 45:
            return "Moderate Potential - Needs Refinement"
        elif score >= 35:
            return "High Risk - Major Pivots Required"
        else:
            return "Not Viable in Current Form"

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