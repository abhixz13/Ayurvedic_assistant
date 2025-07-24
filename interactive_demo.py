#!/usr/bin/env python3
"""
Interactive demo for the Ayurvedic Diagnostic Assistant display functionality.
"""

import sys
import os
from pathlib import Path

# Add src to path
sys.path.append('src')

from src.utils.helpers import setup_logging, validate_environment
from src.ai.diagnostic_engine import AyurvedicDiagnosticEngine
from src.ui.display import DiagnosisDisplay

def main():
    """Main interactive demo function."""
    print("🩺 Ayurvedic Diagnostic Assistant - Interactive Demo")
    print("=" * 60)
    
    # Setup logging
    setup_logging('INFO')
    
    # Validate environment
    print("🔍 Validating environment...")
    validation = validate_environment()
    if not validation['environment_valid']:
        print("❌ Environment validation failed:")
        for req in validation['missing_requirements']:
            print(f"  - {req}")
        return
    
    print("✅ Environment is valid")
    
    # Initialize diagnostic engine
    print("🚀 Initializing diagnostic engine...")
    try:
        engine = AyurvedicDiagnosticEngine()
        print("✅ Diagnostic engine initialized")
    except Exception as e:
        print(f"❌ Failed to initialize engine: {e}")
        print("Please check your Google API key in .env file")
        return
    
    # Initialize display utility
    display_util = DiagnosisDisplay()
    
    print("\n🎯 Interactive Demo Started!")
    print("💡 Type 'quit' to exit, 'help' for commands, 'demo' for examples")
    
    while True:
        try:
            # Get user input
            symptoms = input("\n📝 Enter your symptoms: ").strip()
            
            # Handle special commands
            if symptoms.lower() in ['quit', 'exit', 'q']:
                print("👋 Goodbye! Thank you for using the Ayurvedic Diagnostic Assistant.")
                break
            elif symptoms.lower() in ['help', 'h']:
                print("\n📚 Available Commands:")
                print("  - 'quit' or 'exit': Exit the demo")
                print("  - 'help': Show this help message")
                print("  - 'demo': Show example symptoms")
                print("  - Enter symptoms: Get Ayurvedic analysis")
                continue
            elif symptoms.lower() in ['demo', 'example']:
                print("\n🧪 Example Symptoms:")
                print("1. Vata: 'I have joint pain, dry skin, and anxiety'")
                print("2. Pitta: 'I get heartburn and skin rashes'")
                print("3. Kapha: 'I feel tired and have gained weight'")
                continue
            elif not symptoms:
                print("❌ Please enter symptoms for analysis.")
                continue
            
            # Analyze symptoms
            print("🔍 Analyzing symptoms...")
            result = engine.analyze_symptoms(symptoms)
            
            if "error" not in result:
                # Show console summary
                dominant_dosha = result.get("dominant_dosha", "Unknown")
                confidence = result.get("confidence", 0)
                diagnosis = result.get("diagnosis", "Not specified")
                
                print(f"\n✅ Analysis Complete!")
                print(f"📊 Dominant Dosha: {dominant_dosha}")
                print(f"🎯 Confidence: {confidence:.1%}")
                print(f"📝 Diagnosis: {diagnosis[:200]}...")
                
                # Ask about HTML display
                display_choice = input("\n🎨 Would you like to see the detailed HTML display? (y/n): ").strip().lower()
                if display_choice in ['y', 'yes']:
                    html_output = display_util.display_diagnosis(result)
                    print("📄 HTML output generated successfully!")
                    
                    # Ask about simple summary
                    simple_choice = input("\n📋 Would you like to see the simple summary? (y/n): ").strip().lower()
                    if simple_choice in ['y', 'yes']:
                        simple_output = display_util.display_simple(result)
                        print("📄 Simple summary generated successfully!")
                
                # Show supporting evidence
                evidence = result.get("supporting_evidence", {})
                if evidence:
                    print(f"\n🔍 Supporting Evidence:")
                    for dosha, symptoms_list in evidence.items():
                        if symptoms_list:
                            print(f"  {dosha}: {', '.join(symptoms_list[:3])}...")
                
                # Show treatment recommendations
                treatments = result.get("recommended_treatments", {})
                if treatments:
                    print(f"\n💊 Treatment Recommendations:")
                    for category, items in list(treatments.items())[:3]:
                        if items and category not in ['important_notes', 'important_note']:
                            if isinstance(items, list):
                                print(f"  {category}: {len(items)} recommendations")
                            else:
                                print(f"  {category}: {str(items)[:50]}...")
                
            else:
                print(f"❌ Analysis failed: {result['error']}")
                
        except KeyboardInterrupt:
            print("\n👋 Goodbye! Thank you for using the Ayurvedic Diagnostic Assistant.")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            print("💡 Try again or type 'help' for assistance.")

if __name__ == "__main__":
    main() 