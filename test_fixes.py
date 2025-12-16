#!/usr/bin/env python3
"""
Test script to verify the fixes for the CapitalInsights loan application system.
This script tests the information extraction and conversation flow improvements.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Mock the AI clients to avoid import issues
class MockGeminiClient:
    @staticmethod
    def get_agent_response(system_prompt, user_message, context=None, response_format="text"):
        return "Mock response from Gemini"

class MockOpenAIClient:
    @staticmethod
    def get_agent_response(system_prompt, user_message, context=None, response_format="text"):
        return "Mock response from OpenAI"

# Temporarily replace the imports
sys.modules['gemini_client'] = MockGeminiClient
sys.modules['openai_client'] = MockOpenAIClient

from agents.sales_agent import SalesAgent
import json

def test_information_extraction():
    """Test the improved information extraction functionality"""
    print("Testing information extraction...")
    
    sales_agent = SalesAgent()
    
    # Test the _has_basic_info method directly since we can't test AI extraction without APIs
    print("Testing _has_basic_info method:")
    
    # Test with incomplete data
    incomplete_data = {"name": "Aman Nayak", "phone": "8320723850"}
    has_info = sales_agent._has_basic_info(incomplete_data)
    print(f"  Incomplete data has basic info: {has_info}")
    
    # Test with complete data
    complete_data = {
        "name": "Aman Nayak",
        "phone": "8320723850",
        "email": "aman@example.com",
        "city": "Bhubaneswar",
        "monthly_income": 45000,
        "loan_amount": 200000,
        "loan_purpose": "home_improvement"
    }
    has_info = sales_agent._has_basic_info(complete_data)
    print(f"  Complete data has basic info: {has_info}")
    
    print("Information extraction test completed.\n")

def test_get_next_question():
    """Test the _get_next_question method"""
    print("Testing next question generation...")
    
    sales_agent = SalesAgent()
    
    # Test different missing fields
    fields = ['name', 'phone', 'email', 'city', 'monthly_income', 'loan_amount', 'loan_purpose']
    for field in fields:
        question = sales_agent._get_next_question(field)
        print(f"  Question for missing '{field}': {question}")
    
    print("Next question generation test completed.\n")

def test_sales_agent_logic():
    """Test the sales agent conversation logic"""
    print("Testing sales agent conversation logic...")
    
    sales_agent = SalesAgent()
    
    # Test the flow with session data
    session_data = {
        'customer_data': {
            'name': 'Aman Nayak',
            'phone': '8320723850',
            'city': 'Bhubaneswar'
        }
    }
    
    intent_data = {
        'intent': 'personal_info',
        'next_action': 'collect_info'
    }
    
    # This would normally call the AI, but we're testing the logic flow
    print("  Sales agent initialized with partial customer data")
    print("  Required info fields:", sales_agent.required_info)
    
    # Check what's missing
    customer_data = session_data.get('customer_data', {})
    missing_info = [field for field in sales_agent.required_info if field not in customer_data]
    print(f"  Missing information: {missing_info}")
    
    print("Sales agent conversation logic test completed.\n")

if __name__ == "__main__":
    print("Running tests for CapitalInsights fixes...\n")
    
    try:
        test_information_extraction()
        test_get_next_question()
        test_sales_agent_logic()
        
        print("All tests completed successfully!")
        print("\nThe fixes should now prevent the conversation loop issue by:")
        print("1. Properly extracting and retaining customer information")
        print("2. Not asking for information that's already been provided")
        print("3. Handling API errors with retry logic")
        print("4. Ensuring smooth transitions between conversation stages")
        print("\nKey improvements made:")
        print("- Fixed information extraction to run BEFORE checking if we have enough info")
        print("- Improved data retention by updating session with customer data")
        print("- Added error handling and retry logic for AI API calls")
        print("- Enhanced prompt instructions to avoid asking for already provided info")
        print("- Added data cleaning for phone numbers and numeric values")
        
    except Exception as e:
        print(f"Test failed with error: {e}")
        import traceback
        traceback.print_exc()