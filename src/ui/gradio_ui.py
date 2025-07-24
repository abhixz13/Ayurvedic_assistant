"""
Gradio UI components for the Ayurvedic Diagnostic Assistant.
"""

import gradio as gr
import logging
from typing import Callable, Dict, Any, List, Tuple
from src.ui.display import DiagnosisDisplay

logger = logging.getLogger(__name__)


class GradioChatUI:
    """Conversational chat interface for the Ayurvedic Diagnostic Assistant."""
    
    def __init__(self, chat_callback: Callable[[str, bool, float], str]):
        """
        Initialize the chat UI.
        
        Args:
            chat_callback: Function to handle chat messages
        """
        self.chat_callback = chat_callback
        self.conversation_history = []
        self.interface = None
        
    def create_interface(self) -> gr.Interface:
        """Create the Gradio chat interface."""
        
        # Custom CSS for better styling
        css = """
        .chat-container {
            max-height: 600px;
            overflow-y: auto;
            border: 1px solid #ddd;
            border-radius: 10px;
            padding: 20px;
            background: #f9f9f9;
        }
        .user-message {
            background: #007bff;
            color: white;
            padding: 10px 15px;
            border-radius: 15px;
            margin: 10px 0;
            max-width: 80%;
            margin-left: auto;
            text-align: right;
        }
        .assistant-message {
            background: #e9ecef;
            color: #333;
            padding: 10px 15px;
            border-radius: 15px;
            margin: 10px 0;
            max-width: 80%;
            margin-right: auto;
        }
        .settings-panel {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            border: 1px solid #dee2e6;
        }
        .example-button {
            margin: 5px;
            padding: 8px 12px;
            border-radius: 5px;
            border: 1px solid #007bff;
            background: #007bff;
            color: white;
            cursor: pointer;
        }
        .example-button:hover {
            background: #0056b3;
        }
        """
        
        def chat_with_assistant(message: str, use_rag: bool, temperature: float) -> Tuple[str, str]:
            """
            Handle chat interaction with the assistant.
            
            Args:
                message: User's message
                use_rag: Whether to use RAG
                temperature: Model temperature
                
            Returns:
                Tuple of (chat_history, status_message)
            """
            if not message.strip():
                return "", "Please enter a message."
            
            try:
                # Add user message to history
                self.conversation_history.append({"user": message, "assistant": ""})
                
                # Get assistant response
                response = self.chat_callback(message, use_rag, temperature)
                
                # Update conversation history
                self.conversation_history[-1]["assistant"] = response
                
                # Format chat history for display
                chat_display = ""
                for turn in self.conversation_history:
                    chat_display += f'<div class="user-message">{turn["user"]}</div>'
                    chat_display += f'<div class="assistant-message">{turn["assistant"]}</div>'
                
                status = f"✅ Response generated successfully"
                return chat_display, status
                
            except Exception as e:
                logger.error(f"Error in chat: {e}")
                error_msg = f"❌ Error: {str(e)}"
                return "", error_msg
        
        def clear_chat() -> Tuple[str, str]:
            """Clear the chat history."""
            self.conversation_history = []
            return "", "🗑️ Chat history cleared"
        
        def add_example_message(example: str) -> Tuple[str, str, str]:
            """Add an example message to the chat."""
            return example, "", "📝 Example message added"
        
        # Create the interface layout
        with gr.Blocks(css=css, title="Ayurvedic Chat Assistant") as interface:
            
            gr.Markdown("""
            # 🩺 Ayurvedic Chat Assistant
            
            Welcome! I'm Dr. Priya, your Ayurvedic health assistant. I can help you with:
            - Ayurvedic principles and dosha analysis
            - Health and wellness advice
            - Symptom interpretation
            - Treatment recommendations
            - Lifestyle and dietary guidance
            
            Feel free to ask me anything about Ayurveda and health!
            """)
            
            with gr.Row():
                # Left sidebar with settings
                with gr.Column(scale=1):
                    gr.Markdown("### ⚙️ Settings")
                    
                    with gr.Group(elem_classes="settings-panel"):
                        use_rag = gr.Checkbox(
                            label="Use RAG Knowledge",
                            value=True,
                            info="Enable to use saved Ayurvedic knowledge"
                        )
                        
                        temperature = gr.Slider(
                            minimum=0.1,
                            maximum=1.0,
                            value=0.2,
                            step=0.1,
                            label="Temperature",
                            info="Higher = more creative, Lower = more focused"
                        )
                        
                        gr.Markdown("### 💡 Example Messages")
                        
                        example_buttons = gr.Row()
                        with example_buttons:
                            gr.Button("👋 Hello", size="sm").click(
                                add_example_message,
                                outputs=[gr.Textbox(label="Message", placeholder="Type your message here..."), gr.Textbox(label="Chat History"), gr.Textbox(label="Status")]
                            )
                            
                        with example_buttons:
                            gr.Button("😴 Sleep Issues", size="sm").click(
                                lambda: add_example_message("I'm having trouble sleeping and feel anxious"),
                                outputs=[gr.Textbox(label="Message", placeholder="Type your message here..."), gr.Textbox(label="Chat History"), gr.Textbox(label="Status")]
                            )
                            
                        with example_buttons:
                            gr.Button("🌿 Vata Dosha", size="sm").click(
                                lambda: add_example_message("Tell me about Vata dosha"),
                                outputs=[gr.Textbox(label="Message", placeholder="Type your message here..."), gr.Textbox(label="Chat History"), gr.Textbox(label="Status")]
                            )
                            
                        with example_buttons:
                            gr.Button("🍽️ Diet Advice", size="sm").click(
                                lambda: add_example_message("What should I eat to balance Pitta dosha?"),
                                outputs=[gr.Textbox(label="Message", placeholder="Type your message here..."), gr.Textbox(label="Chat History"), gr.Textbox(label="Status")]
                            )
                        
                        clear_btn = gr.Button("🗑️ Clear Chat", variant="secondary")
                
                # Main chat area
                with gr.Column(scale=3):
                    gr.Markdown("### 💬 Chat Window")
                    
                    # Chat display area
                    chat_display = gr.HTML(
                        value="",
                        label="Chat History",
                        elem_classes="chat-container"
                    )
                    
                    # Message input
                    message_input = gr.Textbox(
                        label="Message",
                        placeholder="Type your message here...",
                        lines=2
                    )
                    
                    # Send button
                    send_btn = gr.Button("💬 Send Message", variant="primary")
                    
                    # Status message
                    status_msg = gr.Textbox(
                        label="Status",
                        value="Ready to chat! 👋",
                        interactive=False
                    )
            
            # Event handlers
            send_btn.click(
                chat_with_assistant,
                inputs=[message_input, use_rag, temperature],
                outputs=[chat_display, status_msg]
            ).then(
                lambda: "",
                outputs=[message_input]
            )
            
            message_input.submit(
                chat_with_assistant,
                inputs=[message_input, use_rag, temperature],
                outputs=[chat_display, status_msg]
            ).then(
                lambda: "",
                outputs=[message_input]
            )
            
            clear_btn.click(
                clear_chat,
                outputs=[chat_display, status_msg]
            )
        
        self.interface = interface
        return interface
    
    def launch(self, **kwargs):
        """Launch the Gradio interface."""
        if self.interface is None:
            self.create_interface()
        
        self.interface.launch(**kwargs)


