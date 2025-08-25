import asyncio
import sys
import os
sys.path.append('backend')

from backend.agents.llm_breakdown_agent import LLMBreakdownAgent

async def test_breakdown():
    agent = LLMBreakdownAgent()
    
    ideas = [
        'Rural EdTech Kits – Offline-first tablets with preloaded learning apps for schools with poor connectivity.',
        'Food delivery app for small towns in India with local restaurant partnerships',
        'EV Charging Network Mapping – App to find, book, and even pay for EV charging points across India.'
    ]
    
    for idea in ideas:
        print(f'\n=== Testing: {idea[:50]}... ===')
        result = await agent.analyze(idea)
        print(f'Industry: {result.get("industry", "Unknown")}')
        print(f'Keywords: {result.get("keywords", [])[:5]}')
        print(f'Business Model: {result.get("business_model", "Unknown")}')

if __name__ == "__main__":
    asyncio.run(test_breakdown())