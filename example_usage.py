#!/usr/bin/env python3
"""
Example usage of the Ayurvedic Diagnostic Assistant.
"""

import sys
import os
from pathlib import Path

# Add src to path
sys.path.append('src')

from src.utils.helpers import setup_logging, validate_environment, create_sample_data
from src.ai.diagnostic_engine import AyurvedicDiagnosticEngine
from src.ui.display import DiagnosisDisplay

def main():
    """Main example function."""
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
    
    # Create sample data if needed
    if not os.path.exists("data/raw"):
        print("📚 Creating sample data...")
        sample_data = create_sample_data()
        print(f"✅ Created {sample_data['sample_files_created']} sample files")
    
    # Initialize diagnostic engine
    print("🚀 Initializing diagnostic engine...")
    try:
        engine = AyurvedicDiagnosticEngine()
        print("✅ Diagnostic engine initialized")
    except Exception as e:
        print(f"❌ Failed to initialize engine: {e}")
        print("Please check your Google API key in .env file")
        return
    
    # Test the system
    print("🧪 Testing system...")
    test_results = engine.test_system()
    for test_name, result in test_results.items():
        status = "✅" if result else "❌"
        print(f"{status} {test_name}: {result}")
    
    if not all(test_results.values()):
        print("⚠️  Some tests failed, but continuing...")
    
    # Example symptoms
    example_symptoms = [
        {
            "description": "Vata Imbalance",
            "symptoms": "I have joint pain that worsens in cold weather, cracking sounds in my knees, constipation, and anxiety. I have trouble sleeping and my skin is very dry."
        },
        {
            "description": "Pitta Imbalance", 
            "symptoms": "I frequently get heartburn and acid reflux, especially after eating spicy foods. I have a reddish complexion, feel hot often, and get irritated easily."
        },
        {
            "description": "Kapha Imbalance",
            "symptoms": "I feel very tired and sluggish, have gained weight, and feel congested. I sleep too much and have slow digestion."
        }
    ]
    
    # Create display utility
    display = DiagnosisDisplay()
    
    # Analyze each example
    print("\n📊 Running example analyses...")
    for i, example in enumerate(example_symptoms, 1):
        print(f"\n{'='*60}")
        print(f"Example {i}: {example['description']}")
        print(f"Symptoms: {example['symptoms']}")
        print(f"{'='*60}")
        
        # Analyze symptoms
        result = engine.analyze_symptoms(example['symptoms'])
        
        # Display results
        if "error" not in result:
            print(f"✅ Analysis completed")
            
            # Handle different JSON structures
            dominant_dosha = "Unknown"
            diagnosis_text = "Not specified"
            recommendations = {}
            
            # Try different possible structures
            if 'ayurvedic_diagnosis' in result:
                diagnosis = result['ayurvedic_diagnosis']
                if isinstance(diagnosis, dict):
                    dominant_dosha = diagnosis.get('dosha_imbalance', 'Unknown')
                    diagnosis_text = diagnosis.get('disease_name', 'Not specified')
                    recommendations = diagnosis.get('recommendations', {})
            elif 'ayurvedic_analysis' in result:
                analysis = result['ayurvedic_analysis']
                if isinstance(analysis, dict):
                    dominant_dosha = analysis.get('dosha_imbalance', 'Unknown')
                    diagnosis_text = analysis.get('diagnosis', 'Not specified')
                    recommendations = analysis.get('recommendations', {})
            elif 'dosha_imbalance' in result:
                dominant_dosha = result.get('dosha_imbalance', 'Unknown')
                diagnosis_text = result.get('diagnosis', 'Not specified')
                recommendations = result.get('ayurvedic_recommendations', {})
            else:
                # Original structure
                dominant_dosha = result.get('dominant_dosha', 'Unknown')
                diagnosis_text = result.get('diagnosis', 'Not specified')
                recommendations = result.get('recommended_treatments', {})
            
            print(f"Dominant Dosha: {dominant_dosha}")
            print(f"Diagnosis: {diagnosis_text}")
            
            # Show recommendations
            if recommendations:
                print("\n🌱 Treatment Recommendations:")
                for category, items in recommendations.items():
                    if items and category not in ['important_notes', 'important_note']:
                        if isinstance(items, list):
                            print(f"  {category.title()}: {', '.join(items[:3])}...")
                        else:
                            print(f"  {category.title()}: {items[:100]}...")
        else:
            print(f"❌ Analysis failed: {result['error']}")
    
    print(f"\n{'='*60}")
    print("🎉 Example usage completed!")
    print("\n📋 To use the interactive interface:")
    print("1. Run: jupyter notebook notebooks/main_assistant.ipynb")
    print("2. Follow the notebook instructions")
    
    print("\n⚠️  Disclaimer:")
    print("This tool is for educational purposes only.")
    print("Always consult qualified Ayurvedic practitioners for proper diagnosis and treatment.")

if __name__ == "__main__":
    main() 