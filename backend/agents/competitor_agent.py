import requests
import asyncio
from typing import Dict, Any, List
import random
import os
from dotenv import load_dotenv

class CompetitorAgent:
    def __init__(self):
        load_dotenv()
        self.serpapi_key = os.getenv("SERPAPI_KEY")
        
        # Fallback competitor database
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
        business_model = breakdown.get("business_model", "")
        
        # Fetch real competitor data
        competitors = await self._fetch_real_competitors(industry, keywords, business_model)
        competitive_analysis = self._analyze_competitive_landscape(competitors, breakdown)
        
        return {
            "direct_competitors": competitors,
            "competitive_advantage": competitive_analysis["advantage"],
            "threat_level": competitive_analysis["threat_level"]
        }

    async def _fetch_real_competitors(self, industry: str, keywords: list, business_model: str) -> List[Dict[str, Any]]:
        """Fetch real competitor data using SerpAPI or fallback to curated list"""
        print(f"🔍 Fetching competitors for industry: {industry}, keywords: {keywords}")
        
        # Try search first, then fallback to curated competitors
        try:
            if self.serpapi_key:
                print("🔍 Attempting to search for competitors using SerpAPI...")
                competitors = await self._search_competitors(industry, keywords, business_model)
                if len(competitors) >= 2:
                    print(f"✅ Found {len(competitors)} competitors via search")
                    return competitors
                else:
                    print("⚠️ Search returned insufficient competitors, using curated fallback")
            else:
                print("⚠️ No SerpAPI key available, using curated competitors")
        except Exception as e:
            print(f"❌ Search failed: {e}, using curated competitors")
        
        # Use curated competitors as fallback
        print("🔄 Using curated competitors for better industry matching")
        return self._get_fallback_competitors(industry, keywords)
        


    async def _search_competitors(self, industry: str, keywords: list, business_model: str) -> List[Dict[str, Any]]:
        """Search for competitors using SerpAPI"""
        if not self.serpapi_key:
            raise Exception("SerpAPI key not available")
        
        # Create search query for competitors
        search_terms = [industry] + keywords[:2]  # Limit keywords
        query = f"{' '.join(search_terms)} companies startups competitors funding"
        
        params = {
            "engine": "google",
            "q": query,
            "api_key": self.serpapi_key,
            "num": 8
        }
        
        try:
            response = requests.get("https://serpapi.com/search", params=params, timeout=10)
            data = response.json()
            
            # Extract competitor information
            competitors = self._extract_competitor_info(data, industry)
            
            return competitors
        except Exception as e:
            print(f"Competitor search failed: {e}")
            raise e

    def _extract_competitor_info(self, search_data: dict, industry: str) -> List[Dict[str, Any]]:
        """Extract competitor information from search results with better company names"""
        competitors = []
        organic_results = search_data.get("organic_results", [])
        
        import re
        
        # India-centric and global competitors by industry
        known_competitors = {
            "technology": ["Infosys", "TCS", "Wipro", "HCL Technologies", "Tech Mahindra", "Zoho", "Freshworks", "Microsoft", "Google", "Amazon"],
            "healthcare": ["Practo", "1mg", "PharmEasy", "Netmeds", "Apollo 24/7", "Lybrate", "DocsApp", "Teladoc", "Amwell"],
            "fintech": ["Paytm", "PhonePe", "Razorpay", "Pine Labs", "Mobikwik", "BharatPe", "CRED", "Stripe", "PayPal"],
            "logistics": ["Swiggy", "Zomato", "Dunzo", "Porter", "BlackBuck", "Rivigo", "Delhivery", "Blue Dart", "FedEx"],
            "ecommerce": ["Flipkart", "Amazon India", "Myntra", "Nykaa", "BigBasket", "Grofers", "Meesho", "Shopify"],
            "electric vehicle": ["Ather Energy", "Ola Electric", "Hero Electric", "Mahindra Electric", "Tata Motors EV", "ChargePoint", "Shell Recharge"],
            "automotive": ["Tata Motors", "Mahindra", "Maruti Suzuki", "Hyundai India", "Hero MotoCorp", "Bajaj Auto", "TVS Motor"],
            "energy": ["Reliance Industries", "Adani Green", "Tata Power", "NTPC", "Coal India", "ONGC", "Indian Oil"],
            "mobility": ["Ola", "Uber India", "Rapido", "Bounce", "Yulu", "Vogo", "Quick Ride", "BlaBlaCar India"],
            "mapping": ["MapmyIndia", "Google Maps", "Ola Maps", "HERE Technologies", "TomTom", "Garmin"],
            "education": ["BYJU'S", "Unacademy", "Vedantu", "Toppr", "WhiteHat Jr", "Simplilearn", "UpGrad", "Coursera", "Khan Academy"],
            "edtech": ["BYJU'S", "Unacademy", "Vedantu", "Toppr", "Doubtnut", "Embibe", "Meritnation", "Khan Academy", "Coursera"],
            "rural": ["ITC e-Choupal", "Mahindra Agri Solutions", "Tata Kisan Sansar", "Digital Green", "CropIn", "AgroStar"],
            "agriculture": ["ITC e-Choupal", "Mahindra Agri Solutions", "UPL", "Bayer CropScience", "Syngenta India", "IFFCO"],
            "tablets": ["Samsung India", "Lenovo India", "Apple India", "Xiaomi India", "Realme", "OnePlus", "Micromax"]
        }
        
        # First try to extract real company names from search results
        for result in organic_results[:5]:
            snippet = result.get("snippet", "")
            title = result.get("title", "")
            text = f"{title} {snippet}"
            
            # Look for known competitors in the text
            industry_competitors = []
            for key, comp_list in known_competitors.items():
                if key in industry.lower():
                    industry_competitors = comp_list
                    break
            
            # Check if any known competitors are mentioned
            for comp in industry_competitors:
                if comp.lower() in text.lower() and comp not in [c["name"] for c in competitors]:
                    # Extract or estimate funding
                    funding_matches = re.findall(r'\$(\d+\.?\d*)\s*(?:million|billion)', text.lower())
                    if funding_matches:
                        funding = float(funding_matches[0])
                        if 'billion' in text.lower():
                            funding *= 1000
                    else:
                        # Estimate based on company size
                        funding = self._estimate_company_funding(comp, industry)
                    
                    market_share = self._estimate_market_share(funding, industry)
                    
                    competitors.append({
                        "name": comp,
                        "funding": int(funding),
                        "market_share": market_share
                    })
                    
                    if len(competitors) >= 4:
                        break
            
            if len(competitors) >= 4:
                break
        
        # If we still don't have enough, add some realistic competitors
        if len(competitors) < 3:
            # Better industry matching for competitors
            industry_competitors = known_competitors.get("technology", known_competitors["technology"])
            
            # Enhanced multi-keyword matching for better industry detection
            industry_lower = industry.lower()
            if any(term in industry_lower for term in ["education", "edtech", "learning", "school", "student"]):
                industry_competitors = known_competitors["edtech"]
            elif any(term in industry_lower for term in ["rural", "village", "farming", "agriculture"]):
                industry_competitors = known_competitors["rural"]
            elif any(term in industry_lower for term in ["tablet", "device", "hardware", "electronics"]):
                industry_competitors = known_competitors["tablets"]
            elif any(term in industry_lower for term in ["electric", "ev", "charging", "battery"]):
                industry_competitors = known_competitors["electric vehicle"]
            elif any(term in industry_lower for term in ["automotive", "car", "auto", "vehicle"]):
                industry_competitors = known_competitors["automotive"]
            elif any(term in industry_lower for term in ["energy", "power", "utility", "renewable"]):
                industry_competitors = known_competitors["energy"]
            elif any(term in industry_lower for term in ["mobility", "transport", "ride", "travel"]):
                industry_competitors = known_competitors["mobility"]
            elif any(term in industry_lower for term in ["map", "navigation", "location", "gps"]):
                industry_competitors = known_competitors["mapping"]
            elif any(term in industry_lower for term in ["health", "medical", "telemedicine", "healthcare"]):
                industry_competitors = known_competitors["healthcare"]
            elif any(term in industry_lower for term in ["finance", "payment", "banking", "fintech"]):
                industry_competitors = known_competitors["fintech"]
            elif any(term in industry_lower for term in ["logistics", "delivery", "courier"]):
                industry_competitors = known_competitors["logistics"]
            elif any(term in industry_lower for term in ["commerce", "retail", "marketplace", "ecommerce"]):
                industry_competitors = known_competitors["ecommerce"]
            elif any(term in industry_lower for term in ["tech", "software", "digital", "saas", "ai"]):
                industry_competitors = known_competitors["technology"]
            
            # Add random competitors from the industry list
            import random
            remaining_competitors = [c for c in industry_competitors if c not in [comp["name"] for comp in competitors]]
            
            while len(competitors) < 3 and remaining_competitors:
                comp = random.choice(remaining_competitors)
                remaining_competitors.remove(comp)
                
                funding = self._estimate_company_funding(comp, industry)
                market_share = self._estimate_market_share(funding, industry)
                
                competitors.append({
                    "name": comp,
                    "funding": int(funding),
                    "market_share": market_share
                })
        
        # If we still don't have competitors, force add from the correct industry
        if len(competitors) == 0:
            print(f"No competitors found via search, using industry defaults for: {industry}")
            # Force add 3 competitors from the correct industry
            import random
            for i in range(3):
                if i < len(industry_competitors):
                    comp = industry_competitors[i]
                    funding = self._estimate_company_funding(comp, industry)
                    market_share = self._estimate_market_share(funding, industry)
                    
                    competitors.append({
                        "name": comp,
                        "funding": int(funding),
                        "market_share": market_share
                    })
        
        return competitors

    def _estimate_company_funding(self, company: str, industry: str) -> float:
        """Estimate funding based on company name and industry with more realistic variation"""
        import random
        import hashlib
        
        # Create a seed based on company name for consistent but varied results
        seed = int(hashlib.md5(company.encode()).hexdigest()[:8], 16)
        random.seed(seed)
        
        # Well-known companies get higher funding estimates
        big_tech = ["Microsoft", "Google", "Amazon", "Meta", "Apple", "Salesforce", "Adobe", "Oracle", "IBM"]
        established = ["Square", "Stripe", "PayPal", "Teladoc", "Shopify", "UberEats", "DoorDash", "Paytm", "PhonePe", "Flipkart"]
        
        # Indian unicorns and major companies
        indian_major = ["Paytm", "PhonePe", "Razorpay", "BYJU'S", "Unacademy", "Ola", "Swiggy", "Zomato", "Flipkart", "Nykaa"]
        
        if company in big_tech:
            funding = random.randint(2000, 8000)  # $2B-8B (more realistic for specific divisions)
        elif company in established or company in indian_major:
            funding = random.randint(200, 2000)   # $200M-2B
        else:
            # More varied funding for smaller companies
            funding_tiers = [
                (0.1, random.randint(5, 50)),      # 10% chance: $5M-50M (early stage)
                (0.3, random.randint(50, 200)),    # 30% chance: $50M-200M (growth stage)
                (0.4, random.randint(200, 800)),   # 40% chance: $200M-800M (mature)
                (0.2, random.randint(800, 2000))   # 20% chance: $800M-2B (late stage)
            ]
            
            rand_val = random.random()
            cumulative = 0
            for prob, funding_val in funding_tiers:
                cumulative += prob
                if rand_val <= cumulative:
                    funding = funding_val
                    break
            else:
                funding = random.randint(100, 500)  # Default fallback
        
        # Reset random seed to avoid affecting other random calls
        random.seed()
        return float(funding)

    def _estimate_market_share(self, funding: float, industry: str) -> int:
        """Estimate market share based on funding and industry with more realistic distribution"""
        import random
        
        # More realistic market share distribution - most markets are fragmented
        if funding > 2000:  # > $2B
            base_share = random.randint(15, 30)
        elif funding > 1000:  # > $1B
            base_share = random.randint(10, 20)
        elif funding > 500:  # > $500M
            base_share = random.randint(6, 15)
        elif funding > 200:  # > $200M
            base_share = random.randint(4, 12)
        elif funding > 50:   # > $50M
            base_share = random.randint(2, 8)
        else:
            base_share = random.randint(1, 5)
        
        # Industry-specific adjustments for more realism
        industry_lower = industry.lower()
        if any(term in industry_lower for term in ["technology", "software", "saas"]):
            base_share = int(base_share * random.uniform(0.6, 0.9))  # Very fragmented
        elif any(term in industry_lower for term in ["healthcare", "medical"]):
            base_share = int(base_share * random.uniform(0.8, 1.1))  # Moderately consolidated
        elif any(term in industry_lower for term in ["fintech", "finance", "payment"]):
            base_share = int(base_share * random.uniform(0.7, 1.0))  # Somewhat fragmented
        elif any(term in industry_lower for term in ["logistics", "delivery"]):
            base_share = int(base_share * random.uniform(0.9, 1.3))  # More consolidated
        elif any(term in industry_lower for term in ["education", "edtech"]):
            base_share = int(base_share * random.uniform(0.5, 0.8))  # Very fragmented
        elif any(term in industry_lower for term in ["electric", "ev", "automotive"]):
            base_share = int(base_share * random.uniform(1.0, 1.4))  # Emerging but consolidating
        
        # Ensure realistic distribution - no single player dominates too much
        return max(1, min(base_share, 25))  # Cap between 1% and 25% for more realism

    def _get_fallback_competitors(self, industry: str, keywords: list) -> List[Dict[str, Any]]:
        """Fallback to hardcoded competitors if real data fails"""
        print(f"🔍 Using fallback competitors for industry: {industry}")
        
        # Use the same industry matching logic as the main method
        known_competitors = {
            "technology": ["Infosys", "TCS", "Wipro", "HCL Technologies", "Tech Mahindra", "Zoho", "Freshworks", "Microsoft", "Google", "Amazon"],
            "healthcare": ["Practo", "1mg", "PharmEasy", "Netmeds", "Apollo 24/7", "Lybrate", "DocsApp", "Teladoc", "Amwell"],
            "fintech": ["Paytm", "PhonePe", "Razorpay", "Pine Labs", "Mobikwik", "BharatPe", "CRED", "Stripe", "PayPal"],
            "logistics": ["Swiggy", "Zomato", "Dunzo", "Porter", "BlackBuck", "Rivigo", "Delhivery", "Blue Dart", "FedEx"],
            "ecommerce": ["Flipkart", "Amazon India", "Myntra", "Nykaa", "BigBasket", "Grofers", "Meesho", "Shopify"],
            "electric vehicle": ["Ather Energy", "Ola Electric", "Hero Electric", "Mahindra Electric", "Tata Motors EV", "ChargePoint", "Shell Recharge"],
            "automotive": ["Tata Motors", "Mahindra", "Maruti Suzuki", "Hyundai India", "Hero MotoCorp", "Bajaj Auto", "TVS Motor"],
            "energy": ["Reliance Industries", "Adani Green", "Tata Power", "NTPC", "Coal India", "ONGC", "Indian Oil"],
            "mobility": ["Ola", "Uber India", "Rapido", "Bounce", "Yulu", "Vogo", "Quick Ride", "BlaBlaCar India"],
            "mapping": ["MapmyIndia", "Google Maps", "Ola Maps", "HERE Technologies", "TomTom", "Garmin"],
            "education": ["BYJU'S", "Unacademy", "Vedantu", "Toppr", "WhiteHat Jr", "Simplilearn", "UpGrad", "Coursera", "Khan Academy"],
            "edtech": ["BYJU'S", "Unacademy", "Vedantu", "Toppr", "Doubtnut", "Embibe", "Meritnation", "Khan Academy", "Coursera"],
            "rural": ["ITC e-Choupal", "Mahindra Agri Solutions", "Tata Kisan Sansar", "Digital Green", "CropIn", "AgroStar"],
            "agriculture": ["ITC e-Choupal", "Mahindra Agri Solutions", "UPL", "Bayer CropScience", "Syngenta India", "IFFCO"],
            "tablets": ["Samsung India", "Lenovo India", "Apple India", "Xiaomi India", "Realme", "OnePlus", "Micromax"]
        }
        
        # Enhanced multi-keyword matching for better industry detection
        # Priority order: specific industries first, then broader categories
        industry_lower = industry.lower()
        industry_competitors = known_competitors["technology"]  # Default
        
        # Check for specific high-priority industries first with more precise matching
        print(f"🔍 Analyzing industry: '{industry_lower}' for competitor matching")
        
        # Use scoring system to find the best match
        industry_scores = {}
        
        # Score each industry based on keyword matches
        if any(term in industry_lower for term in ["fintech", "finance", "payment", "banking", "wallet", "money"]):
            industry_scores["fintech"] = industry_scores.get("fintech", 0) + 10
        if any(term in industry_lower for term in ["education", "edtech", "learning", "school", "student"]):
            industry_scores["edtech"] = industry_scores.get("edtech", 0) + 10
        if any(term in industry_lower for term in ["electric", "ev", "charging", "battery"]):
            industry_scores["electric vehicle"] = industry_scores.get("electric vehicle", 0) + 10
        if any(term in industry_lower for term in ["health", "medical", "telemedicine", "healthcare"]):
            industry_scores["healthcare"] = industry_scores.get("healthcare", 0) + 10
        if any(term in industry_lower for term in ["food", "delivery", "restaurant", "beverage"]):
            industry_scores["logistics"] = industry_scores.get("logistics", 0) + 10
        if any(term in industry_lower for term in ["tablet", "device", "hardware", "electronics"]):
            industry_scores["tablets"] = industry_scores.get("tablets", 0) + 10
        if any(term in industry_lower for term in ["automotive", "car", "auto", "vehicle"]):
            industry_scores["automotive"] = industry_scores.get("automotive", 0) + 10
        if any(term in industry_lower for term in ["energy", "power", "utility", "renewable"]):
            industry_scores["energy"] = industry_scores.get("energy", 0) + 10
        if any(term in industry_lower for term in ["mobility", "transport", "ride", "travel"]):
            industry_scores["mobility"] = industry_scores.get("mobility", 0) + 10
        if any(term in industry_lower for term in ["map", "navigation", "location", "gps"]):
            industry_scores["mapping"] = industry_scores.get("mapping", 0) + 10
        if any(term in industry_lower for term in ["logistics", "courier"]):
            industry_scores["logistics"] = industry_scores.get("logistics", 0) + 8
        if any(term in industry_lower for term in ["commerce", "retail", "marketplace", "ecommerce"]):
            industry_scores["ecommerce"] = industry_scores.get("ecommerce", 0) + 10
        if any(term in industry_lower for term in ["rural", "village", "farming", "agriculture"]):
            industry_scores["rural"] = industry_scores.get("rural", 0) + 5  # Lower score for rural
        if any(term in industry_lower for term in ["tech", "software", "digital", "saas", "ai"]):
            industry_scores["technology"] = industry_scores.get("technology", 0) + 3  # Lower score for generic tech
        
        # Find the industry with the highest score
        if industry_scores:
            best_industry = max(industry_scores, key=industry_scores.get)
            industry_competitors = known_competitors.get(best_industry, known_competitors["technology"])
            print(f"✅ Best match: {best_industry} (score: {industry_scores[best_industry]}), using: {industry_competitors[:3]}")
        else:
            print(f"⚠️ No specific industry match found for: {industry_lower}, using Technology default")
        
        # Create competitor objects
        competitors = []
        import random
        for i, comp in enumerate(industry_competitors[:3]):
            funding = self._estimate_company_funding(comp, industry)
            market_share = self._estimate_market_share(funding, industry)
            
            competitors.append({
                "name": comp,
                "funding": int(funding),
                "market_share": market_share
            })
        
        return competitors

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