"""
Interactive widgets for the Ayurvedic Diagnostic Assistant.
"""

import logging
from typing import Dict, Any, Callable, Optional
import ipywidgets as widgets
from IPython.display import display, HTML
from src.ui.display import DiagnosisDisplay

logger = logging.getLogger(__name__)


class InteractiveDiagnosticWidget:
    """Interactive widget for Ayurvedic diagnosis."""
    
    def __init__(self, diagnostic_callback: Callable[[str], Dict[str, Any]]):
        """
        Initialize the interactive widget.
        
        Args:
            diagnostic_callback: Function that takes symptoms and returns diagnosis
        """
        self.diagnostic_callback = diagnostic_callback
        self.display = DiagnosisDisplay()
        self._create_widgets()
        self._setup_layout()
    
    def _create_widgets(self):
        """Create the interactive widgets."""
        # Symptoms input
        self.symptoms_input = widgets.Textarea(
            value='',
            placeholder='Describe your symptoms here...\nExample: I have joint pain, dry skin, and anxiety.',
            description='Symptoms:',
            layout=widgets.Layout(width='100%', height='120px')
        )
        
        # Analysis options
        self.use_rag_checkbox = widgets.Checkbox(
            value=True,
            description='Use RAG (Knowledge Base)',
            layout=widgets.Layout(width='auto')
        )
        
        self.temperature_slider = widgets.FloatSlider(
            value=0.2,
            min=0.0,
            max=1.0,
            step=0.1,
            description='Temperature:',
            layout=widgets.Layout(width='300px')
        )
        
        # Buttons
        self.analyze_button = widgets.Button(
            description='🩺 Analyze Symptoms',
            button_style='primary',
            layout=widgets.Layout(width='auto', height='40px')
        )
        
        self.clear_button = widgets.Button(
            description='🗑️ Clear',
            button_style='warning',
            layout=widgets.Layout(width='auto', height='40px')
        )
        
        # Progress indicator
        self.progress = widgets.HTML(
            value='',
            layout=widgets.Layout(width='100%')
        )
        
        # Output area
        self.output_area = widgets.Output(
            layout=widgets.Layout(width='100%', height='600px', overflow='auto')
        )
        
        # Status indicator
        self.status_indicator = widgets.HTML(
            value='<div style="color: #6c757d;">Ready for analysis</div>',
            layout=widgets.Layout(width='100%')
        )
        
        # Connect button events
        self.analyze_button.on_click(self._on_analyze_click)
        self.clear_button.on_click(self._on_clear_click)
    
    def _setup_layout(self):
        """Setup the widget layout."""
        # Options row
        options_row = widgets.HBox([
            self.use_rag_checkbox,
            self.temperature_slider
        ], layout=widgets.Layout(justify_content='space-between'))
        
        # Buttons row
        buttons_row = widgets.HBox([
            self.analyze_button,
            self.clear_button
        ], layout=widgets.Layout(justify_content='flex-start', gap='10px'))
        
        # Main layout
        self.main_widget = widgets.VBox([
            widgets.HTML('<h2>🩺 Ayurvedic Diagnostic Assistant</h2>'),
            widgets.HTML('<p>Enter your symptoms below for an Ayurvedic analysis:</p>'),
            self.symptoms_input,
            options_row,
            buttons_row,
            self.progress,
            self.status_indicator,
            self.output_area
        ], layout=widgets.Layout(width='100%', gap='15px'))
    
    def _on_analyze_click(self, button):
        """Handle analyze button click."""
        symptoms = self.symptoms_input.value.strip()
        
        if not symptoms:
            self._show_error("Please enter symptoms for analysis.")
            return
        
        # Update UI state
        self.analyze_button.disabled = True
        self.analyze_button.description = '⏳ Analyzing...'
        self.progress.value = '<div style="color: #007bff;">🔄 Analyzing symptoms...</div>'
        self.status_indicator.value = '<div style="color: #007bff;">Processing...</div>'
        
        try:
            # Call diagnostic function
            diagnosis = self.diagnostic_callback(
                symptoms,
                use_rag=self.use_rag_checkbox.value,
                temperature=self.temperature_slider.value
            )
            
            # Display results
            self._display_results(diagnosis)
            
        except Exception as e:
            logger.error(f"Error in diagnostic analysis: {e}")
            self._show_error(f"Analysis failed: {str(e)}")
        
        finally:
            # Reset UI state
            self.analyze_button.disabled = False
            self.analyze_button.description = '🩺 Analyze Symptoms'
            self.progress.value = ''
    
    def _on_clear_click(self, button):
        """Handle clear button click."""
        self.symptoms_input.value = ''
        self.output_area.clear_output()
        self.status_indicator.value = '<div style="color: #6c757d;">Ready for analysis</div>'
        self.progress.value = ''
    
    def _display_results(self, diagnosis: Dict[str, Any]):
        """Display diagnostic results."""
        with self.output_area:
            self.output_area.clear_output()
            
            if "error" in diagnosis:
                self._show_error(diagnosis["error"])
                return
            
            # Display the diagnosis
            display(self.display.display_diagnosis(diagnosis))
            
            # Update status
            dominant_dosha = diagnosis.get("dominant_dosha", "Unknown")
            self.status_indicator.value = f'<div style="color: #28a745;">✅ Analysis complete - {dominant_dosha} predominance detected</div>'
    
    def _show_error(self, message: str):
        """Show error message."""
        error_html = f"""
        <div style="background: #f8d7da; border: 1px solid #f5c6cb; border-radius: 8px; padding: 15px; margin: 10px 0; color: #721c24;">
            <strong>⚠️ Error:</strong> {message}
        </div>
        """
        
        with self.output_area:
            self.output_area.clear_output()
            display(HTML(error_html))
        
        self.status_indicator.value = f'<div style="color: #dc3545;">❌ Error occurred</div>'
    
    def display(self):
        """Display the interactive widget."""
        display(self.main_widget)
    
    def get_widget(self):
        """Get the main widget."""
        return self.main_widget


