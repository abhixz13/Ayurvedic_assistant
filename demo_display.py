#!/usr/bin/env python3
"""
Demo script showing how to use the Ayurvedic Diagnostic Assistant display functionality.
"""

import sys
import os
from pathlib import Path

# Add src to path
sys.path.append('src')

from src.utils.helpers import setup_logging, validate_environment
from src.ai.diagnostic_engine import AyurvedicDiagnosticEngine
from src.ui.widgets import InteractiveDiagnosticWidget, BatchAnalysisWidget
from src.ui.display import DiagnosisDisplay

def main():
    """Main demonstration function."""
    print("🩺 Ayurvedic Diagnostic Assistant - Display Demo")
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
    
    # Example symptoms for testing
    example_symptoms = {
        "Vata Imbalance": "I have joint pain that worsens in cold weather, cracking sounds in my knees, constipation, and anxiety. I have trouble sleeping and my skin is very dry.",
        "Pitta Imbalance": "I frequently get heartburn and acid reflux, especially after eating spicy foods. I have a reddish complexion, feel hot often, and get irritated easily.",
        "Kapha Imbalance": "I feel very tired and sluggish, have gained weight, and feel congested. I sleep too much and have slow digestion."
    }
    
    # Create display utility
    display_util = DiagnosisDisplay()
    
    print("\n📊 Testing Display Functionality")
    print("=" * 60)
    
    # Test each example
    for dosha_type, symptoms in example_symptoms.items():
        print(f"\n🧪 Testing {dosha_type}:")
        print(f"Symptoms: {symptoms[:100]}...")
        
        # Analyze symptoms
        result = engine.analyze_symptoms(symptoms)
        
        if "error" not in result:
            print("✅ Analysis completed successfully")
            
            # Display results using the display utility
            print("\n📋 Displaying Results:")
            print("-" * 40)
            
            # Show full diagnosis display
            html_output = display_util.display_diagnosis(result)
            print("Full diagnosis display generated successfully")
            
            # Show simple display
            simple_output = display_util.display_simple(result)
            print("Simple summary display generated successfully")
            
            # Extract key information for console display
            dominant_dosha = result.get("dominant_dosha", "Unknown")
            diagnosis_text = result.get("diagnosis", "Not specified")
            
            print(f"\n📊 Console Summary:")
            print(f"   Dominant Dosha: {dominant_dosha}")
            print(f"   Diagnosis: {diagnosis_text[:100]}...")
            
            # Show recommendations summary
            recommendations = result.get("recommended_treatments", {})
            if recommendations:
                print(f"   Treatment Categories: {len(recommendations)}")
                for category, items in list(recommendations.items())[:3]:
                    if items and category not in ['important_notes', 'important_note']:
                        if isinstance(items, list):
                            print(f"     - {category}: {len(items)} items")
                        else:
                            print(f"     - {category}: {str(items)[:50]}...")
            
        else:
            print(f"❌ Analysis failed: {result['error']}")
    
    print(f"\n{'='*60}")
    print("🎉 Display Demo Completed!")
    print("\n📋 To use the interactive interface:")
    print("1. Run: jupyter notebook notebooks/main_assistant.ipynb")
    print("2. Follow the notebook instructions")
    print("\n💡 Key Display Features:")
    print("- Beautiful HTML formatting with colors and icons")
    print("- Dosha badges with color coding")
    print("- Organized treatment recommendations")
    print("- Supporting evidence sections")
    print("- Medical disclaimers")
    print("- Analysis metadata")
    
    print("\n⚠️  Disclaimer:")
    print("This tool is for educational purposes only.")
    print("Always consult qualified Ayurvedic practitioners for proper diagnosis and treatment.")

if __name__ == "__main__":
    main() 