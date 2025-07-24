# 🩺 Ayurvedic Diagnostic Assistant - Display Guide

This guide explains how to see the output in display as assistant QA using the Ayurvedic Diagnostic Assistant.

## 📋 Table of Contents

1. [Overview](#overview)
2. [Interactive Widget Display](#interactive-widget-display)
3. [Direct Display Usage](#direct-display-usage)
4. [Jupyter Notebook Interface](#jupyter-notebook-interface)
5. [Display Features](#display-features)
6. [Examples](#examples)
7. [Troubleshooting](#troubleshooting)

## 🎯 Overview

The Ayurvedic Diagnostic Assistant provides multiple ways to display results as assistant QA:

- **Interactive Widgets**: Beautiful UI with real-time analysis
- **HTML Display**: Rich formatted output with colors and icons
- **Jupyter Notebook**: Full interactive experience
- **Console Output**: Simple text-based results

## 🎨 Interactive Widget Display

### Method 1: Jupyter Notebook (Recommended)

1. **Start Jupyter Notebook**:
   ```bash
   jupyter notebook notebooks/main_assistant.ipynb
   ```

2. **Run the notebook cells** to see the interactive interface

3. **Use the Interactive Widget**:
   - Enter symptoms in the text area
   - Adjust RAG and temperature settings
   - Click "🩺 Analyze Symptoms"
   - View beautiful formatted results

### Method 2: Direct Python Usage

```python
from src.ui.widgets import InteractiveDiagnosticWidget
from src.ai.diagnostic_engine import AyurvedicDiagnosticEngine

# Initialize engine
engine = AyurvedicDiagnosticEngine()

# Create callback function
def diagnostic_callback(symptoms: str, use_rag: bool = True, temperature: float = 0.2):
    engine.use_rag = use_rag
    engine.temperature = temperature
    return engine.analyze_symptoms(symptoms)

# Create and display widget
widget = InteractiveDiagnosticWidget(diagnostic_callback)
widget.display()
```

## 📊 Direct Display Usage

### Using DiagnosisDisplay Class

```python
from src.ui.display import DiagnosisDisplay
from src.ai.diagnostic_engine import AyurvedicDiagnosticEngine

# Initialize
engine = AyurvedicDiagnosticEngine()
display_util = DiagnosisDisplay()

# Analyze symptoms
symptoms = "I have joint pain, dry skin, and anxiety"
result = engine.analyze_symptoms(symptoms)

# Display results
if "error" not in result:
    # Full diagnosis display
    html_output = display_util.display_diagnosis(result)
    
    # Simple summary display
    simple_output = display_util.display_simple(result)
    
    # In Jupyter notebook, these will show beautiful formatted output
    display(html_output)
    display(simple_output)
```

## 📓 Jupyter Notebook Interface

### Complete Example

```python
# Import required libraries
import sys
sys.path.append('src')

from src.utils.helpers import setup_logging, validate_environment
from src.ai.diagnostic_engine import AyurvedicDiagnosticEngine
from src.ui.widgets import InteractiveDiagnosticWidget
from src.ui.display import DiagnosisDisplay

# Setup
setup_logging('INFO')
engine = AyurvedicDiagnosticEngine()
display_util = DiagnosisDisplay()

# Define callback for interactive widget
def diagnostic_callback(symptoms: str, use_rag: bool = True, temperature: float = 0.2):
    engine.use_rag = use_rag
    engine.temperature = temperature
    return engine.analyze_symptoms(symptoms)

# Create interactive widget
interactive_widget = InteractiveDiagnosticWidget(diagnostic_callback)
interactive_widget.display()
```

## 🎨 Display Features

### 1. Beautiful HTML Output
- **Color-coded dosha badges**: Vata (purple), Pitta (pink), Kapha (blue)
- **Gradient backgrounds**: Modern design with smooth transitions
- **Icons and emojis**: Visual indicators for different sections
- **Responsive layout**: Works on different screen sizes

### 2. Organized Sections
- **Diagnosis Header**: Main dosha identification
- **Supporting Evidence**: Symptoms matching dosha
- **Treatment Recommendations**: Organized by category
- **Lifestyle Advice**: Daily routine suggestions
- **Medical Disclaimer**: Important safety information

### 3. Interactive Elements
- **Real-time analysis**: Instant results as you type
- **Parameter adjustment**: Control RAG and temperature
- **Progress indicators**: Visual feedback during analysis
- **Error handling**: Clear error messages

## 📝 Examples

### Example 1: Vata Imbalance
```python
symptoms = "I have joint pain that worsens in cold weather, cracking sounds in my knees, constipation, and anxiety. I have trouble sleeping and my skin is very dry."

result = engine.analyze_symptoms(symptoms)
display(display_util.display_diagnosis(result))
```

**Expected Output**:
- Dominant Dosha: Vata
- Color-coded purple badge
- Treatment recommendations for Vata imbalance
- Supporting evidence from symptoms

### Example 2: Pitta Imbalance
```python
symptoms = "I frequently get heartburn and acid reflux, especially after eating spicy foods. I have a reddish complexion, feel hot often, and get irritated easily."

result = engine.analyze_symptoms(symptoms)
display(display_util.display_diagnosis(result))
```

**Expected Output**:
- Dominant Dosha: Pitta
- Color-coded pink badge
- Cooling treatments and diet recommendations
- Heat-related symptom evidence

### Example 3: Kapha Imbalance
```python
symptoms = "I feel very tired and sluggish, have gained weight, and feel congested. I sleep too much and have slow digestion."

result = engine.analyze_symptoms(symptoms)
display(display_util.display_simple(result))
```

**Expected Output**:
- Dominant Dosha: Kapha
- Simple summary format
- Energizing treatments
- Weight management advice

## 🚀 Quick Start Guide

### Step 1: Environment Setup
```bash
# Ensure you have the required dependencies
pip install -r requirements.txt

# Set up your Google API key
cp env.example .env
# Edit .env and add your GOOGLE_API_KEY
```

### Step 2: Run Interactive Demo
```bash
# Run the interactive demo
python interactive_demo.py

# Or run the display demo
python demo_display.py
```

### Step 3: Use Jupyter Notebook
```bash
# Start Jupyter notebook
jupyter notebook notebooks/main_assistant.ipynb
```

### Step 4: Try the Widgets
1. Enter symptoms in the text area
2. Adjust analysis parameters
3. Click "Analyze Symptoms"
4. View beautiful formatted results

## 🔧 Troubleshooting

### Common Issues

1. **"Engine not initialized"**
   - Check your Google API key in `.env` file
   - Ensure internet connection is available

2. **"Environment validation failed"**
   - Install missing dependencies: `pip install -r requirements.txt`
   - Check Python version (3.8+ required)

3. **"No display output"**
   - In Jupyter: Use `display()` function
   - In console: Results are text-based
   - Check if HTML output is generated

4. **"Widget not showing"**
   - Ensure you're in Jupyter notebook environment
   - Install ipywidgets: `pip install ipywidgets`
   - Enable Jupyter extensions: `jupyter nbextension enable --py widgetsnbextension`

### Debug Mode

```python
# Enable debug logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Test individual components
from src.ui.display import DiagnosisDisplay
display_util = DiagnosisDisplay()

# Test with sample data
test_result = {
    "dominant_dosha": "Vata",
    "diagnosis": "Vata imbalance detected",
    "recommended_treatments": {
        "diet": ["Warm foods", "Oily foods"],
        "lifestyle": ["Regular routine", "Warm oil massage"]
    }
}

html_output = display_util.display_diagnosis(test_result)
print("HTML output generated successfully")
```

## 📚 Additional Resources

- **Full Documentation**: See `README.md` for complete setup
- **Example Usage**: Check `example_usage.py` for basic examples
- **RAG System**: Use `query_rag.py` for knowledge base queries
- **Configuration**: Modify `src/config/settings.py` for customization

## ⚠️ Important Notes

1. **Medical Disclaimer**: This tool is for educational purposes only
2. **API Limits**: Be mindful of Google API usage limits
3. **Professional Consultation**: Always consult qualified Ayurvedic practitioners
4. **Internet Required**: API calls require internet connection

## 🎉 Success Indicators

When working correctly, you should see:

✅ **Interactive Widget**: Text area, buttons, and output area  
✅ **Beautiful HTML**: Color-coded sections with gradients  
✅ **Dosha Badges**: Purple (Vata), Pink (Pitta), Blue (Kapha)  
✅ **Treatment Sections**: Organized recommendations  
✅ **Evidence Display**: Supporting symptoms and indicators  
✅ **Medical Disclaimer**: Important safety information  

---

**Happy Diagnosing! 🌿**

For more help, check the main README.md or run the interactive demos. 