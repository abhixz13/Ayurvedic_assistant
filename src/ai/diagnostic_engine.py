"""
Main diagnostic engine for Ayurvedic analysis.
"""

import logging
import json
import re
from typing import Dict, Any, List, Optional
from src.ai.gemini_client import GeminiClient
from src.ai.prompts import PromptManager
from src.rag.retriever import AyurvedicRetriever
from src.config.settings import settings

logger = logging.getLogger(__name__)


class AyurvedicDiagnosticEngine:
    """Main engine for Ayurvedic diagnostic analysis."""
    
    def __init__(self, 
                 gemini_client: GeminiClient = None,
                 retriever: AyurvedicRetriever = None,
                 prompt_manager: PromptManager = None):
        """
        Initialize the diagnostic engine.
        
        Args:
            gemini_client: Gemini client instance
            retriever: Ayurvedic retriever instance
            prompt_manager: Prompt manager instance
        """
        self.gemini_client = gemini_client or GeminiClient()
        self.retriever = retriever or AyurvedicRetriever()
        self.prompt_manager = prompt_manager or PromptManager()
        
        logger.info("Initialized Ayurvedic Diagnostic Engine")
    
    def chat(self, user_message: str, 
             use_rag: bool = True,
             temperature: float = None,
             conversation_history: List[Dict] = None) -> str:
        """
        Handle conversational chat with the user.
        
        Args:
            user_message: User's message
            use_rag: Whether to use RAG for context retrieval
            temperature: Model temperature for generation
            conversation_history: Previous conversation turns
            
        Returns:
            Assistant's conversational response
        """
        try:
            logger.info(f"Processing chat message: {user_message[:100]}...")
            
            # Step 1: Retrieve relevant context (RAG) for health-related queries
            context = ""
            if use_rag and self.retriever.is_initialized():
                # Only retrieve context for health-related queries
                if self._is_health_related(user_message):
                    context = self.retriever.get_relevant_context(user_message)
                    logger.info(f"Retrieved context with {len(context)} characters")
                else:
                    logger.info("Query not health-related, skipping RAG retrieval")
            else:
                logger.info("RAG not available or not initialized, proceeding without context")
            
            # Step 2: Create conversational prompt
            prompt = self.prompt_manager.create_conversational_prompt(
                user_message=user_message,
                context=context,
                conversation_history=conversation_history
            )
            
            # Step 3: Generate response
            response = self.gemini_client.generate_text_response(
                prompt=prompt,
                temperature=temperature or settings.temperature
            )
            
            # Step 4: Validate response
            if not self.prompt_manager.validate_response(response):
                logger.warning("Generated response was incomplete, generating fallback")
                response = self._generate_fallback_response(user_message)
            
            logger.info("Chat response generated successfully")
            return response
            
        except Exception as e:
            logger.error(f"Error in chat processing: {e}")
            return f"I apologize, but I'm having trouble processing your request right now. Could you please try again? If the problem persists, please check your internet connection."
    
    def _is_health_related(self, message: str) -> bool:
        """
        Determine if a message is health-related.
        
        Args:
            message: User's message
            
        Returns:
            True if health-related, False otherwise
        """
        health_keywords = [
            'pain', 'symptom', 'health', 'sick', 'ill', 'disease', 'condition',
            'dosha', 'vata', 'pitta', 'kapha', 'ayurveda', 'treatment',
            'medicine', 'herb', 'diet', 'lifestyle', 'wellness', 'healing',
            'joint', 'headache', 'stomach', 'digestion', 'sleep', 'energy',
            'stress', 'anxiety', 'depression', 'skin', 'hair', 'weight',
            'blood', 'heart', 'lung', 'liver', 'kidney', 'bone', 'muscle',
            'tired', 'fatigue', 'sluggish', 'weak', 'exhausted', 'dizzy',
            'nausea', 'vomiting', 'fever', 'cough', 'cold', 'flu', 'infection',
            'inflammation', 'swelling', 'rash', 'itch', 'burn', 'numb',
            'tingle', 'cramp', 'spasm', 'stiff', 'sore', 'ache', 'throb',
            'pulse', 'heartbeat', 'breath', 'breathe', 'chest', 'back',
            'neck', 'shoulder', 'arm', 'leg', 'foot', 'hand', 'finger',
            'toe', 'eye', 'ear', 'nose', 'throat', 'mouth', 'tongue',
            'appetite', 'hunger', 'thirst', 'urine', 'bowel', 'constipation',
            'diarrhea', 'bloating', 'gas', 'acid', 'reflux', 'ulcer'
        ]
        
        message_lower = message.lower()
        return any(keyword in message_lower for keyword in health_keywords)
    
    def _generate_fallback_response(self, user_message: str) -> str:
        """
        Generate a fallback response when the main response is incomplete.
        
        Args:
            user_message: User's message
            
        Returns:
            Fallback response
        """
        if self._is_health_related(user_message):
            return "I understand you're asking about health concerns. Let me help you with that. Could you please provide more specific details about your symptoms or what you'd like to know about Ayurvedic health?"
        else:
            return "I'm sorry, that's outside my scope. I'm here to help with Ayurvedic and health-related questions. How can I assist you with your wellness journey?"
    
    def analyze_symptoms(self, symptoms: str, 
                        use_rag: bool = True,
                        temperature: float = None) -> Dict[str, Any]:
        """
        Analyze patient symptoms and provide Ayurvedic diagnosis.
        
        Args:
            symptoms: Patient symptoms
            use_rag: Whether to use RAG for context retrieval
            temperature: Model temperature for generation
            
        Returns:
            Dictionary with diagnosis results
        """
        try:
            logger.info(f"Analyzing symptoms: {symptoms[:100]}...")
            
            # Step 1: Retrieve relevant context (RAG)
            context = ""
            if use_rag and self.retriever.is_initialized():
                context = self.retriever.get_relevant_context(symptoms)
                logger.info(f"Retrieved context with {len(context)} characters")
            else:
                logger.info("RAG not available or not initialized, proceeding without context")
            
            # Step 2: Create prompt
            if context:
                prompt = self.prompt_manager.create_diagnostic_prompt(symptoms, context)
            else:
                prompt = self.prompt_manager.create_simple_prompt(symptoms)
            
            # Step 3: Generate response
            result = self.gemini_client.generate_json_response(
                prompt=prompt,
                temperature=temperature or settings.temperature
            )
            
            # Step 4: Parse and validate response
            parsed_result = self._parse_diagnostic_response(result)
            
            # Add metadata
            parsed_result["metadata"] = {
                "symptoms": symptoms,
                "use_rag": use_rag,
                "temperature": temperature or settings.temperature,
                "model": self.gemini_client.model_name,
                "context_length": len(context) if context else 0
            }
            
            logger.info("Diagnostic analysis completed successfully")
            return parsed_result
            
        except Exception as e:
            logger.error(f"Error in diagnostic analysis: {e}")
            return {
                "error": f"Diagnostic analysis failed: {str(e)}",
                "symptoms": symptoms,
                "use_rag": use_rag
            }
    
    def _parse_diagnostic_response(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Parse and validate the diagnostic response.
        
        Args:
            result: Raw response from Gemini model
            
        Returns:
            Parsed and validated result
        """
        try:
            # Check for errors
            if "error" in result:
                return {
                    "error": result["error"],
                    "raw_content": result.get("content", "")
                }
            
            # Try to get parsed JSON
            if "parsed_json" in result and result["parsed_json"]:
                return result["parsed_json"]
            
            # Try to extract JSON from content
            content = result.get("content", "")
            json_match = self._extract_json_from_content(content)
            
            if json_match:
                try:
                    parsed_json = json.loads(json_match)
                    return parsed_json
                except json.JSONDecodeError as e:
                    logger.warning(f"Failed to parse extracted JSON: {e}")
            
            # Return raw content if JSON parsing fails
            return {
                "error": "Failed to parse JSON response",
                "raw_content": content,
                "json_error": result.get("json_error", "Unknown parsing error")
            }
            
        except Exception as e:
            logger.error(f"Error parsing diagnostic response: {e}")
            return {
                "error": f"Response parsing failed: {str(e)}",
                "raw_content": result.get("content", "")
            }
    
    def _extract_json_from_content(self, content: str) -> Optional[str]:
        """
        Extract JSON from model response content.
        
        Args:
            content: Raw content from model
            
        Returns:
            Extracted JSON string or None
        """
        try:
            # Try to find JSON block
            json_patterns = [
                r'```json\s*(\{.*\})\s*```',  # JSON in markdown code block
                r'```\s*(\{.*\})\s*```',      # JSON in code block
                r'(\{.*\})',                    # Any JSON object
            ]
            
            for pattern in json_patterns:
                match = re.search(pattern, content, re.DOTALL)
                if match:
                    return match.group(1)
            
            return None
            
        except Exception as e:
            logger.error(f"Error extracting JSON: {e}")
            return None
    
    def batch_analyze_symptoms(self, symptoms_list: List[str], 
                              use_rag: bool = True) -> List[Dict[str, Any]]:
        """
        Analyze multiple symptom sets in batch.
        
        Args:
            symptoms_list: List of symptom strings
            use_rag: Whether to use RAG for context retrieval
            
        Returns:
            List of diagnostic results
        """
        results = []
        
        for i, symptoms in enumerate(symptoms_list):
            logger.info(f"Processing batch item {i+1}/{len(symptoms_list)}")
            result = self.analyze_symptoms(symptoms, use_rag)
            results.append(result)
        
        return results
    
    def get_system_info(self) -> Dict[str, Any]:
        """Get information about the diagnostic system."""
        return {
            "gemini_client": self.gemini_client.get_model_info(),
            "retriever_initialized": self.retriever.is_initialized(),
            "vector_store_info": self.retriever.get_vector_store_info(),
            "settings": {
                "temperature": settings.temperature,
                "max_tokens": settings.max_tokens,
                "top_k_retrieval": settings.top_k_retrieval
            }
        }
    
    def test_system(self) -> Dict[str, Any]:
        """Test the diagnostic system components."""
        test_results = {
            "gemini_connection": self.gemini_client.test_connection(),
            "retriever_available": self.retriever.is_initialized(),
            "prompt_validation": self.prompt_manager.validate_prompt(
                self.prompt_manager.create_simple_prompt("test symptoms")
            )
        }
        
        # Test with sample symptoms
        if test_results["gemini_connection"]:
            sample_symptoms = "I have mild joint pain and feel tired"
            test_diagnosis = self.analyze_symptoms(sample_symptoms, use_rag=False)
            test_results["sample_diagnosis"] = "error" not in test_diagnosis
        
        return test_results
    
    def validate_diagnosis(self, diagnosis: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate a diagnosis result.
        
        Args:
            diagnosis: Diagnosis dictionary
            
        Returns:
            Validation results
        """
        validation = {
            "is_valid": True,
            "missing_fields": [],
            "recommendations": []
        }
        
        required_fields = [
            "dominant_dosha",
            "imbalances", 
            "diagnosis",
            "supporting_evidence",
            "recommended_treatments"
        ]
        
        for field in required_fields:
            if field not in diagnosis:
                validation["is_valid"] = False
                validation["missing_fields"].append(field)
        
        # Check dosha values
        valid_doshas = ["Vata", "Pitta", "Kapha"]
        if "dominant_dosha" in diagnosis:
            if diagnosis["dominant_dosha"] not in valid_doshas:
                validation["recommendations"].append("Invalid dosha value")
        
        # Check treatment structure
        if "recommended_treatments" in diagnosis:
            treatments = diagnosis["recommended_treatments"]
            required_treatment_types = ["dietary", "herbs", "therapies", "lifestyle"]
            
            for treatment_type in required_treatment_types:
                if treatment_type not in treatments:
                    validation["recommendations"].append(f"Missing {treatment_type} recommendations")
        
        return validation 