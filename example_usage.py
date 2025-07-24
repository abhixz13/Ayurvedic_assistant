#!/usr/bin/env python3
"""
Example usage of the Ayurvedic Diagnostic Assistant.
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
    """Main example usage function."""
    print("🩺 Ayurvedic Diagnostic Assistant - Example Usage")
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
    
    # Example symptoms
    example_symptoms = [
        "I have joint pain that worsens in cold weather, cracking sounds in my knees, constipation, and anxiety. I have trouble sleeping and my skin is very dry.",
        "I frequently get heartburn and acid reflux, especially after eating spicy foods. I have a reddish complexion, feel hot often, and get irritated easily.",
        "I feel very tired and sluggish, have gained weight, and feel congested. I sleep too much and have slow digestion."
    ]
    
    print("\n🎯 Running example analysis...")
    
    for i, symptoms in enumerate(example_symptoms, 1):
        print(f"\n📋 Example {i}: {symptoms[:100]}...")
        
        try:
            # Analyze symptoms
            result = engine.analyze_symptoms(symptoms)
            
            if "error" not in result:
                # Extract key information
                dominant_dosha = result.get("dominant_dosha", "Unknown")
                confidence = result.get("confidence", 0)
                diagnosis = result.get("diagnosis", "Not specified")
                
                print(f"✅ Analysis complete!")
                print(f"   📊 Dominant Dosha: {dominant_dosha}")
                print(f"   🎯 Confidence: {confidence:.1%}")
                print(f"   📝 Diagnosis: {diagnosis[:100]}...")
                
                # Generate HTML output
                html_output = display_util.display_diagnosis(result)
                simple_output = display_util.display_simple(result)
                
                print(f"   📄 HTML Output: {len(html_output.data)} characters")
                print(f"   📋 Simple Output: {len(simple_output.data)} characters")
                
            else:
                print(f"❌ Analysis failed: {result['error']}")
                
        except Exception as e:
            print(f"❌ Error processing example {i}: {e}")
    
    print("\n🎉 Example usage completed!")
    print("\n💡 Available interfaces:")
    print("1. Run: python gradio_demo.py (for web interface)")
    print("2. Run: python interactive_demo.py (for command-line interface)")
    print("3. Run: python demo_display.py (for display functionality demo)")

if __name__ == "__main__":
    main() 