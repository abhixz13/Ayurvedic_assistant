# 🏗️ Ayurvedic Diagnostic Assistant - System Design

## 📋 Overview

This document provides a comprehensive system design overview of the Ayurvedic Diagnostic Assistant, tracing the complete flow from user input to response generation.

## 🎯 System Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   User Input    │───▶│  Gradio UI      │───▶│  Diagnostic     │
│   (Symptoms)    │    │  (gradio_ui.py) │    │  Engine         │
└─────────────────┘    └─────────────────┘    │(diagnostic_engine.py)
                                              └─────────────────┘
                                                       │
                                                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Beautiful     │◀───│  Display        │◀───│  Gemini AI      │
│   HTML Output   │    │  (display.py)   │    │  (gemini_client.py)
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🔄 Complete User Journey Flow

### 1. **User Input Phase**
**File: `gradio_demo.py`**
- User enters symptoms in the Gradio web interface
- User can adjust RAG settings and temperature
- User clicks "Analyze Symptoms" button

### 2. **Gradio Interface Processing**
**File: `src/ui/gradio_ui.py`**
- `GradioDiagnosticUI.analyze_symptoms()` function receives input
- Validates user input (checks if symptoms are provided)
- Calls the diagnostic callback function
- Handles errors and displays appropriate messages

### 3. **Diagnostic Engine Processing**
**File: `src/ai/diagnostic_engine.py`**
- `AyurvedicDiagnosticEngine.analyze_symptoms()` method:
  - **Step 1**: Retrieves relevant context using RAG (if enabled)
  - **Step 2**: Creates appropriate prompt based on context availability
  - **Step 3**: Generates response using Gemini AI
  - **Step 4**: Parses and validates the response
  - **Step 5**: Adds metadata to the result

### 4. **RAG (Retrieval-Augmented Generation)**
**File: `src/rag/retriever.py`**
- `AyurvedicRetriever.get_relevant_context()` method:
  - Searches vector store for relevant Ayurvedic knowledge
  - Retrieves top-k most similar documents
  - Formats context for inclusion in prompt

### 5. **Prompt Management**
**File: `src/ai/prompts.py`**
- `PromptManager.create_diagnostic_prompt()` or `create_simple_prompt()`:
  - Constructs appropriate prompt based on available context
  - Includes symptoms and retrieved knowledge
  - Ensures proper JSON response format

### 6. **AI Model Interaction**
**File: `src/ai/gemini_client.py`**
- `GeminiClient.generate_json_response()` method:
  - Sends prompt to Google Gemini model
  - Configures temperature and token limits
  - Extracts and validates JSON response
  - Handles API errors gracefully

### 7. **Response Processing**
**File: `src/ai/diagnostic_engine.py`**
- `_parse_diagnostic_response()` method:
  - Extracts JSON from model response
  - Validates response structure
  - Ensures all required fields are present
  - Handles malformed responses

### 8. **Display Generation**
**File: `src/ui/display.py`**
- `DiagnosisDisplay.display_diagnosis()` method:
  - Generates beautiful HTML output
  - Applies CSS styling with color-coded dosha badges
  - Organizes information into sections:
    - Dominant dosha analysis
    - Identified imbalances
    - Supporting evidence
    - Treatment recommendations
    - Lifestyle advice
    - Medical disclaimers

### 9. **User Response**
**File: `src/ui/gradio_ui.py`**
- Returns formatted HTML to Gradio interface
- Updates status message with analysis results
- Displays beautiful, interactive web output

## 📁 File-by-File Responsibility

### **Entry Point Files**
| File | Responsibility |
|------|---------------|
| `gradio_demo.py` | Main entry point, initializes system and launches Gradio UI |
| `interactive_demo.py` | Command-line interface for testing and development |
| `demo_display.py` | Demonstrates display functionality |
| `example_usage.py` | Shows basic usage examples |

### **UI Layer**
| File | Responsibility |
|------|---------------|
| `src/ui/gradio_ui.py` | Gradio web interface components and event handling |
| `src/ui/display.py` | HTML generation and styling for diagnostic results |
| `src/ui/__init__.py` | UI module exports and imports |

