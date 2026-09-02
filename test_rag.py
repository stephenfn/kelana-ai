#!/usr/bin/env python3
"""
Session 9 RAG Testing Script
Test Knowledge Base integration with KelanaAI backend
"""

import requests
import json
import sys
from typing import Optional

# Configuration
BASE_URL = "http://localhost:8000"
TEST_EMAIL = "test-rag@kelana.com"
TEST_PASSWORD = "testpassword123"

class RAGTester:
    def __init__(self, base_url: str = BASE_URL):
        self.base_url = base_url
        self.token = None
        self.session = requests.Session()
    
    def register_user(self) -> bool:
        """Register test user"""
        print("\n🔐 [TEST 1] Register User")
        print(f"  Email: {TEST_EMAIL}")
        
        response = self.session.post(
            f"{self.base_url}/api/v1/auth/register",
            json={
                "name": "RAG Test User",
                "email": TEST_EMAIL,
                "password": TEST_PASSWORD
            }
        )
        
        if response.status_code == 200:
            print("  ✅ Registration successful")
            return True
        elif response.status_code == 400 and "already registered" in response.text:
            print("  ⚠️  User already exists (continuing)")
            return True
        else:
            print(f"  ❌ Registration failed: {response.text}")
            return False
    
    def login_user(self) -> bool:
        """Login and get JWT token"""
        print("\n🔐 [TEST 2] Login User")
        print(f"  Email: {TEST_EMAIL}")
        
        response = self.session.post(
            f"{self.base_url}/api/v1/auth/login",
            json={
                "email": TEST_EMAIL,
                "password": TEST_PASSWORD
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            self.token = data["access_token"]
            print(f"  ✅ Login successful")
            print(f"  📋 Token: {self.token[:50]}...")
            return True
        else:
            print(f"  ❌ Login failed: {response.text}")
            return False
    
    def test_ask_endpoint(self, question: str) -> dict:
        """Test /api/v1/ask endpoint"""
        if not self.token:
            print("  ❌ No token available")
            return None
        
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
        
        response = self.session.post(
            f"{self.base_url}/api/v1/ask",
            json={"question": question},
            headers=headers
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"  ❌ Request failed: {response.text}")
            return None
    
    def print_response(self, response: dict, test_number: int):
        """Pretty print response"""
        if response:
            print(f"  📝 Question: {response['question']}")
            print(f"  💬 Answer: {response['answer'][:150]}...")
            if response.get('sources'):
                print(f"  📚 Sources:")
                for source in response['sources']:
                    print(f"     - {source['document']} ({source['source']})")
            print(f"  ✅ Test {test_number} passed")
        else:
            print(f"  ❌ Test {test_number} failed")
    
    def run_all_tests(self):
        """Run all RAG tests"""
        print("=" * 60)
        print("🚀 KelanaAI Session 9 RAG Testing Suite")
        print("=" * 60)
        
        # Test 1: Register
        if not self.register_user():
            print("❌ Registration failed - stopping tests")
            return False
        
        # Test 2: Login
        if not self.login_user():
            print("❌ Login failed - stopping tests")
            return False
        
        # Test 3-7: Knowledge Base queries
        test_cases = [
            ("Do I need a visa to visit Japan?", "Visa Requirements"),
            ("What are the top attractions in Tokyo?", "Tokyo Attractions"),
            ("What should I pack for Japan?", "Packing Tips"),
            ("How much does travel insurance cost?", "Travel Insurance"),
            ("What is the baggage allowance?", "Baggage Info"),
        ]
        
        results = []
        for i, (question, description) in enumerate(test_cases, 3):
            print(f"\n❓ [TEST {i}] {description}")
            print(f"  Question: {question}")
            
            response = self.test_ask_endpoint(question)
            if response:
                self.print_response(response, i)
                results.append(True)
            else:
                results.append(False)
        
        # Test 8: Test /api/v1/assistant endpoint
        print(f"\n❓ [TEST 8] Test /api/v1/assistant Endpoint")
        question = "What are visa requirements for Japan?"
        print(f"  Question: {question}")
        
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
        
        response = self.session.post(
            f"{self.base_url}/api/v1/assistant",
            json={"question": question},
            headers=headers
        )
        
        if response.status_code == 200:
            data = response.json()
            self.print_response(data, 8)
            results.append(True)
        else:
            print(f"  ❌ /api/v1/assistant failed: {response.text}")
            results.append(False)
        
        # Test 9: Test without auth header
        print(f"\n🔒 [TEST 9] Security Test - No Auth Header")
        response = self.session.post(
            f"{self.base_url}/api/v1/ask",
            json={"question": "test"}
        )
        
        if response.status_code == 401:
            print(f"  ✅ Correctly rejected (401)")
            results.append(True)
        else:
            print(f"  ❌ Security test failed - should return 401")
            results.append(False)
        
        # Test 10: Test with invalid token
        print(f"\n🔒 [TEST 10] Security Test - Invalid Token")
        headers = {"Authorization": "Bearer invalid_token"}
        response = self.session.post(
            f"{self.base_url}/api/v1/ask",
            json={"question": "test"},
            headers=headers
        )
        
        if response.status_code == 401:
            print(f"  ✅ Correctly rejected (401)")
            results.append(True)
        else:
            print(f"  ❌ Security test failed - should return 401")
            results.append(False)
        
        # Summary
        print("\n" + "=" * 60)
        print("📊 Test Summary")
        print("=" * 60)
        passed = sum(results)
        total = len(results)
        print(f"✅ Passed: {passed}/{total}")
        print(f"❌ Failed: {total - passed}/{total}")
        
        if passed == total:
            print("\n🎉 All tests passed!")
            return True
        else:
            print(f"\n⚠️  {total - passed} test(s) failed")
            return False


def main():
    """Main entry point"""
    tester = RAGTester()
    
    try:
        success = tester.run_all_tests()
        sys.exit(0 if success else 1)
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Cannot connect to backend")
        print("   Make sure the backend is running:")
        print("   cd backend && python -m uvicorn main:app --reload")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
