"""
Display utilities for Ayurvedic diagnostic results.
"""

import logging
from datetime import datetime
from typing import Dict, Any, Optional
from IPython.display import HTML, display

logger = logging.getLogger(__name__)


class DiagnosisDisplay:
    """Display utilities for Ayurvedic diagnostic results."""
    
    def __init__(self):
        self.css_styles = self._get_css_styles()
    
    def _get_css_styles(self) -> str:
        """Get CSS styles for the display."""
        return """
        <style>
        .ayurvedic-diagnosis {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            max-width: 1200px;
            margin: 20px auto;
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            overflow: hidden;
        }
        
        .diagnosis-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 25px;
            text-align: center;
        }
        
        .diagnosis-header h1 {
            margin: 0;
            font-size: 2.5em;
            font-weight: 300;
        }
        
        .diagnosis-header .subtitle {
            font-size: 1.1em;
            opacity: 0.9;
            margin-top: 10px;
        }
        
        .diagnosis-content {
            padding: 30px;
        }
        
        .diagnosis-section {
            background: white;
            margin: 20px 0;
            border-radius: 10px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.08);
            overflow: hidden;
        }
        
        .section-header {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            color: white;
            padding: 15px 25px;
            font-size: 1.3em;
            font-weight: 600;
            display: flex;
            align-items: center;
        }
        
        .section-header .icon {
            margin-right: 10px;
            font-size: 1.2em;
        }
        
        .section-content {
            padding: 25px;
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
        
        .treatment-category {
            background: #f8f9fa;
            border-left: 4px solid #007bff;
            padding: 15px;
            margin: 10px 0;
            border-radius: 5px;
        }
        
        .treatment-category h4 {
            margin: 0 0 10px 0;
            color: #495057;
            font-size: 1.1em;
        }
        
        .treatment-list {
            list-style: none;
            padding: 0;
            margin: 0;
        }
        
        .treatment-list li {
            padding: 8px 0;
            border-bottom: 1px solid #e9ecef;
            color: #6c757d;
        }
        
        .treatment-list li:last-child {
            border-bottom: none;
        }
        
        .evidence-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin: 15px 0;
        }
        
        .evidence-item {
            background: #f8f9fa;
            padding: 15px;
            border-radius: 8px;
            border-left: 4px solid #28a745;
        }
        
        .evidence-item h5 {
            margin: 0 0 10px 0;
            color: #495057;
            font-size: 1em;
        }
        
        .evidence-item ul {
            margin: 0;
            padding-left: 20px;
            color: #6c757d;
        }
        
        .disclaimer {
            background: #fff3cd;
            border: 1px solid #ffeaa7;
            border-radius: 8px;
            padding: 15px;
            margin: 20px 0;
            color: #856404;
            font-size: 0.9em;
        }
        
        .metadata {
            background: #e9ecef;
            padding: 15px;
            border-radius: 8px;
            margin: 20px 0;
            font-size: 0.85em;
            color: #6c757d;
        }
        
        .error-message {
            background: #f8d7da;
            border: 1px solid #f5c6cb;
            border-radius: 8px;
            padding: 20px;
            margin: 20px 0;
            color: #721c24;
        }
        </style>
        """
    
    def display_diagnosis(self, diagnosis: Dict[str, Any]) -> HTML:
        """
        Display a complete Ayurvedic diagnosis.
        
        Args:
            diagnosis: Diagnosis dictionary
            
        Returns:
            HTML display object
        """
        try:
            if "error" in diagnosis:
                return self._display_error(diagnosis)
            
            html_content = self._generate_diagnosis_html(diagnosis)
            return HTML(html_content)
            
        except Exception as e:
            logger.error(f"Error displaying diagnosis: {e}")
            return HTML(f"<div class='error-message'>Error displaying diagnosis: {str(e)}</div>")
    
    def _display_error(self, diagnosis: Dict[str, Any]) -> HTML:
        """Display error message."""
        error_html = f"""
        <div class='ayurvedic-diagnosis'>
            <div class='diagnosis-header'>
                <h1>⚠️ Diagnostic Error</h1>
            </div>
            <div class='diagnosis-content'>
                <div class='error-message'>
                    <h3>Error occurred during diagnosis:</h3>
                    <p>{diagnosis.get('error', 'Unknown error')}</p>
                    {f"<p><strong>Raw content:</strong> {diagnosis.get('raw_content', '')}</p>" if 'raw_content' in diagnosis else ''}
                </div>
            </div>
        </div>
        """
        return HTML(self.css_styles + error_html)
    
    def _generate_diagnosis_html(self, diagnosis: Dict[str, Any]) -> str:
        """Generate HTML for diagnosis display."""
        
        # Get dosha-specific styling
        dominant_dosha = diagnosis.get("dominant_dosha", "Unknown")
        dosha_class = f"dosha-{dominant_dosha.lower()}"
        
        html = f"""
        <div class='ayurvedic-diagnosis'>
            <div class='diagnosis-header'>
                <h1>🩺 Ayurvedic Diagnostic Report</h1>
                <div class='subtitle'>Comprehensive Analysis & Treatment Recommendations</div>
            </div>
            
            <div class='diagnosis-content'>
                
                <!-- Dominant Dosha Section -->
                <div class='diagnosis-section'>
                    <div class='section-header'>
                        <span class='icon'>⚖️</span>
                        Dominant Dosha Analysis
                    </div>
                    <div class='section-content'>
                        <div class='{dosha_class} dosha-badge'>
                            {dominant_dosha} Predominance
                        </div>
                        <p><strong>Primary Diagnosis:</strong> {diagnosis.get('diagnosis', 'Not specified')}</p>
                    </div>
                </div>
                
                <!-- Imbalances Section -->
                <div class='diagnosis-section'>
                    <div class='section-header'>
                        <span class='icon'>🔍</span>
                        Identified Imbalances
                    </div>
                    <div class='section-content'>
                        <ul class='treatment-list'>
                            {self._format_list_items(diagnosis.get('imbalances', []))}
                        </ul>
                    </div>
                </div>
                
                <!-- Supporting Evidence Section -->
                <div class='diagnosis-section'>
                    <div class='section-header'>
                        <span class='icon'>📋</span>
                        Supporting Evidence
                    </div>
                    <div class='section-content'>
                        {self._format_supporting_evidence(diagnosis.get('supporting_evidence', {}))}
                    </div>
                </div>
                
                <!-- Treatment Recommendations Section -->
                <div class='diagnosis-section'>
                    <div class='section-header'>
                        <span class='icon'>🌱</span>
                        Treatment Recommendations
                    </div>
                    <div class='section-content'>
                        {self._format_treatments(diagnosis.get('recommended_treatments', {}))}
                    </div>
                </div>
                
                <!-- Disclaimer -->
                <div class='disclaimer'>
                    <strong>⚠️ Important Disclaimer:</strong> This analysis is for educational and informational purposes only. 
                    It should not replace professional medical advice. Always consult with qualified Ayurvedic practitioners 
                    for proper diagnosis and treatment. Individual results may vary.
                </div>
                
                <!-- Metadata -->
                {self._format_metadata(diagnosis.get('metadata', {}))}
                
            </div>
        </div>
        """
        
        return self.css_styles + html
    
    def _format_list_items(self, items: list) -> str:
        """Format a list of items as HTML."""
        if not items:
            return "<li>No items specified</li>"
        
        html_items = []
        for item in items:
            html_items.append(f"<li>{item}</li>")
        
        return "".join(html_items)
    
    def _format_supporting_evidence(self, evidence: Dict[str, Any]) -> str:
        """Format supporting evidence section."""
        if not evidence:
            return "<p>No supporting evidence provided.</p>"
        
        html_parts = []
        
        if "symptoms_matching_dosha" in evidence:
            html_parts.append(f"""
            <div class='evidence-item'>
                <h5>🎯 Symptoms Matching Dosha</h5>
                <ul class='treatment-list'>
                    {self._format_list_items(evidence['symptoms_matching_dosha'])}
                </ul>
            </div>
            """)
        
        if "pulse_indication" in evidence:
            html_parts.append(f"""
            <div class='evidence-item'>
                <h5>💓 Pulse Indication</h5>
                <p>{evidence['pulse_indication']}</p>
            </div>
            """)
        
        if "tongue_indication" in evidence:
            html_parts.append(f"""
            <div class='evidence-item'>
                <h5>👅 Tongue Indication</h5>
                <p>{evidence['tongue_indication']}</p>
            </div>
            """)
        
        return f"""
        <div class='evidence-grid'>
            {''.join(html_parts)}
        </div>
        """
    
    def _format_treatments(self, treatments: Dict[str, Any]) -> str:
        """Format treatment recommendations."""
        if not treatments:
            return "<p>No treatment recommendations provided.</p>"
        
        treatment_categories = {
            "dietary": {"icon": "🍴", "title": "Dietary Recommendations"},
            "herbs": {"icon": "🌿", "title": "Herbal Recommendations"},
            "ayurvedic_medicines": {"icon": "💊", "title": "Ayurvedic Medicines"},
            "therapies": {"icon": "👐", "title": "Therapeutic Recommendations"},
            "lifestyle": {"icon": "❤️", "title": "Lifestyle Recommendations"}
        }
        
        html_parts = []
        
        for category, config in treatment_categories.items():
            if category in treatments and treatments[category]:
                html_parts.append(f"""
                <div class='treatment-category'>
                    <h4>{config['icon']} {config['title']}</h4>
                    <ul class='treatment-list'>
                        {self._format_list_items(treatments[category])}
                    </ul>
                </div>
                """)
        
        return "".join(html_parts)
    
    def _format_metadata(self, metadata: Dict[str, Any]) -> str:
        """Format metadata section."""
        if not metadata:
            return ""
        
        metadata_items = []
        for key, value in metadata.items():
            if key != "symptoms":  # Don't show symptoms in metadata
                metadata_items.append(f"<strong>{key}:</strong> {value}")
        
        if metadata_items:
            return f"""
            <div class='metadata'>
                <strong>Analysis Details:</strong><br>
                {', '.join(metadata_items)}<br>
                <em>Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</em>
            </div>
            """
        
        return ""
    
    def display_simple(self, diagnosis: Dict[str, Any]) -> HTML:
        """
        Display a simplified version of the diagnosis.
        
        Args:
            diagnosis: Diagnosis dictionary
            
        Returns:
            HTML display object
        """
        try:
            if "error" in diagnosis:
                return self._display_error(diagnosis)
            
            dominant_dosha = diagnosis.get("dominant_dosha", "Unknown")
            diagnosis_text = diagnosis.get("diagnosis", "Not specified")
            
            simple_html = f"""
            <div style='background: #f8f9fa; padding: 20px; border-radius: 10px; margin: 10px 0;'>
                <h3>🩺 Quick Diagnosis Summary</h3>
                <p><strong>Dominant Dosha:</strong> {dominant_dosha}</p>
                <p><strong>Diagnosis:</strong> {diagnosis_text}</p>
                <p><em>Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</em></p>
            </div>
            """
            
            return HTML(simple_html)
            
        except Exception as e:
            logger.error(f"Error displaying simple diagnosis: {e}")
            return HTML(f"<div style='color: red;'>Error: {str(e)}</div>") 