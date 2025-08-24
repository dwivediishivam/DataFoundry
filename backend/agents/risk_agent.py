import asyncio
from typing import Dict, Any, List
import random

class RiskAgent:
    def __init__(self):
        # Risk categories and templates
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
        
        # Get industry-specific risks
        base_risks = self._get_industry_risks(industry)
        
        # Add business model specific risks
        model_risks = self._get_business_model_risks(business_model)
        
        # Add regulatory risks
        regulatory_risks = self._get_regulatory_risks(regulatory_considerations)
        
        # Combine and prioritize risks
        all_risks = base_risks + model_risks + regulatory_risks
        
        # Remove duplicates and limit to top 5 risks
        unique_risks = []
        seen_categories = set()
        
        for risk in all_risks:
            if risk["category"] not in seen_categories:
                unique_risks.append(risk)
                seen_categories.add(risk["category"])
                
        return unique_risks[:5]

    def _get_industry_risks(self, industry: str) -> List[Dict[str, Any]]:
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