### **AI Layer**
| File | Responsibility |
|------|---------------|
| `src/ai/diagnostic_engine.py` | Main orchestration of diagnostic analysis |
| `src/ai/gemini_client.py` | Google Gemini API interaction and response handling |
| `src/ai/prompts.py` | Prompt construction and management |

### **RAG Layer**
| File | Responsibility |
|------|---------------|
| `src/rag/retriever.py` | Knowledge retrieval from vector store |
| `src/rag/vector_store.py` | Vector database management |
| `src/rag/embeddings.py` | Text embedding generation |

### **Data Processing**
| File | Responsibility |
|------|---------------|
| `src/data_processing/document_loader.py` | Document loading and parsing |
| `src/data_processing/text_chunker.py` | Text chunking for vector storage |

### **Configuration & Utilities**
| File | Responsibility |
|------|---------------|
| `src/config/settings.py` | System configuration and environment variables |
| `src/utils/helpers.py` | Utility functions and logging setup |

## 🔧 Detailed Process Flow

### **Step 1: User Input Reception**
```python
# gradio_demo.py -> src/ui/gradio_ui.py
def analyze_symptoms(symptoms: str, use_rag: bool, temperature: float):
    # Validates input
    # Calls diagnostic_callback
    # Returns (status_message, html_output)
```

### **Step 2: Diagnostic Engine Processing**
```python
# src/ai/diagnostic_engine.py
def analyze_symptoms(self, symptoms: str, use_rag: bool, temperature: float):
    # 1. Retrieve context (RAG)
    context = self.retriever.get_relevant_context(symptoms)
    
    # 2. Create prompt
    prompt = self.prompt_manager.create_diagnostic_prompt(symptoms, context)
    
    # 3. Generate response
    result = self.gemini_client.generate_json_response(prompt, temperature)
    
    # 4. Parse response
    parsed_result = self._parse_diagnostic_response(result)
    
    # 5. Add metadata
    parsed_result["metadata"] = {...}
    
    return parsed_result
```

### **Step 3: RAG Context Retrieval**
```python
# src/rag/retriever.py
def get_relevant_context(self, query: str, top_k: int = None):
    # 1. Search vector store
    results = self.vector_store.search(query, top_k)
    
    # 2. Format context
    context_parts = []
    for result in results:
        context_parts.append(f"Source: {result['source']}\n{result['content']}")
    
    return "\n\n".join(context_parts)
```

### **Step 4: AI Model Interaction**
```python
# src/ai/gemini_client.py
def generate_json_response(self, prompt: str, temperature: float):
    # 1. Configure generation
    generation_config = genai.types.GenerationConfig(
        temperature=temperature,
        max_output_tokens=settings.max_tokens
    )
    
    # 2. Generate content
    response = self.model.generate_content(prompt, generation_config)
    
    # 3. Extract JSON
    content = response.text
    json_content = self._extract_json_from_content(content)
    
    return json.loads(json_content)
```

### **Step 5: Response Display**
```python
# src/ui/display.py
def display_diagnosis(self, diagnosis: Dict[str, Any]):
    # 1. Generate HTML
    html_content = self._generate_diagnosis_html(diagnosis)
    
    # 2. Apply CSS styling
    full_html = self.css_styles + html_content
    
    # 3. Return HTML object
    return HTML(full_html)
```

## 🎨 Display Components

### **HTML Structure Generated**
```html
<div class='ayurvedic-diagnosis'>
    <div class='diagnosis-header'>
        <h1>🩺 Ayurvedic Diagnostic Report</h1>
    </div>
    <div class='diagnosis-content'>
        <!-- Dominant Dosha Section -->
        <div class='diagnosis-section'>
            <div class='section-header'>⚖️ Dominant Dosha Analysis</div>
            <div class='section-content'>
                <div class='dosha-vata dosha-badge'>Vata Predominance</div>
            </div>
        </div>
        
        <!-- Supporting Evidence Section -->
        <div class='diagnosis-section'>
            <div class='section-header'>📋 Supporting Evidence</div>
            <div class='section-content'>
                <!-- Evidence content -->
            </div>
        </div>
        
        <!-- Treatment Recommendations -->
        <div class='diagnosis-section'>
            <div class='section-header'>🌱 Treatment Recommendations</div>
            <div class='section-content'>
                <!-- Treatment content -->
            </div>
        </div>
    </div>
</div>
```

