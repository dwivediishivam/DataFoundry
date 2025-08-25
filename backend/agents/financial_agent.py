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
        # More dynamic base revenue calculation
        base_revenue = self._calculate_base_revenue(business_model, scope)
        
        # Adjust based on business model complexity
        if "marketplace" in business_model.lower() or "platform" in business_model.lower():
            base_revenue *= random.uniform(1.3, 1.8)  # Platform businesses scale better
        elif "saas" in business_model.lower() or "subscription" in business_model.lower():
            base_revenue *= random.uniform(1.1, 1.5)  # Recurring revenue premium
        elif "ai" in business_model.lower() or "automation" in business_model.lower():
            base_revenue *= random.uniform(1.2, 1.6)  # AI premium
        elif "hardware" in business_model.lower():
            base_revenue *= random.uniform(0.8, 1.2)  # Hardware has different economics
        
        # Adjust based on geographic scope with more variation
        scope_multipliers = {
            "global": random.uniform(1.8, 2.5),
            "national": random.uniform(0.9, 1.2),
            "regional": random.uniform(0.5, 0.8),
            "local": random.uniform(0.2, 0.5)
        }
        scope_multiplier = scope_multipliers.get(scope.lower(), 1.0)
        base_revenue *= scope_multiplier
        
        # Add some randomness to make each analysis unique
        base_revenue *= random.uniform(0.8, 1.3)
        
        # Calculate other metrics
        revenue_potential = round(base_revenue, 1)
        funding_required = round(revenue_potential * benchmarks["funding_ratio"] * random.uniform(0.8, 1.4), 1)
        break_even_timeline = benchmarks["break_even_months"]
        roi_projection = random.randint(*benchmarks["roi_range"])
        
        # More dynamic break-even calculation
        if funding_required > 150:  # Very high funding requirement
            break_even_timeline += random.randint(8, 12)
        elif funding_required > 75:  # High funding requirement
            break_even_timeline += random.randint(3, 8)
        elif funding_required < 25:  # Low funding requirement
            break_even_timeline -= random.randint(2, 6)
        
        # Adjust based on business model
        if "marketplace" in business_model.lower():
            break_even_timeline += random.randint(3, 8)  # Network effects take time
        elif "saas" in business_model.lower():
            break_even_timeline -= random.randint(1, 4)  # Faster to break even
        
        return {
            "revenue_potential": revenue_potential,
            "break_even_timeline": max(break_even_timeline, 6),  # Minimum 6 months
            "funding_required": max(funding_required, 5.0),  # Minimum $5M
            "roi_projection": roi_projection
        }

    def _calculate_base_revenue(self, business_model: str, scope: str) -> float:
        """Calculate base revenue with more realistic variation based on business model"""
        import random
        import hashlib
        
        # Create consistent seed based on business model for reproducible but varied results
        model_seed = int(hashlib.md5(business_model.encode()).hexdigest()[:8], 16)
        random.seed(model_seed)
        
        # More realistic revenue ranges based on actual business model characteristics
        if "marketplace" in business_model.lower() or "platform" in business_model.lower():
            # Platforms have high variability - can be huge or struggle
            revenue_tiers = [
                (0.2, random.uniform(20, 80)),     # 20% chance: struggling platforms
                (0.4, random.uniform(80, 300)),    # 40% chance: moderate success
                (0.3, random.uniform(300, 800)),   # 30% chance: successful platforms
                (0.1, random.uniform(800, 2000))   # 10% chance: unicorn platforms
            ]
        elif "saas" in business_model.lower() or "subscription" in business_model.lower():
            # SaaS has more predictable but varied growth
            revenue_tiers = [
                (0.3, random.uniform(10, 50)),     # 30% chance: small SaaS
                (0.4, random.uniform(50, 200)),    # 40% chance: mid-market SaaS
                (0.2, random.uniform(200, 500)),   # 20% chance: enterprise SaaS
                (0.1, random.uniform(500, 1200))   # 10% chance: major SaaS
            ]
        elif "hardware" in business_model.lower() or "product" in business_model.lower():
            # Hardware requires significant capital and volume
            revenue_tiers = [
                (0.4, random.uniform(50, 150)),    # 40% chance: niche hardware
                (0.3, random.uniform(150, 400)),   # 30% chance: moderate volume
                (0.2, random.uniform(400, 800)),   # 20% chance: mass market
                (0.1, random.uniform(800, 1500))   # 10% chance: major manufacturer
            ]
        elif "service" in business_model.lower() or "consulting" in business_model.lower():
            # Service businesses are more limited by human capital
            revenue_tiers = [
                (0.5, random.uniform(5, 30)),      # 50% chance: small service business
                (0.3, random.uniform(30, 100)),    # 30% chance: growing service firm
                (0.15, random.uniform(100, 300)),  # 15% chance: established firm
                (0.05, random.uniform(300, 600))   # 5% chance: major consultancy
            ]
        elif "ai" in business_model.lower() or "automation" in business_model.lower():
            # AI businesses have high potential but uncertain outcomes
            revenue_tiers = [
                (0.3, random.uniform(15, 60)),     # 30% chance: early AI startup
                (0.4, random.uniform(60, 250)),    # 40% chance: growing AI company
                (0.2, random.uniform(250, 600)),   # 20% chance: successful AI platform
                (0.1, random.uniform(600, 1500))   # 10% chance: AI unicorn
            ]
        else:
            # General technology business
            revenue_tiers = [
                (0.3, random.uniform(25, 100)),    # 30% chance: small tech business
                (0.4, random.uniform(100, 350)),   # 40% chance: growing tech company
                (0.2, random.uniform(350, 700)),   # 20% chance: successful tech firm
                (0.1, random.uniform(700, 1200))   # 10% chance: major tech company
            ]
        
        # Select revenue based on probability distribution
        rand_val = random.random()
        cumulative = 0
        revenue = 100  # Default fallback
        
        for prob, revenue_val in revenue_tiers:
            cumulative += prob
            if rand_val <= cumulative:
                revenue = revenue_val
                break
        
        # Reset random seed
        random.seed()
        return revenue