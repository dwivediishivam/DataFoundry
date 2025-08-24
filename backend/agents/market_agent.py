import requests
import asyncio
from typing import Dict, Any
import random

class MarketAnalysisAgent:
    def __init__(self):
        self.world_bank_base = "https://api.worldbank.org/v2"
        self.statista_keywords = {
            "technology": {"tam": 4500, "growth": 8.2},
            "healthcare": {"tam": 2800, "growth": 6.5},
            "fintech": {"tam": 1200, "growth": 12.3},
            "logistics": {"tam": 850, "growth": 7.8},
            "ecommerce": {"tam": 3200, "growth": 9.1},
            "default": {"tam": 1000, "growth": 5.5}
        }

    async def analyze(self, breakdown: Dict[str, Any]) -> Dict[str, Any]:
        industry = breakdown.get("industry", "Technology").lower()
        keywords = breakdown.get("keywords", [])
        
        # Simulate market data based on industry
        market_data = self._get_market_estimates(industry, keywords)
        trends = await self._get_market_trends(industry, keywords)
        
        return {
            "tam": market_data["tam"],
            "sam": round(market_data["tam"] * 0.1, 1),  # 10% of TAM
            "som": round(market_data["tam"] * 0.01, 1),  # 1% of TAM
            "growth_rate": market_data["growth"],
            "market_trends": trends
        }

    def _get_market_estimates(self, industry: str, keywords: list) -> Dict[str, float]:
        # Match industry to market data
        for keyword in keywords:
            if keyword.lower() in self.statista_keywords:
                return self.statista_keywords[keyword.lower()]
        
        # Check industry categories
        if any(term in industry for term in ["tech", "software", "digital"]):
            return self.statista_keywords["technology"]
        elif any(term in industry for term in ["health", "medical", "pharma"]):
            return self.statista_keywords["healthcare"]
        elif any(term in industry for term in ["finance", "payment", "banking"]):
            return self.statista_keywords["fintech"]
        elif any(term in industry for term in ["logistics", "delivery", "transport"]):
            return self.statista_keywords["logistics"]
        elif any(term in industry for term in ["retail", "commerce", "marketplace"]):
            return self.statista_keywords["ecommerce"]
        else:
            return self.statista_keywords["default"]

    async def _get_market_trends(self, industry: str, keywords: list) -> list:
        # Simulate trend analysis based on industry
        trend_templates = {
            "technology": [
                "AI and machine learning adoption increasing by 25% annually",
                "Cloud infrastructure spending up 18% year-over-year",
                "Mobile-first solutions dominating market share"
            ],
            "logistics": [
                "Last-mile delivery costs rising 15% annually",
                "Drone delivery market expected to grow 57% CAGR",
                "Sustainability concerns driving green logistics adoption"
            ],
            "healthcare": [
                "Telemedicine adoption increased 3800% since 2020",
                "Digital health funding reached $29.1B in 2022",
                "Regulatory approval processes becoming more digital-friendly"
            ],
            "default": [
                "Digital transformation accelerating across industries",
                "Consumer behavior shifting towards on-demand services",
                "Regulatory landscape evolving to accommodate innovation"
            ]
        }
        
        # Select relevant trends
        if any(term in industry for term in ["logistics", "delivery", "transport"]):
            return trend_templates["logistics"]
        elif any(term in industry for term in ["health", "medical"]):
            return trend_templates["healthcare"]
        elif any(term in industry for term in ["tech", "software", "digital"]):
            return trend_templates["technology"]
        else:
            return trend_templates["default"]