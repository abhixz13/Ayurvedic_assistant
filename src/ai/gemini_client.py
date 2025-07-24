"""
Gemini client for interacting with Google's Gemini model.
"""

import logging
import json
from typing import Dict, Any, Optional, List
import google.generativeai as genai
from src.config.settings import settings

logger = logging.getLogger(__name__)


class GeminiClient:
    """Client for interacting with Google's Gemini model."""
    
    def __init__(self, api_key: str = None, model_name: str = None):
        """
        Initialize Gemini client.
        
        Args:
            api_key: Google API key
            model_name: Name of the Gemini model to use
        """
        self.api_key = api_key or settings.google_api_key
        self.model_name = model_name or settings.model_name
        
        if not self.api_key:
            raise ValueError("Google API key is required")
        
        # Configure the API
        genai.configure(api_key=self.api_key)
        
        # Initialize the model
        try:
            self.model = genai.GenerativeModel(self.model_name)
            logger.info(f"Initialized Gemini model: {self.model_name}")
        except Exception as e:
            logger.error(f"Error initializing Gemini model: {e}")
            raise
    
    def generate_content(self, prompt: str, 
                        temperature: float = None,
                        max_tokens: int = None) -> Dict[str, Any]:
        """
        Generate content using the Gemini model.
        
        Args:
            prompt: Input prompt
            temperature: Sampling temperature (0.0 to 1.0)
            max_tokens: Maximum number of tokens to generate
            
        Returns:
            Dictionary with generated content and metadata
        """
        try:
            # Set generation config
            generation_config = genai.types.GenerationConfig(
                temperature=temperature or settings.temperature,
                max_output_tokens=max_tokens or settings.max_tokens
            )
            
            # Generate content
            response = self.model.generate_content(
                prompt,
                generation_config=generation_config
            )
            
            # Extract content
            if hasattr(response, 'text'):
                content = response.text
            else:
                content = str(response)
            
            result = {
                "content": content,
                "model": self.model_name,
                "temperature": temperature or settings.temperature,
                "max_tokens": max_tokens or settings.max_tokens
            }
            
            logger.info(f"Generated content successfully using {self.model_name}")
            return result
            
        except Exception as e:
            logger.error(f"Error generating content: {e}")
            return {
                "content": f"Error generating content: {str(e)}",
                "error": str(e),
                "model": self.model_name
            }
    
    def generate_json_response(self, prompt: str, 
                             temperature: float = None,
                             max_tokens: int = None) -> Dict[str, Any]:
        """
        Generate JSON response from the model.
        
        Args:
            prompt: Input prompt
            temperature: Sampling temperature
            max_tokens: Maximum number of tokens
            
        Returns:
            Dictionary with parsed JSON response
        """
        try:
            # Generate JSON response
            result = self.generate_content(
                prompt=prompt,
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            # Parse JSON content
            if "error" not in result:
                try:
                    # Extract JSON from markdown code blocks
                    content = result["content"]
                    json_match = self._extract_json_from_content(content)
                    
                    if json_match:
                        json_content = json.loads(json_match)
                        result["parsed_json"] = json_content
                    else:
                        # Fallback to direct parsing
                        json_content = json.loads(content)
                        result["parsed_json"] = json_content
                        
                except json.JSONDecodeError as e:
                    logger.warning(f"Failed to parse JSON response: {e}")
                    result["parsed_json"] = None
                    result["json_error"] = str(e)
            
            return result
            
        except Exception as e:
            logger.error(f"Error generating JSON response: {e}")
            return {
                "content": f"Error generating JSON response: {str(e)}",
                "error": str(e),
                "model": self.model_name
            }
    
    def chat_conversation(self, messages: List[Dict[str, str]], 
                         temperature: float = None) -> Dict[str, Any]:
        """
        Conduct a chat conversation with the model.
        
        Args:
            messages: List of message dictionaries with 'role' and 'content'
            temperature: Sampling temperature
            
        Returns:
            Dictionary with model response
        """
        try:
            # Create chat session
            chat = self.model.start_chat(history=[])
            
            # Add messages to chat
            for message in messages:
                if message["role"] == "user":
                    chat.send_message(message["content"])
                elif message["role"] == "assistant":
                    # For assistant messages, we need to handle them differently
                    # This is a simplified approach
                    pass
            
            # Get the last user message
            last_user_message = messages[-1]["content"] if messages else ""
            
            # Generate response
            response = chat.send_message(last_user_message)
            
            result = {
                "content": response.text,
                "model": self.model_name,
                "temperature": temperature or settings.temperature,
                "conversation_length": len(messages)
            }
            
            logger.info(f"Generated chat response successfully")
            return result
            
        except Exception as e:
            logger.error(f"Error in chat conversation: {e}")
            return {
                "content": f"Error in chat conversation: {str(e)}",
                "error": str(e),
                "model": self.model_name
            }
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the current model."""
        return {
            "model_name": self.model_name,
            "api_key_configured": bool(self.api_key),
            "temperature": settings.temperature,
            "max_tokens": settings.max_tokens
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
            import re
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
    
    def test_connection(self) -> bool:
        """Test the connection to the Gemini API."""
        try:
            test_prompt = "Hello, this is a test message. Please respond with 'OK'."
            result = self.generate_content(test_prompt, temperature=0.1)
            
            if "error" not in result:
                logger.info("Gemini API connection test successful")
                return True
            else:
                logger.error(f"Gemini API connection test failed: {result.get('error')}")
                return False
                
        except Exception as e:
            logger.error(f"Gemini API connection test failed: {e}")
            return False 