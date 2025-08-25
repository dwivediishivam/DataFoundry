import google.generativeai as genai
import os
from typing import Dict, Any
import json
from dotenv import load_dotenv

class LLMBreakdownAgent:
    def __init__(self):
        # Load environment variables
        load_dotenv()
        
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
            
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')

    async def analyze(self, idea: str) -> Dict[str, Any]:
        prompt = f"""
        Analyze the following startup idea and break it down into structured categories:

        Startup Idea: {idea}

        Please provide a JSON response with the following structure:
        {{
            "industry": "primary industry category",
            "business_model": "description of how the business makes money",
            "target_market": "description of target customers",
            "key_features": ["list", "of", "main", "features"],
            "technology_stack": ["required", "technologies"],
            "regulatory_considerations": ["potential", "regulatory", "issues"],
            "geographic_scope": "local/national/global",
            "keywords": ["relevant", "industry", "keywords", "for", "research"]
        }}

        Focus on being specific and actionable for market research.
        """

        try:
            response = self.model.generate_content(prompt)
            # Extract JSON from response
            response_text = response.text
            
            # Find JSON in the response
            start_idx = response_text.find('{')
            end_idx = response_text.rfind('}') + 1
            
            if start_idx != -1 and end_idx != -1:
                json_str = response_text[start_idx:end_idx]
                return json.loads(json_str)
            else:
                # Fallback if JSON parsing fails
                return self._create_smart_fallback_breakdown(idea)
                
        except Exception as e:
            print(f"LLM Breakdown error: {e}")
            # Check if it's a rate limit error
            if "429" in str(e) or "quota" in str(e).lower():
                print("Rate limit detected, using smart fallback analysis...")
                return self._create_smart_fallback_breakdown(idea)
            return self._create_smart_fallback_breakdown(idea)

    def _create_fallback_breakdown(self, idea: str) -> Dict[str, Any]:
        return {
            "industry": "Technology",
            "business_model": "Platform/Marketplace",
            "target_market": "General consumers",
            "key_features": ["Digital platform", "On-demand service"],
            "technology_stack": ["Web platform", "Mobile app", "API"],
            "regulatory_considerations": ["Data privacy", "Industry regulations"],
            "geographic_scope": "National",
            "keywords": ["startup", "technology", "platform", "service"]
        }
    
    def _create_smart_fallback_breakdown(self, idea: str) -> Dict[str, Any]:
        """Create a smarter fallback breakdown by analyzing keywords in the idea"""
        idea_lower = idea.lower()
        
        # Industry detection - order matters, more specific first
        industry = "Technology"  # Default
        
        # Check for EV/Electric first (before general automotive)
        if any(term in idea_lower for term in ["ev charging", "electric vehicle charging", "charging station", "charging point", "charging network"]):
            industry = "Electric Vehicle (EV) Infrastructure & Technology"
        elif any(term in idea_lower for term in ["electric", "ev", "charging", "battery"]) and any(term in idea_lower for term in ["vehicle", "car", "auto"]):
            industry = "Electric Vehicle (EV) Infrastructure & Technology"
        elif any(term in idea_lower for term in ["health", "medical", "telemedicine", "doctor", "patient"]):
            industry = "Healthcare & Telemedicine"
        elif any(term in idea_lower for term in ["finance", "payment", "banking", "fintech", "money", "wallet"]):
            industry = "Financial Technology (FinTech)"
        elif any(term in idea_lower for term in ["education", "learning", "school", "student", "edtech", "teaching"]):
            industry = "Education Technology (EdTech)"
        elif any(term in idea_lower for term in ["rural", "village", "farming", "agriculture"]) and any(term in idea_lower for term in ["education", "learning", "school"]):
            industry = "Rural Technology & Agriculture"
        elif any(term in idea_lower for term in ["food", "restaurant", "delivery", "meal", "cooking"]):
            industry = "Food & Beverage Technology"
        elif any(term in idea_lower for term in ["drone", "aerial", "aviation", "flying"]) and any(term in idea_lower for term in ["delivery", "transport", "logistics"]):
            industry = "Drone & Aviation Technology"
        elif any(term in idea_lower for term in ["logistics", "delivery", "transport", "shipping", "courier"]):
            industry = "Logistics & Transportation"
        elif any(term in idea_lower for term in ["retail", "ecommerce", "shopping", "marketplace", "store"]):
            industry = "E-commerce & Retail Technology"
        elif any(term in idea_lower for term in ["fitness", "health", "workout", "exercise", "wellness"]) and any(term in idea_lower for term in ["vr", "virtual", "ar", "augmented"]):
            industry = "Virtual & Augmented Reality"
        elif any(term in idea_lower for term in ["fitness", "health", "workout", "exercise", "wellness"]):
            industry = "Health & Fitness Technology"
        elif any(term in idea_lower for term in ["ai", "artificial intelligence", "machine learning", "automation"]):
            industry = "Artificial Intelligence & Automation"
        elif any(term in idea_lower for term in ["blockchain", "crypto", "decentralized", "web3"]):
            industry = "Blockchain & Web3 Technology"
        elif any(term in idea_lower for term in ["vr", "virtual reality", "ar", "augmented reality", "metaverse"]):
            industry = "Virtual & Augmented Reality"
        elif any(term in idea_lower for term in ["car", "vehicle", "automotive", "ride", "sharing"]):
            industry = "Automotive & Mobility Technology"
        elif any(term in idea_lower for term in ["rural", "village", "farming", "agriculture"]):
            industry = "Rural Technology & Agriculture"
        
        # Business model detection
        business_model = "Platform/Marketplace"  # Default
        if any(term in idea_lower for term in ["subscription", "saas", "software as a service"]):
            business_model = "Software as a Service (SaaS) - Subscription model"
        elif any(term in idea_lower for term in ["marketplace", "platform", "connect", "matching"]):
            business_model = "Two-sided marketplace connecting users"
        elif any(term in idea_lower for term in ["delivery", "on-demand", "service"]):
            business_model = "On-demand service platform"
        elif any(term in idea_lower for term in ["hardware", "device", "product", "kit"]):
            business_model = "Hardware product sales with software integration"
        elif any(term in idea_lower for term in ["consulting", "service", "professional"]):
            business_model = "Professional services and consulting"
        elif any(term in idea_lower for term in ["advertising", "marketing", "promotion"]):
            business_model = "Advertising and marketing platform"
        
        # Geographic scope detection
        geographic_scope = "National"  # Default
        if any(term in idea_lower for term in ["global", "worldwide", "international"]):
            geographic_scope = "Global"
        elif any(term in idea_lower for term in ["local", "city", "urban", "neighborhood"]):
            geographic_scope = "Local/Urban"
        elif any(term in idea_lower for term in ["rural", "village", "remote"]):
            geographic_scope = "Rural/Regional"
        
        # Extract keywords from the idea
        keywords = self._extract_keywords_from_idea(idea, industry)
        
        # Key features based on common patterns
        key_features = self._extract_key_features(idea_lower)
        
        # Technology stack based on industry and features
        technology_stack = self._determine_tech_stack(industry, key_features)
        
        # Regulatory considerations based on industry
        regulatory_considerations = self._determine_regulatory_considerations(industry)
        
        # Target market based on idea content
        target_market = self._determine_target_market(idea_lower, industry)
        
        return {
            "industry": industry,
            "business_model": business_model,
            "target_market": target_market,
            "key_features": key_features,
            "technology_stack": technology_stack,
            "regulatory_considerations": regulatory_considerations,
            "geographic_scope": geographic_scope,
            "keywords": keywords
        }
    
    def _extract_keywords_from_idea(self, idea: str, industry: str) -> list:
        """Extract relevant keywords from the idea text"""
        idea_lower = idea.lower()
        keywords = []
        
        # Industry-specific keyword extraction
        if "electric vehicle" in industry.lower() or "ev" in industry.lower():
            if "charging" in idea_lower:
                keywords.extend(["EV charging", "Electric vehicle charging stations", "EV charging app"])
            if "network" in idea_lower:
                keywords.extend(["EV charging network", "charging infrastructure"])
            if "map" in idea_lower or "find" in idea_lower:
                keywords.extend(["EV charging map", "charging station locator"])
            if "book" in idea_lower or "pay" in idea_lower:
                keywords.extend(["EV charging booking", "charging payment system"])
            keywords.extend(["India EV infrastructure", "Electric vehicle charging network"])
        elif "healthcare" in industry.lower():
            if "telemedicine" in idea_lower:
                keywords.extend(["telemedicine", "remote healthcare", "digital health"])
            if "medical" in idea_lower:
                keywords.extend(["medical technology", "healthcare software"])
        elif "fintech" in industry.lower():
            if "payment" in idea_lower:
                keywords.extend(["digital payments", "payment processing", "fintech"])
            if "banking" in idea_lower:
                keywords.extend(["digital banking", "financial services"])
        elif "edtech" in industry.lower():
            if "learning" in idea_lower:
                keywords.extend(["online learning", "educational technology", "e-learning"])
            if "school" in idea_lower:
                keywords.extend(["school management", "educational software"])
            if "rural" in idea_lower:
                keywords.extend(["Rural EdTech", "Offline learning", "Educational tablets"])
        elif "logistics" in industry.lower():
            if "delivery" in idea_lower:
                keywords.extend(["delivery services", "logistics technology", "supply chain"])
            if "drone" in idea_lower:
                keywords.extend(["drone delivery", "aerial logistics", "autonomous delivery"])
        elif "ai" in industry.lower():
            keywords.extend(["artificial intelligence", "machine learning", "automation"])
            if "content" in idea_lower:
                keywords.extend(["AI content creation", "automated content"])
            if "social" in idea_lower:
                keywords.extend(["social media marketing", "AI social tools"])
        elif "blockchain" in industry.lower():
            keywords.extend(["blockchain technology", "decentralized systems", "smart contracts"])
            if "supply" in idea_lower:
                keywords.extend(["blockchain", "supply chain", "food safety"])
        elif "vr" in industry.lower() or "ar" in industry.lower():
            keywords.extend(["virtual reality", "augmented reality", "immersive technology"])
            if "fitness" in idea_lower:
                keywords.extend(["VR fitness", "virtual workouts"])
        elif "automotive" in industry.lower():
            if "sharing" in idea_lower:
                keywords.extend(["car sharing", "mobility services", "peer-to-peer"])
            if "electric" in idea_lower:
                keywords.extend(["electric vehicles", "EV technology", "sustainable transport"])
        elif "rural" in industry.lower():
            keywords.extend(["rural technology", "offline solutions", "connectivity"])
        
        # Add general keywords based on common terms
        if "app" in idea_lower:
            keywords.append("mobile application")
        if "platform" in idea_lower:
            keywords.append("digital platform")
        if "ai" in idea_lower:
            keywords.append("AI-powered")
        if "social" in idea_lower:
            keywords.append("social media")
        if "business" in idea_lower:
            keywords.append("business solutions")
        
        # Ensure we have at least 3 keywords
        if len(keywords) < 3:
            keywords.extend(["technology platform", "digital solution", "innovation"])
        
        return keywords[:8]  # Limit to 8 keywords
    
    def _extract_key_features(self, idea_lower: str) -> list:
        """Extract key features from the idea"""
        features = []
        
        if "ai" in idea_lower or "artificial intelligence" in idea_lower:
            features.append("AI-powered automation")
        if "mobile" in idea_lower or "app" in idea_lower:
            features.append("Mobile application")
        if "platform" in idea_lower:
            features.append("Digital platform")
        if "real-time" in idea_lower or "live" in idea_lower:
            features.append("Real-time processing")
        if "analytics" in idea_lower or "data" in idea_lower:
            features.append("Data analytics")
        if "payment" in idea_lower:
            features.append("Payment processing")
        if "notification" in idea_lower or "alert" in idea_lower:
            features.append("Push notifications")
        if "tracking" in idea_lower or "monitor" in idea_lower:
            features.append("Tracking and monitoring")
        if "booking" in idea_lower or "reservation" in idea_lower:
            features.append("Booking system")
        if "social" in idea_lower:
            features.append("Social features")
        
        # Default features if none detected
        if not features:
            features = ["User-friendly interface", "Cloud-based platform", "Mobile optimization"]
        
        return features[:5]  # Limit to 5 features
    
    def _determine_tech_stack(self, industry: str, features: list) -> list:
        """Determine technology stack based on industry and features"""
        tech_stack = ["Cloud infrastructure", "API development"]
        
        # Add mobile if mobile features detected
        if any("mobile" in feature.lower() for feature in features):
            tech_stack.extend(["React Native/Flutter", "Mobile app development"])
        
        # Industry-specific tech
        if "ai" in industry.lower():
            tech_stack.extend(["Machine Learning frameworks", "Natural Language Processing"])
        elif "blockchain" in industry.lower():
            tech_stack.extend(["Blockchain development", "Smart contracts"])
        elif "healthcare" in industry.lower():
            tech_stack.extend(["HIPAA compliance", "Healthcare APIs"])
        elif "fintech" in industry.lower():
            tech_stack.extend(["Payment gateways", "Financial APIs", "Security protocols"])
        elif "vr" in industry.lower() or "ar" in industry.lower():
            tech_stack.extend(["Unity/Unreal Engine", "3D graphics", "VR/AR SDKs"])
        
        # Common web technologies
        tech_stack.extend(["Web application", "Database management"])
        
        return tech_stack[:6]  # Limit to 6 technologies
    
    def _determine_regulatory_considerations(self, industry: str) -> list:
        """Determine regulatory considerations based on industry"""
        regulations = ["Data privacy (GDPR, CCPA)"]
        
        if "healthcare" in industry.lower():
            regulations.extend(["HIPAA compliance", "Medical device regulations"])
        elif "fintech" in industry.lower():
            regulations.extend(["Financial regulations", "PCI DSS compliance", "Anti-money laundering"])
        elif "drone" in industry.lower():
            regulations.extend(["Aviation regulations", "Drone operation permits"])
        elif "automotive" in industry.lower():
            regulations.extend(["Transportation regulations", "Insurance requirements"])
        elif "education" in industry.lower():
            regulations.extend(["FERPA compliance", "Child privacy protection"])
        elif "food" in industry.lower():
            regulations.extend(["Food safety regulations", "Health department compliance"])
        
        regulations.append("Industry-specific compliance")
        return regulations[:4]  # Limit to 4 regulations
    
    def _determine_target_market(self, idea_lower: str, industry: str) -> str:
        """Determine target market based on idea content"""
        if "small business" in idea_lower or "smb" in idea_lower:
            return "Small and medium businesses (SMBs)"
        elif "enterprise" in idea_lower or "large business" in idea_lower:
            return "Enterprise customers"
        elif "consumer" in idea_lower or "individual" in idea_lower:
            return "Individual consumers"
        elif "healthcare" in industry.lower():
            return "Healthcare providers and patients"
        elif "education" in industry.lower():
            if "school" in idea_lower:
                return "Educational institutions and schools"
            else:
                return "Students and educational institutions"
        elif "rural" in idea_lower:
            return "Rural communities and underserved populations"
        elif "urban" in idea_lower:
            return "Urban consumers and city dwellers"
        else:
            return "General consumers and businesses"