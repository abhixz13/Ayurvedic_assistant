# Ayurvedic Knowledge AI Assistant

An intelligent diagnostic assistant that leverages Google's Gemini model and Retrieval-Augmented Generation (RAG) to provide Ayurvedic analysis and recommendations based on traditional principles.

## 🎯 Project Overview

This AI assistant analyzes patient symptoms through the lens of traditional Ayurvedic principles (Tridosha theory: Vata, Pitta, Kapha) and provides structured diagnostic reports with treatment recommendations.

## 🚀 Key Features

- **RAG-Enhanced Analysis**: Combines Gemini model with Ayurvedic knowledge base
- **Structured Output**: Generates consistent JSON-formatted diagnostic reports
- **Interactive Interface**: User-friendly Jupyter notebook interface
- **Comprehensive Treatment Plans**: Diet, herbs, medicines, therapies, and lifestyle recommendations
- **Evidence-Based**: Grounded in traditional Ayurvedic texts and principles

## 📁 Project Structure

```
Ayurvedic_Diagnostic_Assistant/
├── data/                           # Ayurvedic texts and documents
│   ├── raw/                       # Original PDF documents
│   └── processed/                 # Processed text chunks
├── src/                           # Source code
│   ├── __init__.py
│   ├── config/                    # Configuration files
│   │   ├── __init__.py
│   │   └── settings.py
│   ├── data_processing/           # Document processing modules
│   │   ├── __init__.py
│   │   ├── document_loader.py
│   │   └── text_chunker.py
│   ├── rag/                       # RAG implementation
│   │   ├── __init__.py
│   │   ├── embeddings.py
│   │   ├── vector_store.py
│   │   └── retriever.py
│   ├── ai/                        # AI and model components
│   │   ├── __init__.py
│   │   ├── gemini_client.py
│   │   ├── prompts.py
│   │   └── diagnostic_engine.py
│   ├── ui/                        # User interface components
│   │   ├── __init__.py
│   │   ├── display.py
│   │   └── widgets.py
│   └── utils/                     # Utility functions
│       ├── __init__.py
│       └── helpers.py
├── notebooks/                     # Jupyter notebooks
│   ├── main_assistant.ipynb
│   └── testing.ipynb
├── tests/                         # Test files
│   ├── __init__.py
│   ├── test_diagnostic_engine.py
│   └── test_rag.py
├── .env.example                   # Environment variables template
├── requirements.txt               # Python dependencies
└── README.md                     # This file
```

## 🛠️ Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd Ayurvedic_Diagnostic_Assistant
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env and add your Google API key
   ```

## 🔧 Configuration

1. **Google API Key**: Get your API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
2. **Environment Variables**: Create a `.env` file with:
   ```
   GOOGLE_API_KEY=your_api_key_here
   ```

## 📚 Usage

### Quick Start

1. **Launch Jupyter Notebook**:
   ```bash
   jupyter notebook
   ```

2. **Open the main notebook**:
   ```
   notebooks/main_assistant.ipynb
   ```

3. **Follow the setup steps**:
   - Load Ayurvedic documents
   - Initialize the RAG system
   - Start the interactive diagnostic assistant

### Programmatic Usage

```python
from src.ai.diagnostic_engine import AyurvedicDiagnosticEngine
from src.rag.vector_store import VectorStore

# Initialize the system
vector_store = VectorStore()
diagnostic_engine = AyurvedicDiagnosticEngine()

# Analyze symptoms
symptoms = "I have joint pain, dry skin, and anxiety"
diagnosis = diagnostic_engine.analyze_symptoms(symptoms)
```

## 🧪 Testing

Run the test suite:
```bash
python -m pytest tests/
```

## 📖 Documentation

- **API Documentation**: See individual module docstrings
- **Examples**: Check the `notebooks/` directory for usage examples
- **Configuration**: See `src/config/settings.py` for all configurable options

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## ⚠️ Disclaimer

This AI assistant is for educational and informational purposes only. It should not replace professional medical advice. Always consult with qualified Ayurvedic practitioners for proper diagnosis and treatment.

## 🆘 Support

For issues and questions:
- Check the documentation
- Review existing issues
- Create a new issue with detailed information

---

**Built with ❤️ for Ayurvedic knowledge preservation and accessibility** 