import asyncio
from typing import Dict, Any
import random

class FinancialAgent:
    def __init__(self):
        # Industry-specific financial benchmarks
        self.financial_benchmarks = {
            "technology": {
                "revenue_multiple": 8.5,
                "break_even_months": 18,
                "funding_ratio": 0.15,
                "roi_range": (25, 45)
            },
            "logistics": {
                "revenue_multiple": 12.0,
                "break_even_months": 24,
                "funding_ratio": 0.25,
                "roi_range": (15, 35)
            },
            "healthcare": {
                "revenue_multiple": 15.0,
                "break_even_months": 30,
                "funding_ratio": 0.35,
                "roi_range": (20, 40)
            },
            "fintech": {
                "revenue_multiple": 6.5,
                "break_even_months": 15,
                "funding_ratio": 0.12,
                "roi_range": (30, 50)
            },
            "default": {
                "revenue_multiple": 10.0,
                "break_even_months": 20,
                "funding_ratio": 0.20,
                "roi_range": (20, 35)
            }
        }

    async def analyze(self, breakdown: Dict[str, Any]) -> Dict[str, Any]:
        industry = breakdown.get("industry", "Technology").lower()
        business_model = breakdown.get("business_model", "")
        geographic_scope = breakdown.get("geographic_scope", "National")
        
        benchmarks = self._get_financial_benchmarks(industry)
        projections = self._calculate_projections(benchmarks, business_model, geographic_scope)
        
        return projections

    def _get_financial_benchmarks(self, industry: str) -> Dict[str, Any]:
        if any(term in industry for term in ["logistics", "delivery", "transport"]):
            return self.financial_benchmarks["logistics"]
        elif any(term in industry for term in ["health", "medical"]):
            return self.financial_benchmarks["healthcare"]
        elif any(term in industry for term in ["finance", "payment", "banking"]):
            return self.financial_benchmarks["fintech"]
        elif any(term in industry for term in ["tech", "software", "digital"]):
            return self.financial_benchmarks["technology"]
        else:
            return self.financial_benchmarks["default"]

    def _calculate_projections(self, benchmarks: Dict, business_model: str, scope: str) -> Dict[str, Any]:
        # Base revenue potential calculation
        base_revenue = random.randint(50, 500)  # Base in millions
        
        # Adjust based on business model
        if "marketplace" in business_model.lower() or "platform" in business_model.lower():
            base_revenue *= 1.5  # Platform businesses scale better
        elif "saas" in business_model.lower() or "subscription" in business_model.lower():
            base_revenue *= 1.3  # Recurring revenue premium
        
        # Adjust based on geographic scope
        scope_multipliers = {
            "global": 2.0,
            "national": 1.0,
            "regional": 0.6,
            "local": 0.3
        }
        scope_multiplier = scope_multipliers.get(scope.lower(), 1.0)
        base_revenue *= scope_multiplier
        
        # Calculate other metrics
        revenue_potential = round(base_revenue, 1)
        funding_required = round(revenue_potential * benchmarks["funding_ratio"], 1)
        break_even_timeline = benchmarks["break_even_months"]
        roi_projection = random.randint(*benchmarks["roi_range"])
        
        # Adjust break-even based on funding
        if funding_required > 100:  # High funding requirement
            break_even_timeline += 6
        elif funding_required < 20:  # Low funding requirement
            break_even_timeline -= 3
        
        return {
            "revenue_potential": revenue_potential,
            "break_even_timeline": max(break_even_timeline, 6),  # Minimum 6 months
            "funding_required": funding_required,
            "roi_projection": roi_projection
        }