class GradioDiagnosticUI:
    """Legacy diagnostic interface (kept for backward compatibility)."""
    
    def __init__(self, diagnostic_callback: Callable[[str, bool, float], Dict[str, Any]]):
        self.diagnostic_callback = diagnostic_callback
        self.display = DiagnosisDisplay()
        self.interface = None
    
    def create_interface(self) -> gr.Interface:
        """Create the Gradio interface."""
        
        def analyze_symptoms(symptoms: str, use_rag: bool, temperature: float) -> Tuple[str, str]:
            """Analyze symptoms and return results."""
            if not symptoms.strip():
                return "", "Please enter symptoms to analyze."
            
            try:
                result = self.diagnostic_callback(symptoms, use_rag, temperature)
                
                if "error" in result:
                    return "", f"❌ Error: {result['error']}"
                
                # Generate HTML display
                html_output = self.display.display_diagnosis(result)
                
                status = f"✅ Analysis completed successfully"
                return html_output, status
                
            except Exception as e:
                logger.error(f"Error in analysis: {e}")
                return "", f"❌ Error: {str(e)}"
        
        # Create the interface
        with gr.Blocks(title="Ayurvedic Diagnostic Assistant") as interface:
            
            gr.Markdown("""
            # 🩺 Ayurvedic Diagnostic Assistant
            
            Enter your symptoms below to receive a comprehensive Ayurvedic analysis.
            """)
            
            with gr.Row():
                with gr.Column(scale=2):
                    # Input section
                    symptoms_input = gr.Textbox(
                        label="Symptoms",
                        placeholder="Describe your symptoms in detail...",
                        lines=5
                    )
                    
                    with gr.Row():
                        use_rag = gr.Checkbox(
                            label="Use RAG Knowledge",
                            value=True,
                            info="Enable to use saved Ayurvedic knowledge"
                        )
                        
                        temperature = gr.Slider(
                            minimum=0.1,
                            maximum=1.0,
                            value=0.2,
                            step=0.1,
                            label="Temperature",
                            info="Higher = more creative, Lower = more focused"
                        )
                    
                    analyze_btn = gr.Button("🔍 Analyze Symptoms", variant="primary")
                    
                    # Example buttons
                    gr.Markdown("### 💡 Example Symptoms")
                    with gr.Row():
                        gr.Button("Vata Example").click(
                            lambda: ("I have joint pain that worsens in cold weather, cracking sounds in my knees, constipation, and anxiety. I have trouble sleeping and my skin is very dry.", "", ""),
                            outputs=[symptoms_input, gr.HTML(label="Results"), gr.Textbox(label="Status")]
                        )
                        gr.Button("Pitta Example").click(
                            lambda: ("I frequently get heartburn and acid reflux, especially after eating spicy foods. I have a reddish complexion, feel hot often, and get irritated easily.", "", ""),
                            outputs=[symptoms_input, gr.HTML(label="Results"), gr.Textbox(label="Status")]
                        )
                        gr.Button("Kapha Example").click(
                            lambda: ("I feel very tired and sluggish, have gained weight, and feel congested. I sleep too much and have slow digestion.", "", ""),
                            outputs=[symptoms_input, gr.HTML(label="Results"), gr.Textbox(label="Status")]
                        )
                
                with gr.Column(scale=2):
                    # Results section
                    results_html = gr.HTML(label="Results")
                    status_msg = gr.Textbox(label="Status", value="Ready to analyze! 🔍", interactive=False)
            
            # Event handlers
            analyze_btn.click(
                analyze_symptoms,
                inputs=[symptoms_input, use_rag, temperature],
                outputs=[results_html, status_msg]
            )
            
            symptoms_input.submit(
                analyze_symptoms,
                inputs=[symptoms_input, use_rag, temperature],
                outputs=[results_html, status_msg]
            )
        
        self.interface = interface
        return interface
    
    def launch(self, **kwargs):
        """Launch the Gradio interface."""
        if self.interface is None:
            self.create_interface()
        
        self.interface.launch(**kwargs)


