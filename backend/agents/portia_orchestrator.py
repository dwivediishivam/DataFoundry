import os
import asyncio
from typing import Dict, Any, List
import httpx
import json
from pydantic import BaseModel

class PortiaAgent(BaseModel):
    """Portia AI Agent configuration"""
    name: str
    role: str
    goal: str
    backstory: str
    tools: List[str] = []

class PortiaTask(BaseModel):
    """Portia AI Task configuration"""
    description: str
    agent: str
    expected_output: str
    context: List[str] = []

class PortiaOrchestrator:
    """Portia AI orchestrator for DataFoundry startup analysis"""
    
    def __init__(self):
        self.api_key = os.getenv("PORTIA_API_KEY")
        self.base_url = "https://api.portia.dev/v1"
        self.client = httpx.AsyncClient(
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            },
            timeout=120.0
        )
        
        # Define specialized agents
        self.agents = self._create_agents()
    
    def _create_agents(self) -> List[PortiaAgent]:
        """Create specialized Portia AI agents for startup analysis"""
        return [
            PortiaAgent(
                name="market_researcher",
                role="Market Research Analyst",
                goal="Analyze market size, growth trends, and opportunities for startup ideas",
                backstory="""You are an expert market research analyst with 10+ years of experience 
                in analyzing TAM/SAM/SOM, market trends, and growth opportunities. You use data-driven 
                approaches and industry benchmarks to provide accurate market sizing and trend analysis.""",
                tools=["market_data_api", "trend_analysis", "industry_reports"]
            ),
            PortiaAgent(
                name="competitor_analyst",
                role="Competitive Intelligence Specialist",
                goal="Identify competitors, analyze market positioning, and assess competitive threats",
                backstory="""You are a competitive intelligence expert who specializes in identifying 
                direct and indirect competitors, analyzing funding data, market share, and competitive 
                positioning. You have deep knowledge of startup ecosystems across industries.""",
                tools=["competitor_database", "funding_tracker", "market_share_analysis"]
            ),
            PortiaAgent(
                name="financial_analyst",
                role="Financial Modeling Expert",
                goal="Create financial projections, funding estimates, and ROI analysis",
                backstory="""You are a senior financial analyst with expertise in startup valuations, 
                financial modeling, and investment analysis. You create realistic financial projections 
                based on industry benchmarks and business model characteristics.""",
                tools=["financial_modeling", "valuation_tools", "benchmark_data"]
            ),
            PortiaAgent(
                name="risk_assessor",
                role="Risk Management Consultant",
                goal="Identify and evaluate business risks across multiple categories",
                backstory="""You are a risk management expert with extensive experience in identifying 
                market, operational, regulatory, and financial risks. You provide comprehensive risk 
                assessments with mitigation strategies.""",
                tools=["risk_database", "regulatory_tracker", "industry_risk_models"]
            ),
            PortiaAgent(
                name="strategic_advisor",
                role="Strategic Business Consultant",
                goal="Synthesize all analyses into actionable strategic recommendations",
                backstory="""You are a senior strategic consultant with 15+ years advising startups 
                and growth companies. You excel at synthesizing complex data into clear, actionable 
                strategic recommendations and investment decisions.""",
                tools=["synthesis_framework", "decision_models", "strategic_templates"]
            )
        ]
    
    async def analyze_startup_idea(self, idea: str) -> Dict[str, Any]:
        """Orchestrate comprehensive startup analysis using Portia AI agents"""
        
        try:
            # Create analysis workflow
            workflow = await self._create_analysis_workflow(idea)
            
            # Execute workflow with Portia AI
            results = await self._execute_workflow(workflow)
            
            # Parse and structure results
            return self._structure_results(results)
            
        except Exception as e:
            print(f"Portia AI analysis failed: {e}")
            return await self._fallback_analysis(idea)
    
    async def _create_analysis_workflow(self, idea: str) -> Dict[str, Any]:
        """Create Portia AI workflow for startup analysis"""
        
        tasks = [
            PortiaTask(
                description=f"""
                Analyze the market opportunity for this startup idea: {idea}
                
                Provide detailed analysis including:
                1. Total Addressable Market (TAM) size in billions USD
                2. Serviceable Available Market (SAM) size in billions USD
                3. Serviceable Obtainable Market (SOM) size in billions USD
                4. Annual market growth rate as percentage
                5. Key market trends (3-5 specific trends with data)
                
                Focus on data-driven insights with specific numbers and percentages.
                """,
                agent="market_researcher",
                expected_output="Structured market analysis with TAM/SAM/SOM figures, growth rate, and trend data"
            ),
            PortiaTask(
                description=f"""
                Analyze the competitive landscape for: {idea}
                
                Identify and analyze:
                1. 3-5 direct competitors with funding amounts (in millions) and market share percentages
                2. Competitive advantages and differentiation opportunities
                3. Competitive threat level (Low/Medium/High) with detailed reasoning
                
                Provide specific company names, funding data, and market positioning analysis.
                """,
                agent="competitor_analyst",
                expected_output="Competitive analysis with specific competitors, funding data, and threat assessment"
            ),
            PortiaTask(
                description=f"""
                Create financial projections for: {idea}
                
                Analyze and project:
                1. 5-year revenue potential in millions USD
                2. Break-even timeline in months
                3. Total funding required in millions USD
                4. Expected ROI percentage over 5 years
                
                Base projections on industry benchmarks and business model characteristics.
                """,
                agent="financial_analyst",
                expected_output="Financial projections with revenue, timeline, funding, and ROI estimates"
            ),
            PortiaTask(
                description=f"""
                Assess business risks for: {idea}
                
                Identify and evaluate:
                1. 4-6 key business risks across categories (Market, Technical, Regulatory, Financial, Operational)
                2. Risk levels (High/Medium/Low) for each identified risk
                3. Specific risk descriptions and potential impact
                
                Focus on industry-specific and business model-specific risks.
                """,
                agent="risk_assessor",
                expected_output="Comprehensive risk assessment with categorized risks and impact analysis"
            ),
            PortiaTask(
                description=f"""
                Synthesize all previous analyses for: {idea}
                
                Based on market, competitive, financial, and risk analyses, provide:
                1. Overall viability score (0-100 scale)
                2. Investment recommendation (Highly Recommended/Recommended/Caution/Not Recommended)
                3. 5-7 key strategic insights and actionable recommendations
                
                Provide clear, data-backed strategic guidance for decision making.
                """,
                agent="strategic_advisor",
                expected_output="Strategic synthesis with viability score, recommendation, and key insights",
                context=["market_analysis", "competitive_analysis", "financial_analysis", "risk_analysis"]
            )
        ]
        
        return {
            "agents": [agent.dict() for agent in self.agents],
            "tasks": [task.dict() for task in tasks],
            "process": "sequential",
            "verbose": True
        }
    
    async def _execute_workflow(self, workflow: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the workflow using Portia AI API"""
        
        try:
            # Create workflow execution request
            response = await self.client.post(
                f"{self.base_url}/workflows/execute",
                json={
                    "workflow": workflow,
                    "timeout": 300  # 5 minutes
                }
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Portia API error: {response.status_code} - {response.text}")
                raise Exception(f"Portia API returned {response.status_code}")
                
        except httpx.TimeoutException:
            print("Portia AI request timed out")
            raise Exception("Analysis timed out")
        except Exception as e:
            print(f"Portia AI execution error: {e}")
            raise
    
    def _structure_results(self, portia_results: Dict[str, Any]) -> Dict[str, Any]:
        """Structure Portia AI results into DataFoundry format"""
        
        try:
            # Extract results from Portia response
            # This would parse the actual Portia AI response format
            
            # For now, return structured mock data that would come from Portia
            return {
                "market_analysis": {
                    "tam": 2400.0,
                    "sam": 240.0,
                    "som": 24.0,
                    "growth_rate": 12.3,
                    "market_trends": [
                        "AI-powered content creation market growing 35% annually",
                        "Small business digital marketing spend up 28% YoY",
                        "Social media automation adoption increasing 45% among SMBs",
                        "Multi-platform content management becoming standard requirement"
                    ]
                },
                "competition": {
                    "direct_competitors": [
                        {"name": "Hootsuite", "funding": 250, "market_share": 18},
                        {"name": "Buffer", "funding": 45, "market_share": 12},
                        {"name": "Sprout Social", "funding": 135, "market_share": 15},
                        {"name": "Later", "funding": 52, "market_share": 8}
                    ],
                    "competitive_advantage": "AI-powered content generation with brand voice analysis provides unique differentiation",
                    "threat_level": "Medium - Established players but AI differentiation creates opportunity"
                },
                "financial_projections": {
                    "revenue_potential": 180.0,
                    "break_even_timeline": 14,
                    "funding_required": 25.0,
                    "roi_projection": 65
                },
                "risks": [
                    {
                        "category": "Market Risk",
                        "level": "Medium",
                        "description": "AI content quality concerns may slow adoption among quality-focused brands"
                    },
                    {
                        "category": "Technical Risk",
                        "level": "Medium", 
                        "description": "Maintaining brand voice consistency across AI-generated content requires sophisticated NLP"
                    },
                    {
                        "category": "Competitive Risk",
                        "level": "High",
                        "description": "Large incumbents may quickly integrate similar AI features"
                    },
                    {
                        "category": "Regulatory Risk",
                        "level": "Low",
                        "description": "Minimal regulatory barriers for social media management tools"
                    }
                ],
                "recommendation": {
                    "score": 82,
                    "verdict": "Highly Recommended",
                    "key_insights": [
                        "Strong market opportunity with 12.3% growth in AI content creation space",
                        "Clear differentiation through AI-powered brand voice analysis",
                        "Attractive financial projections with 65% ROI and 14-month break-even",
                        "Competitive moat possible through superior AI content quality",
                        "Focus on rapid product development to stay ahead of incumbent responses",
                        "Target quality-conscious SMBs willing to pay premium for brand consistency",
                        "Consider strategic partnerships with content creators for market validation"
                    ]
                }
            }
            
        except Exception as e:
            print(f"Error structuring Portia results: {e}")
            raise
    
    async def _fallback_analysis(self, idea: str) -> Dict[str, Any]:
        """Fallback analysis if Portia AI is unavailable"""
        
        # Use the original simple agents as fallback
        from .llm_breakdown_agent import LLMBreakdownAgent
        from .market_agent import MarketAnalysisAgent
        from .competitor_agent import CompetitorAgent
        from .financial_agent import FinancialAgent
        from .risk_agent import RiskAgent
        from .insight_agent import InsightAgent
        
        try:
            breakdown_agent = LLMBreakdownAgent()
            market_agent = MarketAnalysisAgent()
            competitor_agent = CompetitorAgent()
            financial_agent = FinancialAgent()
            risk_agent = RiskAgent()
            insight_agent = InsightAgent()
            
            # Get breakdown
            breakdown = await breakdown_agent.analyze(idea)
            
            # Run agents in parallel
            tasks = [
                market_agent.analyze(breakdown),
                competitor_agent.analyze(breakdown),
                financial_agent.analyze(breakdown),
                risk_agent.analyze(breakdown)
            ]
            
            market_data, competitor_data, financial_data, risk_data = await asyncio.gather(*tasks)
            
            # Generate insights
            combined_data = {
                "breakdown": breakdown,
                "market_analysis": market_data,
                "competition": competitor_data,
                "financial_projections": financial_data,
                "risks": risk_data
            }
            
            recommendation = await insight_agent.generate_recommendation(combined_data)
            
            return {
                "market_analysis": market_data,
                "competition": competitor_data,
                "financial_projections": financial_data,
                "risks": risk_data,
                "recommendation": recommendation
            }
            
        except Exception as e:
            print(f"Fallback analysis failed: {e}")
            return self._get_minimal_fallback()
    
    def _get_minimal_fallback(self) -> Dict[str, Any]:
        """Minimal fallback response"""
        return {
            "market_analysis": {
                "tam": 1000.0,
                "sam": 100.0,
                "som": 10.0,
                "growth_rate": 5.0,
                "market_trends": ["Analysis temporarily unavailable"]
            },
            "competition": {
                "direct_competitors": [{"name": "Analysis unavailable", "funding": 0, "market_share": 0}],
                "competitive_advantage": "Analysis unavailable",
                "threat_level": "Unknown"
            },
            "financial_projections": {
                "revenue_potential": 50.0,
                "break_even_timeline": 24,
                "funding_required": 10.0,
                "roi_projection": 20
            },
            "risks": [
                {"category": "System Risk", "level": "High", "description": "Analysis system temporarily unavailable"}
            ],
            "recommendation": {
                "score": 50,
                "verdict": "Analysis Incomplete",
                "key_insights": ["Please try again later", "System temporarily unavailable"]
            }
        }
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.aclose()