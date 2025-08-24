import requests
import asyncio
from typing import Dict, Any, List
import random

class CompetitorAgent:
    def __init__(self):
        # Simulated competitor database
        self.competitor_db = {
            "logistics": [
                {"name": "UberEats", "funding": 8500, "market_share": 22},
                {"name": "DoorDash", "funding": 2500, "market_share": 35},
                {"name": "Zipline", "funding": 250, "market_share": 3}
            ],
            "technology": [
                {"name": "TechCorp", "funding": 1200, "market_share": 15},
                {"name": "InnovateLabs", "funding": 800, "market_share": 12},
                {"name": "StartupX", "funding": 450, "market_share": 8}
            ],
            "healthcare": [
                {"name": "HealthTech", "funding": 950, "market_share": 18},
                {"name": "MedConnect", "funding": 650, "market_share": 14},
                {"name": "CareAI", "funding": 320, "market_share": 9}
            ],
            "fintech": [
                {"name": "PayFlow", "funding": 1800, "market_share": 25},
                {"name": "FinanceAI", "funding": 1100, "market_share": 19},
                {"name": "CryptoBase", "funding": 750, "market_share": 12}
            ]
        }

    async def analyze(self, breakdown: Dict[str, Any]) -> Dict[str, Any]:
        industry = breakdown.get("industry", "Technology").lower()
        keywords = breakdown.get("keywords", [])
        
        competitors = self._get_competitors(industry, keywords)
        competitive_analysis = self._analyze_competitive_landscape(competitors, breakdown)
        
        return {
            "direct_competitors": competitors,
            "competitive_advantage": competitive_analysis["advantage"],
            "threat_level": competitive_analysis["threat_level"]
        }

    def _get_competitors(self, industry: str, keywords: list) -> List[Dict[str, Any]]:
        # Match industry to competitor data
        if any(term in industry for term in ["logistics", "delivery", "transport"]):
            return self.competitor_db["logistics"]
        elif any(term in industry for term in ["health", "medical"]):
            return self.competitor_db["healthcare"]
        elif any(term in industry for term in ["finance", "payment", "banking"]):
            return self.competitor_db["fintech"]
        elif any(term in industry for term in ["tech", "software", "digital"]):
            return self.competitor_db["technology"]
        else:
            # Generate random competitors for unknown industries
            return [
                {"name": f"Competitor{i+1}", "funding": random.randint(100, 2000), "market_share": random.randint(5, 30)}
                for i in range(3)
            ]

    def _analyze_competitive_landscape(self, competitors: List[Dict], breakdown: Dict) -> Dict[str, str]:
        total_funding = sum(comp["funding"] for comp in competitors)
        avg_market_share = sum(comp["market_share"] for comp in competitors) / len(competitors)
        
        # Determine competitive advantage based on business model
        business_model = breakdown.get("business_model", "").lower()
        key_features = breakdown.get("key_features", [])
        
        if "ai" in " ".join(key_features).lower() or "automation" in business_model:
            advantage = "Advanced AI and automation capabilities provide operational efficiency"
        elif "platform" in business_model or "marketplace" in business_model:
            advantage = "Network effects and platform scalability create competitive moats"
        elif "niche" in business_model or len(competitors) < 3:
            advantage = "First-mover advantage in underserved market segment"
        else:
            advantage = "Differentiated approach to customer experience and service delivery"
        
        # Determine threat level
        if total_funding > 5000 and avg_market_share > 20:
            threat_level = "High - Well-funded incumbents with significant market share"
        elif total_funding > 2000 or avg_market_share > 15:
            threat_level = "Medium - Established players but room for disruption"
        else:
            threat_level = "Low - Fragmented market with opportunity for new entrants"
        
        return {
            "advantage": advantage,
            "threat_level": threat_level
        }