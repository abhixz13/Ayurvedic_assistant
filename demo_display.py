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
from src.ui.display import DiagnosisDisplay

def main():
    """Main demo function."""
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
    
    # Initialize display utility
    display_util = DiagnosisDisplay()
    
    # Example symptoms for different doshas
    example_symptoms = {
        "Vata": "I have joint pain that worsens in cold weather, cracking sounds in my knees, constipation, and anxiety. I have trouble sleeping and my skin is very dry.",
        "Pitta": "I frequently get heartburn and acid reflux, especially after eating spicy foods. I have a reddish complexion, feel hot often, and get irritated easily.",
        "Kapha": "I feel very tired and sluggish, have gained weight, and feel congested. I sleep too much and have slow digestion."
    }
    
    print("\n🎯 Running diagnostic analysis...")
    print("📊 This demo shows the beautiful HTML output capabilities")
    
    # Process each example
    for dosha_type, symptoms in example_symptoms.items():
        print(f"\n🔍 Analyzing {dosha_type} symptoms...")
        
        try:
            # Analyze symptoms
            result = engine.analyze_symptoms(symptoms)
            
            if "error" not in result:
                # Generate HTML output
                html_output = display_util.display_diagnosis(result)
                simple_output = display_util.display_simple(result)
                
                # Print summary to console
                dominant_dosha = result.get("dominant_dosha", "Unknown")
                confidence = result.get("confidence", 0)
                
                print(f"✅ Analysis complete!")
                print(f"   📊 Dominant Dosha: {dominant_dosha}")
                print(f"   🎯 Confidence: {confidence:.1%}")
                print(f"   📝 HTML Output Length: {len(html_output.data)} characters")
                print(f"   📋 Simple Output Length: {len(simple_output.data)} characters")
                
                # Show a snippet of the HTML
                html_preview = html_output.data[:200] + "..." if len(html_output.data) > 200 else html_output.data
                print(f"   🎨 HTML Preview: {html_preview}")
                
            else:
                print(f"❌ Error in analysis: {result['error']}")
                
        except Exception as e:
            print(f"❌ Error processing {dosha_type} symptoms: {e}")
    
    print("\n🎉 Display demo completed!")
    print("\n💡 Next steps:")
    print("1. Run: python gradio_demo.py (for web interface)")
    print("2. Run: python interactive_demo.py (for command-line interface)")
    print("3. Check the HTML output files for detailed formatting")

if __name__ == "__main__":
    main() 