## 🔄 Error Handling Flow

### **Input Validation Errors**
- **File**: `src/ui/gradio_ui.py`
- **Function**: `analyze_symptoms()`
- **Action**: Returns error message and empty HTML

### **RAG Errors**
- **File**: `src/rag/retriever.py`
- **Function**: `get_relevant_context()`
- **Action**: Returns empty context, continues without RAG

### **AI Model Errors**
- **File**: `src/ai/gemini_client.py`
- **Function**: `generate_json_response()`
- **Action**: Returns error in response, handled by diagnostic engine

### **Display Errors**
- **File**: `src/ui/display.py`
- **Function**: `display_diagnosis()`
- **Action**: Shows error message with red styling

## 📊 Performance Considerations

### **Response Time Optimization**
1. **RAG Retrieval**: ~100-500ms (depending on vector store size)
2. **AI Model Generation**: ~2-5 seconds (depending on prompt length)
3. **HTML Generation**: ~10-50ms
4. **Total Response Time**: ~3-6 seconds

### **Caching Strategy**
- Vector store embeddings are cached
- CSS styles are pre-generated
- Model responses are not cached (fresh analysis each time)

### **Scalability**
- Gradio handles multiple concurrent users
- Vector store can handle large knowledge bases
- Gemini API has rate limits (handled gracefully)

## 🔧 Configuration Points

### **Environment Variables** (`.env`)
```bash
GOOGLE_API_KEY=your_api_key_here
MODEL_NAME=gemini-2.0-flash-exp
TEMPERATURE=0.2
MAX_TOKENS=4096
```

### **RAG Settings** (`src/config/settings.py`)
```python
EMBEDDING_MODEL=all-MiniLM-L6-v2
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
TOP_K_RETRIEVAL=5
```

### **Display Settings** (`src/ui/display.py`)
- CSS styling for different dosha types
- Color schemes and gradients
- Responsive design elements

## 🚀 Deployment Considerations

### **Local Development**
```bash
python gradio_demo.py
# Access at http://localhost:7860
```

### **Network Deployment**
```bash
python gradio_demo.py
# Access from any device on network
# Modify server_name="0.0.0.0" in gradio_ui.py
```

### **Production Deployment**
- Deploy to cloud platforms (AWS, GCP, Azure)
- Use containerization (Docker)
- Implement proper security measures
- Add monitoring and logging

## 🔍 Monitoring and Logging

### **Key Log Points**
1. **User Input**: `gradio_ui.py` logs symptom input
2. **RAG Retrieval**: `retriever.py` logs context retrieval
3. **AI Generation**: `gemini_client.py` logs API calls
4. **Response Processing**: `diagnostic_engine.py` logs parsing
5. **Display Generation**: `display.py` logs HTML generation

### **Error Tracking**
- All components log errors with context
- User-friendly error messages in UI
- Detailed error logs for debugging

## 📈 Future Enhancements

### **Planned Improvements**
1. **Caching**: Cache common symptom analyses
2. **Batch Processing**: Process multiple symptoms simultaneously
3. **User Sessions**: Save user history and preferences
4. **Advanced RAG**: Implement more sophisticated retrieval
5. **Mobile App**: Native mobile application
6. **API Endpoints**: RESTful API for integration

### **Architecture Evolution**
- Microservices architecture for scalability
- Database integration for user management
- Real-time collaboration features
- Advanced analytics and reporting

---

**This system design ensures a robust, scalable, and user-friendly Ayurvedic diagnostic experience with clear separation of concerns and comprehensive error handling.** 