"""
Helper utilities for the Ayurvedic Diagnostic Assistant.
"""

import os
import logging
import json
from pathlib import Path
from typing import Dict, Any, List
from src.config.settings import settings

logger = logging.getLogger(__name__)


def setup_logging(level: str = "INFO") -> None:
    """
    Setup logging configuration.
    
    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR)
    """
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('ayurvedic_assistant.log')
        ]
    )
    
    # Set specific logger levels
    logging.getLogger('urllib3').setLevel(logging.WARNING)
    logging.getLogger('requests').setLevel(logging.WARNING)


def validate_environment() -> Dict[str, Any]:
    """
    Validate the environment setup.
    
    Returns:
        Dictionary with validation results
    """
    validation_results = {
        "environment_valid": True,
        "missing_requirements": [],
        "warnings": []
    }
    
    # Check required environment variables
    if not settings.google_api_key:
        validation_results["environment_valid"] = False
        validation_results["missing_requirements"].append("GOOGLE_API_KEY")
    
    # Check directories
    required_dirs = [
        settings.data_raw_path,
        settings.data_processed_path,
        os.path.dirname(settings.vector_store_path)
    ]
    
    for directory in required_dirs:
        if not os.path.exists(directory):
            try:
                os.makedirs(directory, exist_ok=True)
                validation_results["warnings"].append(f"Created directory: {directory}")
            except Exception as e:
                validation_results["environment_valid"] = False
                validation_results["missing_requirements"].append(f"Directory: {directory}")
    
    # Check file permissions
    try:
        test_file = os.path.join(settings.data_processed_path, "test.txt")
        with open(test_file, 'w') as f:
            f.write("test")
        os.remove(test_file)
    except Exception as e:
        validation_results["environment_valid"] = False
        validation_results["missing_requirements"].append(f"Write permissions: {settings.data_processed_path}")
    
    return validation_results


def create_sample_data() -> Dict[str, Any]:
    """
    Create sample Ayurvedic text data for testing.
    
    Returns:
        Dictionary with sample data information
    """
    sample_texts = {
        "vata_imbalance": """
        Vata dosha is composed of air and ether elements. When Vata is imbalanced, 
        it can cause symptoms such as anxiety, insomnia, dry skin, constipation, 
        joint pain, and irregular digestion. Vata imbalance is often aggravated by 
        cold, dry weather, irregular routines, and excessive travel.
        
        Treatment for Vata imbalance includes warm, cooked foods, regular daily 
        routines, warm oil massage (Abhyanga), and grounding practices like yoga 
        and meditation. Herbs like Ashwagandha, Guggulu, and Haritaki are beneficial.
        """,
        
        "pitta_imbalance": """
        Pitta dosha is composed of fire and water elements. Pitta imbalance 
        manifests as inflammation, heat, acidity, skin rashes, irritability, 
        and excessive thirst. Pitta is aggravated by hot weather, spicy foods, 
        and excessive stress.
        
        Cooling treatments are essential for Pitta imbalance. This includes 
        cooling foods, avoiding spicy and sour tastes, and using herbs like 
        Amalaki, Guduchi, and Shatavari. Therapies like Shirodhara with 
        cooling oils are beneficial.
        """,
        
        "kapha_imbalance": """
        Kapha dosha is composed of earth and water elements. Kapha imbalance 
        leads to weight gain, lethargy, congestion, slow digestion, and 
        excessive sleep. Kapha is aggravated by cold, damp weather and 
        heavy, sweet foods.
        
        Treatment for Kapha imbalance includes stimulating practices, light 
        foods, regular exercise, and herbs like Trikatu, Guggulu, and 
        Punarnava. Therapies like Udvartana (dry massage) are beneficial.
        """
    }
    
    # Create sample files
    sample_files = {}
    for name, content in sample_texts.items():
        file_path = os.path.join(settings.data_raw_path, f"{name}.txt")
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            sample_files[name] = file_path
        except Exception as e:
            logger.error(f"Error creating sample file {name}: {e}")
    
    return {
        "sample_files_created": len(sample_files),
        "file_paths": sample_files,
        "total_content_length": sum(len(content) for content in sample_texts.values())
    }


def save_diagnosis_results(results: List[Dict[str, Any]], 
                          output_path: str = None) -> str:
    """
    Save diagnosis results to a JSON file.
    
    Args:
        results: List of diagnosis results
        output_path: Path to save results
        
    Returns:
        Path where results were saved
    """
    if output_path is None:
        output_path = os.path.join(settings.data_processed_path, 
                                  f"diagnosis_results_{len(results)}.json")
    
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Saved {len(results)} diagnosis results to {output_path}")
        return output_path
        
    except Exception as e:
        logger.error(f"Error saving diagnosis results: {e}")
        raise


def load_diagnosis_results(file_path: str) -> List[Dict[str, Any]]:
    """
    Load diagnosis results from a JSON file.
    
    Args:
        file_path: Path to the results file
        
    Returns:
        List of diagnosis results
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            results = json.load(f)
        
        logger.info(f"Loaded {len(results)} diagnosis results from {file_path}")
        return results
        
    except Exception as e:
        logger.error(f"Error loading diagnosis results: {e}")
        raise


def get_system_info() -> Dict[str, Any]:
    """
    Get comprehensive system information.
    
    Returns:
        Dictionary with system information
    """
    import platform
    import sys
    
    return {
        "python_version": sys.version,
        "platform": platform.platform(),
        "settings": {
            "model_name": settings.model_name,
            "temperature": settings.temperature,
            "embedding_model": settings.embedding_model,
            "chunk_size": settings.chunk_size,
            "top_k_retrieval": settings.top_k_retrieval
        },
        "paths": {
            "data_raw": settings.data_raw_path,
            "data_processed": settings.data_processed_path,
            "vector_store": settings.vector_store_path
        },
        "environment": validate_environment()
    }


def create_test_cases() -> List[Dict[str, str]]:
    """
    Create test cases for validation.
    
    Returns:
        List of test cases with symptoms and expected outcomes
    """
    return [
        {
            "symptoms": "I have joint pain that worsens in cold weather, cracking sounds in my knees, constipation, and anxiety. I have trouble sleeping and my skin is very dry.",
            "expected_dosha": "Vata",
            "description": "Classic Vata imbalance symptoms"
        },
        {
            "symptoms": "I frequently get heartburn and acid reflux, especially after eating spicy foods. I have a reddish complexion, feel hot often, and get irritated easily. I also have some skin rashes that worsen when I'm stressed.",
            "expected_dosha": "Pitta", 
            "description": "Classic Pitta imbalance symptoms"
        },
        {
            "symptoms": "I feel very tired and sluggish, have gained weight, and feel congested. I sleep too much and have slow digestion. I feel heavy and lethargic.",
            "expected_dosha": "Kapha",
            "description": "Classic Kapha imbalance symptoms"
        }
    ] 