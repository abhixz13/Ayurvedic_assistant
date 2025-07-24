# 🩺 Ayurvedic Diagnostic Assistant

An AI-powered Ayurvedic diagnostic assistant with a modern Gradio web interface and RAG (Retrieval-Augmented Generation) system.

## 🌟 Features

- **Modern Gradio Web Interface**: Beautiful, responsive web UI accessible from any device
- **RAG System**: Knowledge base integration for accurate Ayurvedic recommendations
- **Beautiful HTML Display**: Color-coded dosha identification and treatment recommendations
- **Batch Analysis**: Process multiple symptom sets at once
- **Real-time Analysis**: Instant results with beautiful formatting
- **Network Accessible**: Share with others on your network
- **Mobile Friendly**: Works on phones, tablets, and desktops
- **Complete System Test**: Comprehensive testing framework for all components

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Google API key for Gemini
- Internet connection for API calls

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/abhixz13/Ayurvedic_assistant.git
   cd Ayurvedic_Diagnostic_Assistant
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment**:
   ```bash
   cp env.example .env
   # Edit .env and add your GOOGLE_API_KEY
   ```

4. **Launch the Gradio web interface**:
   ```bash
   python gradio_demo.py
   ```

## 🧪 System Testing

Run the complete system test to verify all components:

```bash
python system_test.py
```

**Test Results**: All 8 system components passed (100% success rate)
- ✅ Environment and Dependencies
- ✅ Configuration Settings
- ✅ Document Processing
- ✅ Vector Store Operations
- ✅ RAG System
- ✅ AI Components
- ✅ UI Components
- ✅ End-to-End Integration

## 🎯 Usage

### Gradio Web Interface
```bash
# Main diagnostic interface
python gradio_demo.py

# Batch analysis interface
python gradio_demo.py --batch
```

### Interactive Demo
```bash
python interactive_demo.py
```

### Display Demo
```bash
python demo_display.py
```

### Example Usage
```bash
python example_usage.py
```

### RAG Query Tool
```bash
python query_rag.py
```

## 🌐 Gradio Web Interface

The Gradio interface provides a modern web-based UI that can be accessed from any device:

### Features:
- **Web-based**: Access from any browser
- **Network accessible**: Share with others on your network
- **Mobile friendly**: Works on phones and tablets
- **Real-time analysis**: Instant results with beautiful formatting
- **Example buttons**: Quick test with sample symptoms
- **Batch processing**: Process multiple symptoms at once

### Launch Options:
```bash
# Main interface (port 7860)
python gradio_demo.py

# Batch interface (port 7861)
python gradio_demo.py --batch

# With public sharing (creates public URL)
# Modify gradio_demo.py to set share=True
```

## 📊 Display Features

### Beautiful HTML Output
- **Color-coded dosha badges**: Vata (purple), Pitta (pink), Kapha (blue)
- **Gradient backgrounds**: Modern design with smooth transitions
- **Icons and emojis**: Visual indicators for different sections
- **Responsive layout**: Works on different screen sizes

### Organized Sections
- **Diagnosis Header**: Main dosha identification
- **Supporting Evidence**: Symptoms matching dosha
- **Treatment Recommendations**: Organized by category
- **Lifestyle Advice**: Daily routine suggestions
- **Medical Disclaimer**: Important safety information

### Interactive Elements
- **Real-time analysis**: Instant results as you type
- **Parameter adjustment**: Control RAG and temperature
- **Progress indicators**: Visual feedback during analysis
- **Error handling**: Clear error messages

## 🧪 Example Symptoms

### Vata Imbalance
```
"I have joint pain that worsens in cold weather, cracking sounds in my knees, constipation, and anxiety. I have trouble sleeping and my skin is very dry."
```

### Pitta Imbalance
```
"I frequently get heartburn and acid reflux, especially after eating spicy foods. I have a reddish complexion, feel hot often, and get irritated easily."
```

### Kapha Imbalance
```
"I feel very tired and sluggish, have gained weight, and feel congested. I sleep too much and have slow digestion."
```

## 📁 Project Structure

```
Ayurvedic_Diagnostic_Assistant/
├── src/
│   ├── ai/                    # AI components
│   │   ├── diagnostic_engine.py
│   │   ├── gemini_client.py
│   │   └── prompts.py
│   ├── config/                # Configuration
│   │   └── settings.py
│   ├── data_processing/       # Data processing
│   │   ├── document_loader.py
│   │   └── text_chunker.py
│   ├── rag/                   # RAG system
│   │   ├── embeddings.py
│   │   ├── retriever.py
│   │   └── vector_store.py
│   ├── ui/                    # User interface
│   │   ├── display.py
│   │   └── gradio_ui.py      # Gradio web interface
│   └── utils/                 # Utilities
│       └── helpers.py
├── tests/                     # Test files
├── data/                      # Data files
├── requirements.txt           # Dependencies
├── setup.py                  # Setup script
├── gradio_demo.py            # Gradio web interface demo
└── README.md                 # This file
```

## 🔧 Configuration

### Environment Variables
Create a `.env` file with:
```
GOOGLE_API_KEY=your_google_api_key_here
```

### Settings
Modify `src/config/settings.py` for:
- Model parameters
- RAG settings
- Display options
- Logging configuration

## 🧪 Testing

Run the test suite:
```bash
python -m pytest tests/
```

## 📚 Documentation

- **[Example Usage](example_usage.py)**: Basic usage examples
- **[Interactive Demo](interactive_demo.py)**: Interactive command-line interface
- **[Gradio Demo](gradio_demo.py)**: Web-based interface
- **[Display Demo](demo_display.py)**: Display functionality demo

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

**Medical Disclaimer**: This tool is for educational and informational purposes only. It should not replace professional medical advice. Always consult with qualified Ayurvedic practitioners for proper diagnosis and treatment.

## 🆘 Support

If you encounter any issues:

1. Ensure your Google API key is properly configured
2. Verify all dependencies are installed
3. Check the logs for detailed error messages
4. Make sure you have internet connection for API calls

## 🎉 Acknowledgments

- Built with Google Gemini AI
- Uses sentence-transformers for embeddings
- Web interface powered by Gradio
- Beautiful display system with custom CSS

---

**Happy Diagnosing! 🌿**

For more information, run the interactive demos or check the example usage scripts. 