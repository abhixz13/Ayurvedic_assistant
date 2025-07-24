"""
Gradio UI for the Ayurvedic Diagnostic Assistant.
"""

import logging
import gradio as gr
from typing import Dict, Any, Callable, Optional, Tuple
from src.ui.display import DiagnosisDisplay

logger = logging.getLogger(__name__)


class GradioDiagnosticUI:
    """Gradio UI for Ayurvedic diagnosis."""
    
    def __init__(self, diagnostic_callback: Callable[[str, bool, float], Dict[str, Any]]):
        """
        Initialize the Gradio UI.
        
        Args:
            diagnostic_callback: Function that takes symptoms, use_rag, temperature and returns diagnosis
        """
        self.diagnostic_callback = diagnostic_callback
        self.display = DiagnosisDisplay()
        self.interface = None
    
    def create_interface(self) -> gr.Interface:
        """Create the Gradio interface."""
        
        # Custom CSS for better styling
        css = """
        .gradio-container {
            max-width: 1200px !important;
            margin: 0 auto !important;
        }
        .main-header {
            text-align: center;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
        }
        .dosha-badge {
            display: inline-block;
            padding: 8px 16px;
            border-radius: 20px;
            font-weight: 600;
            font-size: 1.1em;
            margin: 10px 0;
        }
        .dosha-vata {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        .dosha-pitta {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            color: white;
        }
        .dosha-kapha {
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
            color: white;
        }
        """
        
        # Define the interface function
        def analyze_symptoms(symptoms: str, use_rag: bool, temperature: float) -> Tuple[str, str]:
            """
            Analyze symptoms and return formatted results.
            
            Args:
                symptoms: User input symptoms
                use_rag: Whether to use RAG system
                temperature: Model temperature for creativity
                
            Returns:
                Tuple of (status_message, html_output)
            """
            try:
                if not symptoms.strip():
                    return "❌ Please enter symptoms for analysis.", ""
                
                # Call the diagnostic function
                result = self.diagnostic_callback(symptoms, use_rag, temperature)
                
                if "error" in result:
                    error_html = f"""
                    <div style="background: #f8d7da; border: 1px solid #f5c6cb; border-radius: 8px; padding: 15px; margin: 10px 0; color: #721c24;">
                        <strong>⚠️ Error:</strong> {result["error"]}
                    </div>
                    """
                    return f"❌ Analysis failed: {result['error']}", error_html
                
                # Generate HTML output
                html_output = self.display.display_diagnosis(result)
                
                # Extract status message
                dominant_dosha = result.get("dominant_dosha", "Unknown")
                status_msg = f"✅ Analysis complete - {dominant_dosha} predominance detected"
                
                return status_msg, html_output.data
                
            except Exception as e:
                logger.error(f"Error in diagnostic analysis: {e}")
                error_html = f"""
                <div style="background: #f8d7da; border: 1px solid #f5c6cb; border-radius: 8px; padding: 15px; margin: 10px 0; color: #721c24;">
                    <strong>⚠️ Error:</strong> {str(e)}
                </div>
                """
                return f"❌ Analysis failed: {str(e)}", error_html
        
        # Create the interface
        with gr.Blocks(css=css, title="🩺 Ayurvedic Diagnostic Assistant") as interface:
            
            # Header
            gr.HTML("""
            <div class="main-header">
                <h1>🩺 Ayurvedic Diagnostic Assistant</h1>
                <p>Enter your symptoms below for an Ayurvedic analysis</p>
            </div>
            """)
            
            with gr.Row():
                with gr.Column(scale=2):
                    # Input section
                    gr.Markdown("### 📝 Enter Your Symptoms")
                    symptoms_input = gr.Textbox(
                        label="Symptoms",
                        placeholder="Describe your symptoms here...\nExample: I have joint pain, dry skin, and anxiety.",
                        lines=5,
                        max_lines=10
                    )
                    
                    with gr.Row():
                        use_rag_checkbox = gr.Checkbox(
                            label="Use RAG (Knowledge Base)",
                            value=True,
                            info="Enable retrieval-augmented generation for more accurate results"
                        )
                        
                        temperature_slider = gr.Slider(
                            label="Temperature",
                            minimum=0.0,
                            maximum=1.0,
                            value=0.2,
                            step=0.1,
                            info="Controls response creativity (0.0 = focused, 1.0 = creative)"
                        )
                    
                    analyze_button = gr.Button(
                        "🩺 Analyze Symptoms",
                        variant="primary",
                        size="lg"
                    )
                    
                    clear_button = gr.Button(
                        "🗑️ Clear",
                        variant="secondary",
                        size="lg"
                    )
                
                with gr.Column(scale=1):
                    # Example symptoms
                    gr.Markdown("### 🧪 Example Symptoms")
                    
                    example_vata = gr.Button(
                        "Vata Imbalance Example",
                        size="sm",
                        variant="outline"
                    )
                    
                    example_pitta = gr.Button(
                        "Pitta Imbalance Example",
                        size="sm",
                        variant="outline"
                    )
                    
                    example_kapha = gr.Button(
                        "Kapha Imbalance Example",
                        size="sm",
                        variant="outline"
                    )
            
            # Status and output
            status_output = gr.Textbox(
                label="Status",
                value="Ready for analysis",
                interactive=False
            )
            
            html_output = gr.HTML(
                label="Diagnosis Results",
                value=""
            )
            
            # Example symptoms
            vata_example = "I have joint pain that worsens in cold weather, cracking sounds in my knees, constipation, and anxiety. I have trouble sleeping and my skin is very dry."
            pitta_example = "I frequently get heartburn and acid reflux, especially after eating spicy foods. I have a reddish complexion, feel hot often, and get irritated easily."
            kapha_example = "I feel very tired and sluggish, have gained weight, and feel congested. I sleep too much and have slow digestion."
            
            # Event handlers
            analyze_button.click(
                fn=analyze_symptoms,
                inputs=[symptoms_input, use_rag_checkbox, temperature_slider],
                outputs=[status_output, html_output]
            )
            
            clear_button.click(
                fn=lambda: ("", "Ready for analysis", ""),
                outputs=[symptoms_input, status_output, html_output]
            )
            
            example_vata.click(
                fn=lambda: vata_example,
                outputs=[symptoms_input]
            )
            
            example_pitta.click(
                fn=lambda: pitta_example,
                outputs=[symptoms_input]
            )
            
            example_kapha.click(
                fn=lambda: kapha_example,
                outputs=[symptoms_input]
            )
            
            # Footer
            gr.HTML("""
            <div style="text-align: center; margin-top: 30px; padding: 20px; background: #f8f9fa; border-radius: 10px;">
                <p><strong>⚠️ Important Disclaimer:</strong></p>
                <p>This tool is for educational and informational purposes only. It should not replace professional medical advice. Always consult with qualified Ayurvedic practitioners for proper diagnosis and treatment.</p>
            </div>
            """)
        
        self.interface = interface
        return interface
    
    def launch(self, **kwargs):
        """Launch the Gradio interface."""
        if self.interface is None:
            self.create_interface()
        
        return self.interface.launch(**kwargs)


