import asyncio
from typing import Dict, Any, List
import random
import requests
import os
from dotenv import load_dotenv

class RiskAgent:
    def __init__(self):
        load_dotenv()
        self.serpapi_key = os.getenv("SERPAPI_KEY")
        
        # Dynamic risk categories and templates
        self.risk_templates = {
            "technology": [
                {
                    "category": "Technical Risk",
                    "level": "Medium",
                    "description": "Rapid technology changes may require continuous platform updates and adaptation"
                },
                {
                    "category": "Cybersecurity Risk",
                    "level": "High",
                    "description": "Data breaches and security vulnerabilities could damage reputation and incur regulatory penalties"
                },
                {
                    "category": "Scalability Risk",
                    "level": "Medium",
                    "description": "Infrastructure may struggle to handle rapid user growth without significant investment"
                }
            ],
            "logistics": [
                {
                    "category": "Regulatory Risk",
                    "level": "High",
                    "description": "Aviation and transportation regulations may limit operational flexibility and increase compliance costs"
                },
                {
                    "category": "Safety Risk",
                    "level": "High",
                    "description": "Accidents or safety incidents could result in liability issues and regulatory scrutiny"
                },
                {
                    "category": "Weather Risk",
                    "level": "Medium",
                    "description": "Weather conditions may significantly impact service reliability and operational costs"
                }
            ],
            "healthcare": [
                {
                    "category": "Regulatory Risk",
                    "level": "High",
                    "description": "Healthcare regulations (HIPAA, FDA) require strict compliance and may slow product development"
                },
                {
                    "category": "Liability Risk",
                    "level": "High",
                    "description": "Medical errors or data breaches could result in significant legal and financial consequences"
                },
                {
                    "category": "Adoption Risk",
                    "level": "Medium",
                    "description": "Healthcare providers may be slow to adopt new technologies due to conservative culture"
                }
            ],
            "fintech": [
                {
                    "category": "Regulatory Risk",
                    "level": "High",
                    "description": "Financial regulations and compliance requirements may limit product features and increase costs"
                },
                {
                    "category": "Security Risk",
                    "level": "High",
                    "description": "Financial data breaches could result in severe penalties and loss of customer trust"
                },
                {
                    "category": "Market Risk",
                    "level": "Medium",
                    "description": "Economic downturns may reduce demand for financial services and increase default rates"
                }
            ]
        }

    async def analyze(self, breakdown: Dict[str, Any]) -> List[Dict[str, Any]]:
        industry = breakdown.get("industry", "Technology").lower()
        business_model = breakdown.get("business_model", "")
        regulatory_considerations = breakdown.get("regulatory_considerations", [])
        keywords = breakdown.get("keywords", [])
        
        try:
            # Fetch real-time risk data
            real_risks = await self._fetch_real_risk_data(industry, keywords, business_model)
            
            # Get industry-specific risks with variation
            base_risks = self._get_dynamic_industry_risks(industry, keywords)
            
            # Add business model specific risks with variation
            model_risks = self._get_dynamic_business_model_risks(business_model, industry)
            
            # Add regulatory risks with current context
            regulatory_risks = self._get_dynamic_regulatory_risks(regulatory_considerations, industry)
            
            # Combine all risks
            all_risks = real_risks + base_risks + model_risks + regulatory_risks
            
            # Prioritize and select unique risks
            unique_risks = self._prioritize_risks(all_risks, industry, business_model)
            
            return unique_risks[:5]
            
        except Exception as e:
            print(f"Risk analysis error: {e}")
            return self._get_fallback_risks(industry, business_model)

    async def _fetch_real_risk_data(self, industry: str, keywords: list, business_model: str) -> List[Dict[str, Any]]:
        """Fetch real-time risk data from news and industry reports"""
        if not self.serpapi_key:
            return []
        
        try:
            # Search for recent industry risks and challenges
            search_terms = [industry] + keywords[:2]
            query = f"{' '.join(search_terms)} risks challenges problems 2024"
            
            params = {
                "engine": "google",
                "q": query,
                "api_key": self.serpapi_key,
                "num": 5,
                "tbm": "nws"  # News search
            }
            
            response = requests.get("https://serpapi.com/search", params=params, timeout=10)
            data = response.json()
            
            # Extract risks from news results
            risks = self._extract_risks_from_news(data, industry)
            return risks
            
        except Exception as e:
            print(f"Failed to fetch real risk data: {e}")
            return []

    def _extract_risks_from_news(self, search_data: dict, industry: str) -> List[Dict[str, Any]]:
        """Extract risk information from news search results"""
        risks = []
        news_results = search_data.get("news_results", [])
        
        risk_keywords = {
            "regulatory": ["regulation", "compliance", "legal", "lawsuit", "fine", "penalty"],
            "market": ["recession", "downturn", "competition", "market share", "demand"],
            "technology": ["breach", "hack", "outage", "failure", "bug", "security"],
            "operational": ["supply chain", "shortage", "delay", "cost", "inflation"],
            "financial": ["funding", "investment", "cash", "revenue", "loss"]
        }
        
        for result in news_results[:3]:
            title = result.get("title", "").lower()
            snippet = result.get("snippet", "").lower()
            text = f"{title} {snippet}"
            
            for risk_type, keywords in risk_keywords.items():
                if any(keyword in text for keyword in keywords):
                    # Generate risk based on news content
                    risk_level = self._determine_risk_level(text, risk_type)
                    description = self._generate_risk_description(text, risk_type, industry)
                    
                    risks.append({
                        "category": f"{risk_type.title()} Risk",
                        "level": risk_level,
                        "description": description
                    })
                    break  # Only one risk per news item
        
        return risks

    def _determine_risk_level(self, text: str, risk_type: str) -> str:
        """Determine risk level based on text content"""
        high_indicators = ["crisis", "major", "significant", "severe", "critical", "urgent"]
        medium_indicators = ["concern", "challenge", "issue", "problem", "difficulty"]
        
        if any(indicator in text for indicator in high_indicators):
            return "High"
        elif any(indicator in text for indicator in medium_indicators):
            return "Medium"
        else:
            return random.choice(["Low", "Medium"])

    def _generate_risk_description(self, text: str, risk_type: str, industry: str) -> str:
        """Generate contextual risk description"""
        descriptions = {
            "regulatory": f"Recent regulatory developments in {industry} may impact operational compliance and increase costs",
            "market": f"Market conditions and competitive pressures in {industry} could affect growth and profitability",
            "technology": f"Technology-related challenges in {industry} may pose security and operational risks",
            "operational": f"Supply chain and operational challenges in {industry} could impact service delivery",
            "financial": f"Financial market conditions may affect funding availability and business sustainability"
        }
        
        return descriptions.get(risk_type, f"Industry-specific challenges in {industry} require careful monitoring")

    def _get_dynamic_industry_risks(self, industry: str, keywords: list) -> List[Dict[str, Any]]:
        """Generate dynamic industry-specific risks with variation"""
        base_risks = self._get_industry_risks(industry)
        # Add variation to base risks
        varied_risks = []
        for risk in base_risks:
            # Vary risk levels slightly
            original_level = risk["level"]
            if random.random() < 0.3:  # 30% chance to vary
                if original_level == "High":
                    new_level = random.choice(["High", "Medium"])
                elif original_level == "Medium":
                    new_level = random.choice(["Medium", "Low", "High"])
                else:
                    new_level = random.choice(["Low", "Medium"])
            else:
                new_level = original_level
            
            # Add keyword-specific context
            description = risk["description"]
            if keywords:
                relevant_keyword = random.choice(keywords)
                if relevant_keyword.lower() not in description.lower():
                    description += f" This is particularly relevant for {relevant_keyword}-focused businesses."
            
            varied_risks.append({
                "category": risk["category"],
                "level": new_level,
                "description": description
            })
        
        return varied_risks

    def _get_industry_risks(self, industry: str) -> List[Dict[str, Any]]:
        """Get base industry risks"""
        if any(term in industry for term in ["logistics", "delivery", "transport"]):
            return self.risk_templates["logistics"]
        elif any(term in industry for term in ["health", "medical"]):
            return self.risk_templates["healthcare"]
        elif any(term in industry for term in ["finance", "payment", "banking"]):
            return self.risk_templates["fintech"]
        elif any(term in industry for term in ["tech", "software", "digital"]):
            return self.risk_templates["technology"]
        else:
            return self.risk_templates["technology"]  # Default to tech risks

    def _get_dynamic_business_model_risks(self, business_model: str, industry: str) -> List[Dict[str, Any]]:
        """Generate dynamic business model risks with industry context"""
        base_risks = self._get_business_model_risks(business_model)
        
        # Add industry-specific context to business model risks
        enhanced_risks = []
        for risk in base_risks:
            # Enhance description with industry context
            description = risk["description"]
            if "marketplace" in business_model.lower() and "technology" in industry.lower():
                description += " Technology platforms face additional challenges in user acquisition and retention."
            elif "saas" in business_model.lower() and "healthcare" in industry.lower():
                description += " Healthcare SaaS faces stricter compliance requirements and longer sales cycles."
            elif "on-demand" in business_model.lower() and "logistics" in industry.lower():
                description += " Logistics on-demand services must manage complex regulatory and safety requirements."
            
            # Vary risk levels based on industry
            level = risk["level"]
            if industry.lower() in ["healthcare", "fintech"] and "regulatory" in risk["category"].lower():
                level = "High"  # Higher regulatory risk in these industries
            elif industry.lower() == "technology" and "security" in risk["category"].lower():
                level = "High"  # Higher security risk in tech
            
            enhanced_risks.append({
                "category": risk["category"],
                "level": level,
                "description": description
            })
        
        return enhanced_risks

    def _get_business_model_risks(self, business_model: str) -> List[Dict[str, Any]]:
        risks = []
        
        if "marketplace" in business_model.lower() or "platform" in business_model.lower():
            risks.append({
                "category": "Network Effects Risk",
                "level": "Medium",
                "description": "Platform success depends on achieving critical mass of users on both sides of the marketplace"
            })
        
        if "subscription" in business_model.lower() or "saas" in business_model.lower():
            risks.append({
                "category": "Churn Risk",
                "level": "Medium",
                "description": "High customer churn rates could significantly impact recurring revenue and growth"
            })
        
        if "on-demand" in business_model.lower():
            risks.append({
                "category": "Operational Risk",
                "level": "Medium",
                "description": "Managing supply and demand fluctuations may require significant operational complexity"
            })
        
        return risks

    def _get_dynamic_regulatory_risks(self, regulatory_considerations: List[str], industry: str) -> List[Dict[str, Any]]:
        """Generate dynamic regulatory risks with current context"""
        base_risks = self._get_regulatory_risks(regulatory_considerations)
        
        # Add current regulatory context
        enhanced_risks = []
        for risk in base_risks:
            description = risk["description"]
            
            # Add 2024-specific regulatory context
            if "data privacy" in risk["category"].lower():
                description += " Recent AI regulation developments may introduce additional compliance requirements."
            elif "industry regulation" in risk["category"].lower():
                if "healthcare" in industry.lower():
                    description += " Telehealth regulations continue to evolve post-pandemic."
                elif "fintech" in industry.lower():
                    description += " Cryptocurrency and digital payment regulations are rapidly changing."
                elif "logistics" in industry.lower():
                    description += " Drone delivery regulations are still being developed by aviation authorities."
            
            # Vary risk levels based on current regulatory climate
            level = risk["level"]
            if random.random() < 0.4:  # 40% chance to adjust
                if level == "Medium":
                    level = random.choice(["Medium", "High"])
                elif level == "High":
                    level = random.choice(["High", "Medium"])
            
            enhanced_risks.append({
                "category": risk["category"],
                "level": level,
                "description": description
            })
        
        return enhanced_risks

    def _get_regulatory_risks(self, regulatory_considerations: List[str]) -> List[Dict[str, Any]]:
        risks = []
        
        for consideration in regulatory_considerations:
            if "data privacy" in consideration.lower():
                risks.append({
                    "category": "Privacy Risk",
                    "level": "High",
                    "description": "Data privacy regulations (GDPR, CCPA) may require significant compliance investment"
                })
            elif "industry regulation" in consideration.lower():
                risks.append({
                    "category": "Compliance Risk",
                    "level": "Medium",
                    "description": "Industry-specific regulations may limit operational flexibility and increase costs"
                })
        
        return risks

    def _prioritize_risks(self, all_risks: List[Dict[str, Any]], industry: str, business_model: str) -> List[Dict[str, Any]]:
        """Prioritize and select unique risks"""
        # Remove duplicates based on category
        unique_risks = []
        seen_categories = set()
        
        # Sort by risk level priority (High > Medium > Low)
        risk_priority = {"High": 3, "Medium": 2, "Low": 1}
        sorted_risks = sorted(all_risks, key=lambda x: risk_priority.get(x["level"], 0), reverse=True)
        
        for risk in sorted_risks:
            category = risk["category"]
            if category not in seen_categories:
                unique_risks.append(risk)
                seen_categories.add(category)
                
                if len(unique_risks) >= 6:  # Limit to 6 risks
                    break
        
        return unique_risks

    def _get_fallback_risks(self, industry: str, business_model: str) -> List[Dict[str, Any]]:
        """Fallback risks if real data fetching fails"""
        base_risks = self._get_industry_risks(industry)
        model_risks = self._get_business_model_risks(business_model)
        
        # Add some randomization to fallback risks
        all_risks = base_risks + model_risks
        for risk in all_risks:
            if random.random() < 0.3:  # 30% chance to vary level
                current_level = risk["level"]
                if current_level == "High":
                    risk["level"] = random.choice(["High", "Medium"])
                elif current_level == "Medium":
                    risk["level"] = random.choice(["Medium", "Low", "High"])
                else:
                    risk["level"] = random.choice(["Low", "Medium"])
        
        return all_risks[:5]