class BatchAnalysisWidget:
    """Widget for batch analysis of multiple symptom sets."""
    
    def __init__(self, diagnostic_callback: Callable[[list], list]):
        """
        Initialize batch analysis widget.
        
        Args:
            diagnostic_callback: Function that takes list of symptoms and returns list of diagnoses
        """
        self.diagnostic_callback = diagnostic_callback
        self.display = DiagnosisDisplay()
        self._create_widgets()
        self._setup_layout()
    
    def _create_widgets(self):
        """Create batch analysis widgets."""
        # File upload for batch processing
        self.file_upload = widgets.FileUpload(
            accept='.txt,.csv',
            multiple=False,
            description='Upload symptoms file:',
            layout=widgets.Layout(width='100%')
        )
        
        # Batch input
        self.batch_input = widgets.Textarea(
            value='',
            placeholder='Enter multiple symptom sets, one per line:\n\nSymptom set 1: I have joint pain and anxiety\nSymptom set 2: I have heartburn and skin rashes\n...',
            description='Batch symptoms:',
            layout=widgets.Layout(width='100%', height='200px')
        )
        
        # Process button
        self.process_button = widgets.Button(
            description='📊 Process Batch',
            button_style='info',
            layout=widgets.Layout(width='auto', height='40px')
        )
        
        # Progress
        self.batch_progress = widgets.HTML(
            value='',
            layout=widgets.Layout(width='100%')
        )
        
        # Results area
        self.batch_output = widgets.Output(
            layout=widgets.Layout(width='100%', height='800px', overflow='auto')
        )
        
        # Connect events
        self.process_button.on_click(self._on_process_click)
    
    def _setup_layout(self):
        """Setup batch analysis layout."""
        self.main_widget = widgets.VBox([
            widgets.HTML('<h3>📊 Batch Analysis</h3>'),
            widgets.HTML('<p>Process multiple symptom sets at once:</p>'),
            self.file_upload,
            widgets.HTML('<p>Or enter symptoms manually:</p>'),
            self.batch_input,
            self.process_button,
            self.batch_progress,
            self.batch_output
        ], layout=widgets.Layout(width='100%', gap='15px'))
    
    def _on_process_click(self, button):
        """Handle batch process click."""
        symptoms_list = self._get_symptoms_list()
        
        if not symptoms_list:
            self._show_batch_error("Please provide symptoms for batch analysis.")
            return
        
        # Update UI
        self.process_button.disabled = True
        self.process_button.description = '⏳ Processing...'
        self.batch_progress.value = f'<div style="color: #007bff;">🔄 Processing {len(symptoms_list)} symptom sets...</div>'
        
        try:
            # Process batch
            results = self.diagnostic_callback(symptoms_list)
            
            # Display results
            self._display_batch_results(results)
            
        except Exception as e:
            logger.error(f"Error in batch analysis: {e}")
            self._show_batch_error(f"Batch processing failed: {str(e)}")
        
        finally:
            # Reset UI
            self.process_button.disabled = False
            self.process_button.description = '📊 Process Batch'
            self.batch_progress.value = ''
    
    def _get_symptoms_list(self) -> list:
        """Get list of symptoms from input."""
        symptoms_list = []
        
        # Check file upload first
        if self.file_upload.value:
            # Handle file upload (simplified)
            pass
        
        # Check manual input
        manual_input = self.batch_input.value.strip()
        if manual_input:
            lines = manual_input.split('\n')
            for line in lines:
                line = line.strip()
                if line and not line.startswith('#'):
                    symptoms_list.append(line)
        
        return symptoms_list
    
    def _display_batch_results(self, results: list):
        """Display batch analysis results."""
        with self.batch_output:
            self.batch_output.clear_output()
            
            for i, result in enumerate(results, 1):
                display(HTML(f'<h4>Result {i}</h4>'))
                
                if "error" in result:
                    display(HTML(f'<div style="color: red;">Error: {result["error"]}</div>'))
                else:
                    display(self.display.display_simple(result))
                
                display(HTML('<hr>'))
    
    def _show_batch_error(self, message: str):
        """Show batch error message."""
        with self.batch_output:
            self.batch_output.clear_output()
            display(HTML(f'<div style="color: red;">❌ {message}</div>'))
    
    def display(self):
        """Display the batch analysis widget."""
        display(self.main_widget)
    
    def get_widget(self):
        """Get the main widget."""
        return self.main_widget 