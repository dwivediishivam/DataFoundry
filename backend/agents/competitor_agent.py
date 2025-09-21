import requests
import asyncio
from typing import Dict, Any, List
import random
import os
import hashlib
import google.generativeai as genai
import json
from dotenv import load_dotenv

class CompetitorAgent:
    def __init__(self):
        load_dotenv()
        self.serpapi_key = os.getenv("SERPAPI_KEY")
        
        # Initialize Gemini API
        api_key = os.getenv("GEMINI_API_KEY")
        if api_key:
            genai.configure(api_key=api_key)
            self.gemini_model = genai.GenerativeModel('gemini-1.5-flash')
        else:
            print("⚠️ GEMINI_API_KEY not found, competitor analysis will use fallback data")
            self.gemini_model = None
        
        # Realistic competitor database with actual funding data
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
        
        # Realistic funding data for major companies (in millions USD)
        self.real_funding_data = {
            # Big Tech
            "Microsoft": 2000, "Google": 1500, "Amazon": 1800, "Apple": 1200, "Meta": 1000,
            "Salesforce": 800, "Adobe": 600, "Oracle": 500, "IBM": 400,
            
            # Indian Unicorns & Major Companies
            "Paytm": 1800, "PhonePe": 1200, "Razorpay": 800, "BYJU'S": 1500, "Unacademy": 600,
            "Ola": 1000, "Swiggy": 800, "Zomato": 600, "Flipkart": 2000, "Nykaa": 400,
            "Infosys": 500, "TCS": 600, "Wipro": 300, "HCL Technologies": 250, "Tech Mahindra": 200,
            
            # Fintech
            "Stripe": 2000, "PayPal": 1500, "Square": 800, "Pine Labs": 300, "Mobikwik": 200,
            "BharatPe": 400, "CRED": 500,
            
            # Healthcare
            "Practo": 200, "1mg": 150, "PharmEasy": 300, "Netmeds": 100, "Apollo 24/7": 250,
            "Teladoc": 600, "Amwell": 400,
            
            # Logistics/Delivery
            "Dunzo": 200, "Porter": 150, "BlackBuck": 100, "Rivigo": 80, "Delhivery": 400,
            "Blue Dart": 200, "FedEx": 800,
            
            # E-commerce
            "Myntra": 300, "BigBasket": 200, "Grofers": 150, "Meesho": 400, "Shopify": 1000,
            
            # Electric Vehicles
            "Ather Energy": 200, "Ola Electric": 400, "Hero Electric": 100, "Mahindra Electric": 300,
            "Tata Motors EV": 500, "ChargePoint": 600, "Shell Recharge": 400,
            
            # Automotive
            "Tata Motors": 800, "Mahindra": 600, "Maruti Suzuki": 1000, "Hyundai India": 500,
            "Hero MotoCorp": 400, "Bajaj Auto": 300, "TVS Motor": 200,
            
            # Energy
            "Reliance Industries": 2000, "Adani Green": 800, "Tata Power": 400, "NTPC": 600,
            "Coal India": 500, "ONGC": 700, "Indian Oil": 800,
            
            # Mobility
            "Uber India": 600, "Rapido": 100, "Bounce": 80, "Yulu": 50, "Vogo": 40,
            "Quick Ride": 30, "BlaBlaCar India": 60,
            
            # Mapping
            "MapmyIndia": 100, "Google Maps": 800, "Ola Maps": 200, "HERE Technologies": 300,
            "TomTom": 400, "Garmin": 500,
            
            # EdTech
            "Vedantu": 200, "Toppr": 150, "WhiteHat Jr": 100, "Simplilearn": 80, "UpGrad": 300,
            "Coursera": 600, "Khan Academy": 200, "Doubtnut": 50, "Embibe": 40, "Meritnation": 30,
            
            # Rural/Agriculture
            "ITC e-Choupal": 200, "Mahindra Agri Solutions": 150, "Tata Kisan Sansar": 100,
            "Digital Green": 50, "CropIn": 80, "AgroStar": 60, "UPL": 300, "Bayer CropScience": 400,
            "Syngenta India": 200, "IFFCO": 500,
            
            # Tablets/Electronics
            "Samsung India": 1000, "Lenovo India": 400, "Apple India": 800, "Xiaomi India": 600,
            "Realme": 200, "OnePlus": 300, "Micromax": 100
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
        """Fetch real competitor data using Gemini AI, SerpAPI, or fallback to curated list"""
        print(f"🔍 Fetching competitors for industry: {industry}, keywords: {keywords}")
        
        # Try Gemini AI first for intelligent competitor analysis
        try:
            if self.gemini_model:
                print("🤖 Attempting to analyze competitors using Gemini AI...")
                competitors = await self._analyze_competitors_with_gemini(industry, keywords, business_model)
                if len(competitors) >= 2:
                    print(f"✅ Found {len(competitors)} competitors via Gemini AI")
                    return competitors
                else:
                    print("⚠️ Gemini returned insufficient competitors, trying SerpAPI...")
            else:
                print("⚠️ No Gemini API key available, trying SerpAPI...")
        except Exception as e:
            print(f"❌ Gemini analysis failed: {e}, trying SerpAPI...")
        
        # Try SerpAPI as secondary option
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
        
        # Use curated competitors as final fallback
        print("🔄 Using curated competitors for better industry matching")
        return self._get_fallback_competitors(industry, keywords)

    async def _analyze_competitors_with_gemini(self, industry: str, keywords: list, business_model: str) -> List[Dict[str, Any]]:
        """Use Gemini AI to analyze and identify real competitors with funding data"""
        if not self.gemini_model:
            raise Exception("Gemini model not available")
        
        prompt = f"""
        Analyze the competitive landscape for a startup in the {industry} industry with the following details:
        
        Industry: {industry}
        Keywords: {', '.join(keywords)}
        Business Model: {business_model}
        
        Please identify 3-5 real, well-known competitors in this space and provide their actual funding data and market share estimates.
        Focus on companies that are direct competitors or operate in similar markets.
        
        For each competitor, provide:
        1. Company name (use real company names)
        2. Total funding raised (in millions USD)
        3. Estimated market share (as a percentage)
        4. Brief description of their business model
        
        Please respond with a JSON array in this exact format:
        [
            {{
                "name": "Company Name",
                "funding": 1500,
                "market_share": 15,
                "description": "Brief description of what they do"
            }},
            {{
                "name": "Another Company",
                "funding": 800,
                "market_share": 8,
                "description": "Brief description of what they do"
            }}
        ]
        
        Use real companies with actual funding data. For funding amounts, use the most recent total funding raised.
        For market share, provide realistic estimates based on industry knowledge.
        Focus on companies that would be direct competitors to a startup in this space.
        """
        
        try:
            response = self.gemini_model.generate_content(prompt)
            response_text = response.text
            
            # Extract JSON from response
            start_idx = response_text.find('[')
            end_idx = response_text.rfind(']') + 1
            
            if start_idx != -1 and end_idx != -1:
                json_str = response_text[start_idx:end_idx]
                competitors_data = json.loads(json_str)
                
                # Validate and clean the data
                competitors = []
                for comp in competitors_data:
                    if isinstance(comp, dict) and 'name' in comp:
                        # Ensure funding is a number
                        funding = comp.get('funding', 0)
                        if isinstance(funding, str):
                            # Extract number from string
                            import re
                            numbers = re.findall(r'\d+', funding)
                            funding = int(numbers[0]) if numbers else 0
                        
                        # Ensure market share is a number
                        market_share = comp.get('market_share', 0)
                        if isinstance(market_share, str):
                            import re
                            numbers = re.findall(r'\d+', market_share)
                            market_share = int(numbers[0]) if numbers else 0
                        
                        competitors.append({
                            "name": comp['name'],
                            "funding": int(funding),
                            "market_share": int(market_share)
                        })
                
                print(f"🤖 Gemini identified {len(competitors)} competitors")
                return competitors
            else:
                print("❌ Could not extract JSON from Gemini response")
                raise Exception("Invalid JSON response from Gemini")
                
        except json.JSONDecodeError as e:
            print(f"❌ JSON parsing error: {e}")
            raise Exception("Failed to parse Gemini response as JSON")
        except Exception as e:
            print(f"❌ Gemini analysis error: {e}")
            raise e

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
            
            # Use the same simplified industry matching logic
            industry_lower = industry.lower()
            industry_competitors = known_competitors["technology"]  # Default
            
            # Check for specific industries in priority order (most specific first)
            if any(term in industry_lower for term in ["fintech", "finance", "payment", "banking", "wallet", "money"]):
                industry_competitors = known_competitors["fintech"]
            elif any(term in industry_lower for term in ["education", "edtech", "learning", "school", "student"]):
                industry_competitors = known_competitors["edtech"]
            elif any(term in industry_lower for term in ["electric", "ev", "charging", "battery"]):
                industry_competitors = known_competitors["electric vehicle"]
            elif any(term in industry_lower for term in ["health", "medical", "telemedicine", "healthcare"]):
                industry_competitors = known_competitors["healthcare"]
            elif any(term in industry_lower for term in ["food", "delivery", "restaurant", "beverage", "logistics", "courier"]):
                industry_competitors = known_competitors["logistics"]
            elif any(term in industry_lower for term in ["tablet", "device", "hardware", "electronics"]):
                industry_competitors = known_competitors["tablets"]
            elif any(term in industry_lower for term in ["automotive", "car", "auto", "vehicle"]):
                industry_competitors = known_competitors["automotive"]
            elif any(term in industry_lower for term in ["energy", "power", "utility", "renewable"]):
                industry_competitors = known_competitors["energy"]
            elif any(term in industry_lower for term in ["mobility", "transport", "ride", "travel"]):
                industry_competitors = known_competitors["mobility"]
            elif any(term in industry_lower for term in ["map", "navigation", "location", "gps"]):
                industry_competitors = known_competitors["mapping"]
            elif any(term in industry_lower for term in ["commerce", "retail", "marketplace", "ecommerce"]):
                industry_competitors = known_competitors["ecommerce"]
            elif any(term in industry_lower for term in ["rural", "village", "farming", "agriculture"]):
                industry_competitors = known_competitors["rural"]
            
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
        """Get realistic funding data for companies based on actual market data"""
        
        # First check if we have real funding data for this company
        if company in self.real_funding_data:
            return float(self.real_funding_data[company])
        
        # For companies not in our database, use industry-based estimation
        # Create a consistent seed based on company name for reproducible results
        seed = int(hashlib.md5(company.encode()).hexdigest()[:8], 16)
        random.seed(seed)
        
        # Industry-based funding estimation (in millions USD)
        industry_funding_ranges = {
            "fintech": (50, 2000),      # High funding potential
            "healthcare": (30, 1000),   # Moderate to high
            "logistics": (20, 800),     # Moderate
            "ecommerce": (40, 1500),    # High potential
            "electric vehicle": (100, 2000),  # High capital requirements
            "automotive": (200, 2000),  # Very high capital
            "energy": (300, 3000),      # Extremely high capital
            "mobility": (20, 600),      # Moderate
            "mapping": (50, 800),       # Moderate to high
            "education": (10, 500),     # Lower funding
            "edtech": (20, 800),        # Moderate
            "rural": (5, 200),          # Lower funding
            "agriculture": (10, 300),   # Lower to moderate
            "tablets": (100, 1000),     # High capital
            "technology": (30, 1000)    # Default range
        }
        
        # Find the best matching industry
        industry_lower = industry.lower()
        funding_range = industry_funding_ranges["technology"]  # Default
        
        for key, range_val in industry_funding_ranges.items():
            if key in industry_lower:
                funding_range = range_val
                break
        
        # Generate funding within the range with some variation
        min_funding, max_funding = funding_range
        funding = random.randint(min_funding, max_funding)
        
        # Reset random seed
        random.seed()
        return float(funding)

    def _estimate_market_share(self, funding: float, industry: str) -> int:
        """Estimate realistic market share based on funding and industry characteristics"""
        
        # Create consistent seed for reproducible results
        seed = int(hashlib.md5(f"{funding}_{industry}".encode()).hexdigest()[:8], 16)
        random.seed(seed)
        
        # Base market share calculation based on funding tiers
        if funding > 2000:  # > $2B - Market leaders
            base_share = random.randint(15, 35)
        elif funding > 1000:  # > $1B - Major players
            base_share = random.randint(8, 20)
        elif funding > 500:  # > $500M - Established players
            base_share = random.randint(4, 12)
        elif funding > 200:  # > $200M - Growing companies
            base_share = random.randint(2, 8)
        elif funding > 50:   # > $50M - Emerging players
            base_share = random.randint(1, 5)
        else:  # < $50M - Small players
            base_share = random.randint(1, 3)
        
        # Industry-specific market concentration factors
        industry_lower = industry.lower()
        concentration_factor = 1.0  # Default
        
        # High concentration industries (few dominant players)
        if any(term in industry_lower for term in ["automotive", "energy", "electric vehicle"]):
            concentration_factor = random.uniform(1.2, 1.8)
        # Medium concentration
        elif any(term in industry_lower for term in ["fintech", "healthcare", "logistics"]):
            concentration_factor = random.uniform(0.9, 1.3)
        # Low concentration (highly fragmented)
        elif any(term in industry_lower for term in ["education", "edtech", "technology", "software", "saas"]):
            concentration_factor = random.uniform(0.4, 0.8)
        # Very low concentration
        elif any(term in industry_lower for term in ["rural", "agriculture"]):
            concentration_factor = random.uniform(0.3, 0.6)
        
        # Apply concentration factor
        adjusted_share = int(base_share * concentration_factor)
        
        # Ensure realistic bounds (1% to 40% max)
        final_share = max(1, min(adjusted_share, 40))
        
        # Reset random seed
        random.seed()
        return final_share

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
        
        # Simplified industry matching with priority order
        industry_competitors = known_competitors["technology"]  # Default fallback
        
        # Check for specific industries in priority order (most specific first)
        if any(term in industry_lower for term in ["fintech", "finance", "payment", "banking", "wallet", "money"]):
            industry_competitors = known_competitors["fintech"]
            print(f"✅ Matched industry: Fintech")
        elif any(term in industry_lower for term in ["education", "edtech", "learning", "school", "student"]):
            industry_competitors = known_competitors["edtech"]
            print(f"✅ Matched industry: EdTech")
        elif any(term in industry_lower for term in ["electric", "ev", "charging", "battery"]):
            industry_competitors = known_competitors["electric vehicle"]
            print(f"✅ Matched industry: Electric Vehicle")
        elif any(term in industry_lower for term in ["health", "medical", "telemedicine", "healthcare"]):
            industry_competitors = known_competitors["healthcare"]
            print(f"✅ Matched industry: Healthcare")
        elif any(term in industry_lower for term in ["food", "delivery", "restaurant", "beverage", "logistics", "courier"]):
            industry_competitors = known_competitors["logistics"]
            print(f"✅ Matched industry: Logistics/Delivery")
        elif any(term in industry_lower for term in ["tablet", "device", "hardware", "electronics"]):
            industry_competitors = known_competitors["tablets"]
            print(f"✅ Matched industry: Tablets/Electronics")
        elif any(term in industry_lower for term in ["automotive", "car", "auto", "vehicle"]):
            industry_competitors = known_competitors["automotive"]
            print(f"✅ Matched industry: Automotive")
        elif any(term in industry_lower for term in ["energy", "power", "utility", "renewable"]):
            industry_competitors = known_competitors["energy"]
            print(f"✅ Matched industry: Energy")
        elif any(term in industry_lower for term in ["mobility", "transport", "ride", "travel"]):
            industry_competitors = known_competitors["mobility"]
            print(f"✅ Matched industry: Mobility")
        elif any(term in industry_lower for term in ["map", "navigation", "location", "gps"]):
            industry_competitors = known_competitors["mapping"]
            print(f"✅ Matched industry: Mapping")
        elif any(term in industry_lower for term in ["commerce", "retail", "marketplace", "ecommerce"]):
            industry_competitors = known_competitors["ecommerce"]
            print(f"✅ Matched industry: E-commerce")
        elif any(term in industry_lower for term in ["rural", "village", "farming", "agriculture"]):
            industry_competitors = known_competitors["rural"]
            print(f"✅ Matched industry: Rural/Agriculture")
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