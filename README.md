# 🩺 Ayurvedic Diagnostic Assistant

An AI-powered Ayurvedic diagnostic assistant with interactive display and RAG (Retrieval-Augmented Generation) system.

## 🌟 Features

- **Interactive Diagnostic Interface**: Beautiful UI with real-time symptom analysis
- **RAG System**: Knowledge base integration for accurate Ayurvedic recommendations
- **Beautiful HTML Display**: Color-coded dosha identification and treatment recommendations
- **Jupyter Notebook Interface**: Full interactive experience with widgets
- **Batch Analysis**: Process multiple symptom sets at once
- **Comprehensive Documentation**: Detailed guides and examples

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Google API key for Gemini
- Internet connection for API calls

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/YOUR_USERNAME/Ayurvedic_Diagnostic_Assistant.git
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

4. **Run the interactive demo**:
   ```bash
   python interactive_demo.py
   ```

## 🎯 Usage

### Interactive Demo
```bash
python interactive_demo.py
```

### Jupyter Notebook Interface
```bash
jupyter notebook notebooks/main_assistant.ipynb
```

### Display Demo
```bash
python demo_display.py
```

### Example Usage
```bash
python example_usage.py
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
│   │   └── widgets.py
│   └── utils/                 # Utilities
│       └── helpers.py
├── notebooks/                 # Jupyter notebooks
│   └── main_assistant.ipynb
├── tests/                     # Test files
├── data/                      # Data files
├── requirements.txt           # Dependencies
├── setup.py                  # Setup script
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

- **[Display Guide](DISPLAY_GUIDE.md)**: Comprehensive guide for using the display system
- **[Example Usage](example_usage.py)**: Basic usage examples
- **[Interactive Demo](interactive_demo.py)**: Interactive command-line interface
- **[Jupyter Notebook](notebooks/main_assistant.ipynb)**: Full interactive experience

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

1. Check the [Display Guide](DISPLAY_GUIDE.md) for troubleshooting
2. Ensure your Google API key is properly configured
3. Verify all dependencies are installed
4. Check the logs for detailed error messages

## 🎉 Acknowledgments

- Built with Google Gemini AI
- Uses sentence-transformers for embeddings
- Interactive widgets powered by ipywidgets
- Beautiful display system with custom CSS

---

**Happy Diagnosing! 🌿**

For more information, check the [Display Guide](DISPLAY_GUIDE.md) or run the interactive demos. 