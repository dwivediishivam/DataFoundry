#!/usr/bin/env python3
"""
Simple test script for DataFoundry API
"""

import requests
import json
import sys

def test_api():
    url = "http://localhost:8000/analyze"
    
    test_idea = """
    An on-demand courier service using drones and small aircraft for same-day delivery in urban areas. 
    The platform would connect businesses needing urgent deliveries with certified pilots operating 
    lightweight aircraft. Target customers include medical facilities, legal firms, and e-commerce 
    businesses requiring rapid document or small package delivery within 50-mile radius of major cities.
    """
    
    payload = {"idea": test_idea.strip()}
    
    try:
        print("Testing DataFoundry API...")
        print(f"Sending request to: {url}")
        
        response = requests.post(url, json=payload, timeout=30)
        
        if response.status_code == 200:
            print("✅ API test successful!")
            data = response.json()
            
            print("\n📊 Analysis Results:")
            print(f"Overall Score: {data['recommendation']['score']}/100")
            print(f"Verdict: {data['recommendation']['verdict']}")
            print(f"Market Size (TAM): ${data['market_analysis']['tam']}B")
            print(f"Growth Rate: {data['market_analysis']['growth_rate']}%")
            print(f"Revenue Potential: ${data['financial_projections']['revenue_potential']}M")
            print(f"Break-even Timeline: {data['financial_projections']['break_even_timeline']} months")
            
            print("\n🔍 Key Insights:")
            for insight in data['recommendation']['key_insights']:
                print(f"  • {insight}")
                
        else:
            print(f"❌ API test failed with status code: {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection failed. Make sure the backend is running on http://localhost:8000")
    except requests.exceptions.Timeout:
        print("❌ Request timed out. The analysis might be taking longer than expected.")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    test_api()