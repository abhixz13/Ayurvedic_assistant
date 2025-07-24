#!/usr/bin/env python3
"""
Demo script for the Conversational Ayurvedic Chat Assistant.
"""

import sys
import os
from pathlib import Path

# Add src to path
sys.path.append('src')

from src.utils.helpers import setup_logging, validate_environment
from src.ai.diagnostic_engine import AyurvedicDiagnosticEngine
from src.ui.gradio_ui import GradioChatUI, GradioDiagnosticUI, GradioBatchUI

def main():
    """Main demo function for Conversational Chat UI."""
    print("🩺 Ayurvedic Chat Assistant - Conversational Demo")
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
    
    # Define the chat callback function
    def chat_callback(message: str, use_rag: bool = True, temperature: float = 0.2):
        """Callback function for the chat UI."""
        try:
            # Use the new chat method
            response = engine.chat(
                user_message=message,
                use_rag=use_rag,
                temperature=temperature
            )
            return response
        except Exception as e:
            return f"I apologize, but I encountered an error: {str(e)}"
    
    # Define the diagnostic callback function (for legacy interface)
    def diagnostic_callback(symptoms: str, use_rag: bool = True, temperature: float = 0.2):
        """Callback function for the diagnostic UI."""
        try:
            # Configure engine parameters
            engine.use_rag = use_rag
            engine.temperature = temperature
            
            # Analyze symptoms
            result = engine.analyze_symptoms(symptoms)
            return result
        except Exception as e:
            return {"error": str(e)}
    
    # Define batch diagnostic callback
    def batch_diagnostic_callback(symptoms_list: list):
        """Callback function for batch analysis."""
        results = []
        for symptoms in symptoms_list:
            try:
                result = engine.analyze_symptoms(symptoms)
                results.append(result)
            except Exception as e:
                results.append({"error": str(e)})
        return results
    
    print("\n🎯 Starting Conversational Chat UI...")
    print("📱 The web interface will open in your browser")
    print("🌐 You can access it from any device on your network")
    
    # Create and launch the chat interface
    try:
        # Create the conversational chat UI
        chat_ui = GradioChatUI(chat_callback)
        
        # Launch the interface
        print("\n🚀 Launching Conversational Chat interface...")
        print("💡 Features available:")
        print("   - Natural conversation with Dr. Priya")
        print("   - Human-like responses and greetings")
        print("   - Scope detection (Ayurveda/health only)")
        print("   - RAG knowledge integration")
        print("   - Temperature control for creativity")
        print("   - Example conversation starters")
        print("   - Chat history and clear function")
        
        # Launch with specific settings
        chat_ui.launch(
            server_name="0.0.0.0",  # Allow external access
            server_port=7860,       # Default Gradio port
            share=False,            # Set to True to create public link
            show_error=True,        # Show detailed errors
            quiet=False             # Show launch information
        )
        
    except Exception as e:
        print(f"❌ Error launching chat interface: {e}")
        print("💡 Make sure you have Gradio installed: pip install gradio")

def launch_diagnostic_ui():
    """Launch the legacy diagnostic interface."""
    print("🔍 Launching Legacy Diagnostic Interface...")
    
    # Setup and validation (same as main)
    setup_logging('INFO')
    validation = validate_environment()
    if not validation['environment_valid']:
        print("❌ Environment validation failed")
        return
    
    try:
        engine = AyurvedicDiagnosticEngine()
    except Exception as e:
        print(f"❌ Failed to initialize engine: {e}")
        return
    
    def diagnostic_callback(symptoms: str, use_rag: bool = True, temperature: float = 0.2):
        try:
            result = engine.analyze_symptoms(symptoms)
            return result
        except Exception as e:
            return {"error": str(e)}
    
    # Create and launch diagnostic UI
    diagnostic_ui = GradioDiagnosticUI(diagnostic_callback)
    diagnostic_ui.launch(
        server_name="0.0.0.0",
        server_port=7861,  # Different port for diagnostic UI
        share=False,
        show_error=True,
        quiet=False
    )

def launch_batch_ui():
    """Launch the batch analysis interface."""
    print("📊 Launching Batch Analysis UI...")
    
    # Setup and validation (same as main)
    setup_logging('INFO')
    validation = validate_environment()
    if not validation['environment_valid']:
        print("❌ Environment validation failed")
        return
    
    try:
        engine = AyurvedicDiagnosticEngine()
    except Exception as e:
        print(f"❌ Failed to initialize engine: {e}")
        return
    
    def batch_diagnostic_callback(symptoms_list: list):
        results = []
        for symptoms in symptoms_list:
            try:
                result = engine.analyze_symptoms(symptoms)
                results.append(result)
            except Exception as e:
                results.append({"error": str(e)})
        return results
    
    # Create and launch batch UI
    batch_ui = GradioBatchUI(batch_diagnostic_callback)
    batch_ui.launch(
        server_name="0.0.0.0",
        server_port=7862,  # Different port for batch UI
        share=False,
        show_error=True,
        quiet=False
    )

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Launch Ayurvedic Chat Assistant")
    parser.add_argument("--mode", choices=["chat", "diagnostic", "batch"], default="chat", 
                       help="Launch mode: chat (default), diagnostic, or batch")
    
    args = parser.parse_args()
    
    if args.mode == "diagnostic":
        launch_diagnostic_ui()
    elif args.mode == "batch":
        launch_batch_ui()
    else:
        main()  # Default to chat mode 