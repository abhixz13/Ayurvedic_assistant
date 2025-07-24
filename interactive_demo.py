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
    """Interactive demonstration function."""
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
    
    # Create display utility
    display_util = DiagnosisDisplay()
    
    print("\n🎯 Interactive Demo Started!")
    print("Enter your symptoms below for Ayurvedic analysis.")
    print("Type 'quit' to exit, 'help' for examples, or 'demo' for sample symptoms.")
    print("-" * 60)
    
    while True:
        try:
            # Get user input
            symptoms = input("\n📝 Enter your symptoms: ").strip()
            
            if symptoms.lower() == 'quit':
                print("👋 Goodbye!")
                break
            elif symptoms.lower() == 'help':
                print("\n💡 Example symptoms you can try:")
                print("1. 'I have joint pain, dry skin, and anxiety'")
                print("2. 'I get heartburn after spicy foods and feel hot often'")
                print("3. 'I feel tired, have gained weight, and sleep too much'")
                print("4. 'I have constipation, cracking joints, and trouble sleeping'")
                continue
            elif symptoms.lower() == 'demo':
                print("\n🧪 Running demo with sample symptoms...")
                symptoms = "I have joint pain that worsens in cold weather, cracking sounds in my knees, constipation, and anxiety. I have trouble sleeping and my skin is very dry."
                print(f"Demo symptoms: {symptoms}")
            
            if not symptoms:
                print("❌ Please enter symptoms for analysis.")
                continue
            
            print(f"\n🔄 Analyzing symptoms...")
            
            # Analyze symptoms
            result = engine.analyze_symptoms(symptoms)
            
            if "error" not in result:
                print("✅ Analysis completed successfully!")
                
                # Extract key information
                dominant_dosha = result.get("dominant_dosha", "Unknown")
                diagnosis_text = result.get("diagnosis", "Not specified")
                
                print(f"\n📊 Analysis Results:")
                print(f"   🎯 Dominant Dosha: {dominant_dosha}")
                print(f"   📋 Diagnosis: {diagnosis_text}")
                
                # Show recommendations summary
                recommendations = result.get("recommended_treatments", {})
                if recommendations:
                    print(f"   🌱 Treatment Categories Available:")
                    for category, items in recommendations.items():
                        if items and category not in ['important_notes', 'important_note']:
                            if isinstance(items, list):
                                print(f"     - {category}: {len(items)} recommendations")
                            else:
                                print(f"     - {category}: {str(items)[:50]}...")
                
                # Ask user if they want to see detailed display
                display_choice = input("\n🎨 Would you like to see the detailed HTML display? (y/n): ").strip().lower()
                
                if display_choice in ['y', 'yes']:
                    print("\n📋 Generating detailed display...")
                    
                    # Generate HTML display
                    html_output = display_util.display_diagnosis(result)
                    print("✅ Detailed HTML display generated successfully!")
                    print("💡 In a Jupyter notebook, this would show beautiful formatted output with:")
                    print("   - Color-coded dosha badges")
                    print("   - Organized treatment sections")
                    print("   - Supporting evidence")
                    print("   - Lifestyle recommendations")
                    print("   - Medical disclaimers")
                    
                    # Show simple version
                    simple_choice = input("\n📋 Would you like to see the simple summary? (y/n): ").strip().lower()
                    if simple_choice in ['y', 'yes']:
                        simple_output = display_util.display_simple(result)
                        print("✅ Simple summary display generated!")
                
                # Show supporting evidence
                evidence = result.get("supporting_evidence", {})
                if evidence:
                    print(f"\n📋 Supporting Evidence:")
                    for key, value in evidence.items():
                        if value:
                            if isinstance(value, list):
                                print(f"   - {key}: {len(value)} indicators")
                            else:
                                print(f"   - {key}: {str(value)[:50]}...")
                
            else:
                print(f"❌ Analysis failed: {result['error']}")
                print("💡 Try rephrasing your symptoms or check your internet connection.")
            
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            print("💡 Please try again or type 'help' for examples.")
    
    print(f"\n{'='*60}")
    print("🎉 Interactive Demo Completed!")
    print("\n📋 To use the full interactive interface:")
    print("1. Run: jupyter notebook notebooks/main_assistant.ipynb")
    print("2. Use the interactive widgets for a better experience")
    print("\n💡 Key Features Available:")
    print("- Real-time symptom analysis")
    print("- Beautiful HTML display formatting")
    print("- Dosha identification and recommendations")
    print("- Treatment and lifestyle advice")
    print("- Supporting evidence and indicators")
    
    print("\n⚠️  Important Disclaimer:")
    print("This tool is for educational purposes only.")
    print("Always consult qualified Ayurvedic practitioners for proper diagnosis and treatment.")

if __name__ == "__main__":
    main() 