class GradioBatchUI:
    """Batch analysis interface."""
    
    def __init__(self, diagnostic_callback: Callable[[list], list]):
        self.diagnostic_callback = diagnostic_callback
        self.display = DiagnosisDisplay()
        self.interface = None
    
    def create_interface(self) -> gr.Interface:
        """Create the batch analysis interface."""
        
        def process_batch(symptoms_list: str) -> Tuple[str, str]:
            """Process multiple symptoms."""
            if not symptoms_list.strip():
                return "", "Please enter symptoms to analyze."
            
            try:
                # Split symptoms by lines
                symptoms = [s.strip() for s in symptoms_list.split('\n') if s.strip()]
                
                if not symptoms:
                    return "", "No valid symptoms found."
                
                # Process each symptom
                results = self.diagnostic_callback(symptoms)
                
                # Generate HTML output
                html_output = ""
                for i, result in enumerate(results, 1):
                    if "error" in result:
                        html_output += f"<h3>Symptom Set {i}</h3><p>❌ Error: {result['error']}</p><hr>"
                    else:
                        html_output += f"<h3>Symptom Set {i}</h3>"
                        html_output += self.display.display_simple(result)
                        html_output += "<hr>"
                
                status = f"✅ Processed {len(symptoms)} symptom sets"
                return html_output, status
                
            except Exception as e:
                logger.error(f"Error in batch processing: {e}")
                return "", f"❌ Error: {str(e)}"
        
        # Create the interface
        with gr.Blocks(title="Ayurvedic Batch Analysis") as interface:
            
            gr.Markdown("""
            # 📊 Ayurvedic Batch Analysis
            
            Enter multiple symptom sets (one per line) for batch analysis.
            """)
            
            with gr.Row():
                with gr.Column():
                    symptoms_input = gr.Textbox(
                        label="Symptoms (one set per line)",
                        placeholder="Enter symptoms here...\n\nEnter more symptoms here...\n\nEnter more symptoms here...",
                        lines=10
                    )
                    
                    process_btn = gr.Button("📊 Process Batch", variant="primary")
                
                with gr.Column():
                    results_html = gr.HTML(label="Results")
                    status_msg = gr.Textbox(label="Status", value="Ready for batch processing! 📊", interactive=False)
            
            # Event handlers
            process_btn.click(
                process_batch,
                inputs=[symptoms_input],
                outputs=[results_html, status_msg]
            )
        
        self.interface = interface
        return interface
    
    def launch(self, **kwargs):
        """Launch the Gradio interface."""
        if self.interface is None:
            self.create_interface()
        
        self.interface.launch(**kwargs) 