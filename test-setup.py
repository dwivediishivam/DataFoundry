#!/usr/bin/env python3
"""
Test script to verify DataFoundry setup
"""

import sys
import os
import requests
import time

def test_backend():
    """Test if backend is running and responding"""
    try:
        print("🔧 Testing backend connection...")
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            print("✅ Backend is running successfully!")
            return True
        else:
            print(f"❌ Backend returned status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to backend. Make sure it's running on port 8000")
        return False
    except Exception as e:
        print(f"❌ Backend test failed: {e}")
        return False

def test_frontend():
    """Test if frontend is running"""
    try:
        print("🎨 Testing frontend connection...")
        response = requests.get("http://localhost:3000", timeout=5)
        if response.status_code == 200:
            print("✅ Frontend is running successfully!")
            return True
        else:
            print(f"❌ Frontend returned status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to frontend. Make sure it's running on port 3000")
        return False
    except Exception as e:
        print(f"❌ Frontend test failed: {e}")
        return False

def test_api_analysis():
    """Test the analysis API with a sample idea"""
    try:
        print("🧠 Testing AI analysis...")
        
        test_idea = "A mobile app that connects dog owners with local dog walkers for on-demand pet care services."
        
        response = requests.post(
            "http://localhost:8000/analyze",
            json={"idea": test_idea},
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ AI analysis working!")
            print(f"   Sample result: {data['recommendation']['verdict']}")
            print(f"   Viability score: {data['recommendation']['score']}/100")
            return True
        else:
            print(f"❌ Analysis API returned status code: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Analysis test failed: {e}")
        return False

def main():
    print("🧪 DataFoundry Setup Test")
    print("=" * 40)
    
    # Test backend
    backend_ok = test_backend()
    time.sleep(1)
    
    # Test frontend
    frontend_ok = test_frontend()
    time.sleep(1)
    
    # Test API if backend is working
    api_ok = False
    if backend_ok:
        api_ok = test_api_analysis()
    
    print("\n" + "=" * 40)
    print("📊 Test Results:")
    print(f"   Backend: {'✅ PASS' if backend_ok else '❌ FAIL'}")
    print(f"   Frontend: {'✅ PASS' if frontend_ok else '❌ FAIL'}")
    print(f"   AI Analysis: {'✅ PASS' if api_ok else '❌ FAIL'}")
    
    if backend_ok and frontend_ok and api_ok:
        print("\n🎉 All tests passed! DataFoundry is ready to use.")
        print("   Visit http://localhost:3000 to start analyzing startup ideas!")
    else:
        print("\n⚠️  Some tests failed. Check the error messages above.")
        
        if not backend_ok:
            print("   💡 Try: cd backend && source venv/bin/activate && uvicorn main:app --reload")
        if not frontend_ok:
            print("   💡 Try: npm run dev")

if __name__ == "__main__":
    main()