class GradioBatchUI:
    """Gradio UI for batch analysis."""
    
    def __init__(self, diagnostic_callback: Callable[[list], list]):
        """
        Initialize the Gradio batch UI.
        
        Args:
            diagnostic_callback: Function that takes list of symptoms and returns list of diagnoses
        """
        self.diagnostic_callback = diagnostic_callback
        self.display = DiagnosisDisplay()
        self.interface = None
    
    def create_interface(self) -> gr.Interface:
        """Create the Gradio batch interface."""
        
        def process_batch(symptoms_list: str) -> Tuple[str, str]:
            """
            Process batch of symptoms.
            
            Args:
                symptoms_list: Newline-separated list of symptoms
                
            Returns:
                Tuple of (status_message, html_output)
            """
            try:
                if not symptoms_list.strip():
                    return "❌ Please enter symptoms for batch analysis.", ""
                
                # Parse symptoms list
                symptoms = [s.strip() for s in symptoms_list.split('\n') if s.strip()]
                
                if not symptoms:
                    return "❌ No valid symptoms found.", ""
                
                # Process batch
                results = self.diagnostic_callback(symptoms)
                
                # Generate HTML output
                html_parts = []
                for i, result in enumerate(results, 1):
                    html_parts.append(f"<h3>Result {i}</h3>")
                    
                    if "error" in result:
                        html_parts.append(f'<div style="color: red;">❌ Error: {result["error"]}</div>')
                    else:
                        simple_output = self.display.display_simple(result)
                        html_parts.append(simple_output.data)
                    
                    html_parts.append("<hr>")
                
                html_output = "".join(html_parts)
                status_msg = f"✅ Processed {len(symptoms)} symptom sets"
                
                return status_msg, html_output
                
            except Exception as e:
                logger.error(f"Error in batch analysis: {e}")
                error_html = f"""
                <div style="background: #f8d7da; border: 1px solid #f5c6cb; border-radius: 8px; padding: 15px; margin: 10px 0; color: #721c24;">
                    <strong>⚠️ Error:</strong> {str(e)}
                </div>
                """
                return f"❌ Batch processing failed: {str(e)}", error_html
        
        # Create the interface
        with gr.Blocks(title="📊 Batch Analysis - Ayurvedic Diagnostic Assistant") as interface:
            
            gr.HTML("""
            <div style="text-align: center; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 10px; margin-bottom: 20px;">
                <h1>📊 Batch Analysis</h1>
                <p>Process multiple symptom sets at once</p>
            </div>
            """)
            
            with gr.Row():
                with gr.Column(scale=1):
                    gr.Markdown("### 📝 Enter Multiple Symptom Sets")
                    batch_input = gr.Textbox(
                        label="Symptoms (one per line)",
                        placeholder="Enter multiple symptom sets, one per line:\n\nSymptom set 1: I have joint pain and anxiety\nSymptom set 2: I have heartburn and skin rashes\n...",
                        lines=10,
                        max_lines=20
                    )
                    
                    process_button = gr.Button(
                        "📊 Process Batch",
                        variant="primary",
                        size="lg"
                    )
                    
                    clear_button = gr.Button(
                        "🗑️ Clear",
                        variant="secondary",
                        size="lg"
                    )
                
                with gr.Column(scale=1):
                    gr.Markdown("### 📋 Example Batch Input")
                    example_batch = gr.Textbox(
                        label="Example",
                        value="I have joint pain, dry skin, and anxiety.\nI frequently get heartburn and acid reflux.\nI feel very tired and sluggish, have gained weight.",
                        lines=10,
                        interactive=False
                    )
            
            # Status and output
            batch_status = gr.Textbox(
                label="Status",
                value="Ready for batch analysis",
                interactive=False
            )
            
            batch_output = gr.HTML(
                label="Batch Results",
                value=""
            )
            
            # Event handlers
            process_button.click(
                fn=process_batch,
                inputs=[batch_input],
                outputs=[batch_status, batch_output]
            )
            
            clear_button.click(
                fn=lambda: ("", "Ready for batch analysis", ""),
                outputs=[batch_input, batch_status, batch_output]
            )
            
            # Footer
            gr.HTML("""
            <div style="text-align: center; margin-top: 30px; padding: 20px; background: #f8f9fa; border-radius: 10px;">
                <p><strong>⚠️ Important Disclaimer:</strong></p>
                <p>This tool is for educational and informational purposes only. It should not replace professional medical advice. Always consult with qualified Ayurvedic practitioners for proper diagnosis and treatment.</p>
            </div>
            """)
        
        self.interface = interface
        return interface
    
    def launch(self, **kwargs):
        """Launch the Gradio batch interface."""
        if self.interface is None:
            self.create_interface()
        
        return self.interface.launch(**kwargs) 