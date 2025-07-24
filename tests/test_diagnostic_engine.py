"""
Tests for the Ayurvedic Diagnostic Engine.
"""

import unittest
from unittest.mock import Mock, patch
from src.ai.diagnostic_engine import AyurvedicDiagnosticEngine
from src.ai.gemini_client import GeminiClient
from src.rag.retriever import AyurvedicRetriever


class TestAyurvedicDiagnosticEngine(unittest.TestCase):
    """Test cases for AyurvedicDiagnosticEngine."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Mock the dependencies
        self.mock_gemini_client = Mock(spec=GeminiClient)
        self.mock_retriever = Mock(spec=AyurvedicRetriever)
        
        # Create engine with mocked dependencies
        self.engine = AyurvedicDiagnosticEngine(
            gemini_client=self.mock_gemini_client,
            retriever=self.mock_retriever
        )
    
    def test_analyze_symptoms_with_rag(self):
        """Test symptom analysis with RAG enabled."""
        # Mock retriever response
        self.mock_retriever.is_initialized.return_value = True
        self.mock_retriever.get_relevant_context.return_value = "Sample context"
        
        # Mock Gemini response
        mock_response = {
            "parsed_json": {
                "dominant_dosha": "Vata",
                "imbalances": ["Vata excess"],
                "diagnosis": "Vata imbalance",
                "supporting_evidence": {"symptoms_matching_vata": ["joint pain"]},
                "recommended_treatments": {"dietary": ["warm foods"]}
            }
        }
        self.mock_gemini_client.generate_json_response.return_value = mock_response
        
        # Test analysis
        result = self.engine.analyze_symptoms("I have joint pain", use_rag=True)
        
        # Assertions
        self.assertIn("dominant_dosha", result)
        self.assertEqual(result["dominant_dosha"], "Vata")
        self.assertIn("metadata", result)
        self.assertTrue(result["metadata"]["use_rag"])
    
    def test_analyze_symptoms_without_rag(self):
        """Test symptom analysis without RAG."""
        # Mock retriever as not initialized
        self.mock_retriever.is_initialized.return_value = False
        
        # Mock Gemini response
        mock_response = {
            "parsed_json": {
                "dominant_dosha": "Pitta",
                "imbalances": ["Pitta excess"],
                "diagnosis": "Pitta imbalance",
                "supporting_evidence": {"symptoms_matching_pitta": ["heartburn"]},
                "recommended_treatments": {"dietary": ["cooling foods"]}
            }
        }
        self.mock_gemini_client.generate_json_response.return_value = mock_response
        
        # Test analysis
        result = self.engine.analyze_symptoms("I have heartburn", use_rag=False)
        
        # Assertions
        self.assertIn("dominant_dosha", result)
        self.assertEqual(result["dominant_dosha"], "Pitta")
        self.assertFalse(result["metadata"]["use_rag"])
    
    def test_analyze_symptoms_error_handling(self):
        """Test error handling in symptom analysis."""
        # Mock Gemini to raise an exception
        self.mock_gemini_client.generate_json_response.side_effect = Exception("API Error")
        
        # Test analysis
        result = self.engine.analyze_symptoms("I have symptoms")
        
        # Assertions
        self.assertIn("error", result)
        self.assertIn("API Error", result["error"])
    
    def test_batch_analyze_symptoms(self):
        """Test batch symptom analysis."""
        # Mock responses for batch processing
        mock_responses = [
            {"parsed_json": {"dominant_dosha": "Vata", "diagnosis": "Vata imbalance"}},
            {"parsed_json": {"dominant_dosha": "Pitta", "diagnosis": "Pitta imbalance"}}
        ]
        self.mock_gemini_client.generate_json_response.side_effect = mock_responses
        
        # Test batch analysis
        symptoms_list = ["I have joint pain", "I have heartburn"]
        results = self.engine.batch_analyze_symptoms(symptoms_list)
        
        # Assertions
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0]["dominant_dosha"], "Vata")
        self.assertEqual(results[1]["dominant_dosha"], "Pitta")
    
    def test_validate_diagnosis_valid(self):
        """Test validation of a valid diagnosis."""
        valid_diagnosis = {
            "dominant_dosha": "Vata",
            "imbalances": ["Vata excess"],
            "diagnosis": "Vata imbalance",
            "supporting_evidence": {"symptoms_matching_vata": ["joint pain"]},
            "recommended_treatments": {
                "dietary": ["warm foods"],
                "herbs": ["Ashwagandha"],
                "therapies": ["Abhyanga"],
                "lifestyle": ["regular routine"]
            }
        }
        
        validation = self.engine.validate_diagnosis(valid_diagnosis)
        
        # Assertions
        self.assertTrue(validation["is_valid"])
        self.assertEqual(len(validation["missing_fields"]), 0)
    
    def test_validate_diagnosis_invalid(self):
        """Test validation of an invalid diagnosis."""
        invalid_diagnosis = {
            "dominant_dosha": "Invalid",
            "imbalances": ["Some imbalance"]
            # Missing required fields
        }
        
        validation = self.engine.validate_diagnosis(invalid_diagnosis)
        
        # Assertions
        self.assertFalse(validation["is_valid"])
        self.assertGreater(len(validation["missing_fields"]), 0)
        self.assertIn("Invalid dosha value", validation["recommendations"])
    
    def test_get_system_info(self):
        """Test getting system information."""
        # Mock system info
        self.mock_gemini_client.get_model_info.return_value = {"model": "test"}
        self.mock_retriever.is_initialized.return_value = True
        self.mock_retriever.get_vector_store_info.return_value = {"docs": 100}
        
        system_info = self.engine.get_system_info()
        
        # Assertions
        self.assertIn("gemini_client", system_info)
        self.assertIn("retriever_initialized", system_info)
        self.assertTrue(system_info["retriever_initialized"])
    
    def test_test_system(self):
        """Test system testing functionality."""
        # Mock test results
        self.mock_gemini_client.test_connection.return_value = True
        self.mock_retriever.is_initialized.return_value = True
        
        # Mock successful diagnosis
        mock_response = {
            "parsed_json": {
                "dominant_dosha": "Vata",
                "diagnosis": "Test diagnosis"
            }
        }
        self.mock_gemini_client.generate_json_response.return_value = mock_response
        
        test_results = self.engine.test_system()
        
        # Assertions
        self.assertTrue(test_results["gemini_connection"])
        self.assertTrue(test_results["retriever_available"])
        self.assertTrue(test_results["sample_diagnosis"])


if __name__ == "__main__":
    unittest.main() 