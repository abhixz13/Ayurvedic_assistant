#!/usr/bin/env python3
"""
Test script for the conversational chatbot functionality.
"""

import sys
import os

# Add src to path
sys.path.append('src')

def test_conversational_system():
    """Test the conversational chatbot system."""
    print("🧪 Testing Conversational Chatbot System")
    print("=" * 50)
    
    try:
        from src.ai.diagnostic_engine import AyurvedicDiagnosticEngine
        from src.utils.helpers import setup_logging
        
        # Setup logging
        setup_logging('INFO')
        
        # Initialize engine
        print("🚀 Initializing diagnostic engine...")
        engine = AyurvedicDiagnosticEngine()
        print("✅ Engine initialized successfully")
        
        # Test cases
        test_cases = [
            {
                "message": "Hi, how are you?",
                "expected": "greeting",
                "description": "Basic greeting"
            },
            {
                "message": "What's the weather like?",
                "expected": "scope_rejection",
                "description": "Out of scope topic"
            },
            {
                "message": "I have joint pain and anxiety",
                "expected": "health_response",
                "description": "Health-related query"
            },
            {
                "message": "Tell me about Vata dosha",
                "expected": "ayurvedic_response",
                "description": "Ayurvedic knowledge query"
            }
        ]
        
        print("\n🔍 Testing conversational responses...")
        
        for i, test_case in enumerate(test_cases, 1):
            print(f"\n📝 Test {i}: {test_case['description']}")
            print(f"   Input: {test_case['message']}")
            
            try:
                # Test without RAG first
                response = engine.chat(
                    user_message=test_case['message'],
                    use_rag=False,
                    temperature=0.2
                )
                
                print(f"   Response: {response[:100]}...")
                
                # Validate response
                if test_case['expected'] == "greeting":
                    if any(word in response.lower() for word in ['hello', 'hi', 'good', 'well']):
                        print("   ✅ Greeting response detected")
                    else:
                        print("   ⚠️  Unexpected greeting response")
                        
                elif test_case['expected'] == "scope_rejection":
                    if any(word in response.lower() for word in ['outside', 'scope', 'sorry']):
                        print("   ✅ Scope rejection detected")
                    else:
                        print("   ⚠️  Unexpected scope response")
                        
                elif test_case['expected'] in ["health_response", "ayurvedic_response"]:
                    if len(response) > 50 and not "error" in response.lower():
                        print("   ✅ Health/Ayurvedic response generated")
                    else:
                        print("   ⚠️  Unexpected health response")
                
            except Exception as e:
                print(f"   ❌ Error: {e}")
        
        print("\n🎯 Testing health-related detection...")
        
        health_tests = [
            ("I have a headache", True),
            ("What's your favorite color?", False),
            ("Tell me about Pitta dosha", True),
            ("How do I cook pasta?", False),
            ("I feel tired and sluggish", True)
        ]
        
        for message, expected in health_tests:
            result = engine._is_health_related(message)
            status = "✅" if result == expected else "❌"
            print(f"   {status} '{message}' -> Health-related: {result} (expected: {expected})")
        
        print("\n🎉 Conversational system test completed!")
        print("\n💡 To test the full interface:")
        print("   python gradio_demo.py")
        print("   Then visit: http://localhost:7860")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    test_conversational_system() 