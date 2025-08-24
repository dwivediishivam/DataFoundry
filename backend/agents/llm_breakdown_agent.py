import google.generativeai as genai
import os
from typing import Dict, Any
import json

class LLMBreakdownAgent:
    def __init__(self):
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
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
                return self._create_fallback_breakdown(idea)
                
        except Exception as e:
            print(f"LLM Breakdown error: {e}")
            return self._create_fallback_breakdown(idea)

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