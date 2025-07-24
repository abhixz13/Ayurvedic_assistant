"""
Prompt management for Ayurvedic diagnostic assistant.
"""

import logging
from typing import Dict, Any, List
from src.config.settings import settings
from pathlib import Path
from src.rag.embedding_manager import EmbeddingManager
from src.rag.vector_store import VectorStore

logger = logging.getLogger(__name__)


class PromptManager:
    """Manage prompts and few-shot examples for Ayurvedic diagnosis."""
    
    def __init__(self):
        self.few_shot_examples = self._get_few_shot_examples()
        self.base_prompt_template = self._get_base_prompt_template()
    
    def _get_few_shot_examples(self) -> str:
        """Get few-shot examples for structured output."""
        return """
Example 1:
Patient Symptoms: "I've been experiencing joint pain that worsens in cold weather, cracking sounds in my knees, constipation, and anxiety. I have trouble sleeping and my skin is very dry."
Ayurvedic Analysis:
{
"dominant_dosha": "Vata",
"imbalances": ["Vata excess in joints (Sandhi Vata)", "Vata affecting colon (Kostha Vata)", "Vata affecting nervous system (Majja Dhatu)"],
"diagnosis": "Sandhigata Vata (Osteoarthritis with Vata predominance) with associated Anidra (Insomnia) and Kostha Baddhata (Constipation)",
"supporting_evidence": {
    "symptoms_matching_vata": ["joint pain worse in cold", "cracking sounds (Vata in joints)", "constipation", "anxiety", "insomnia", "dry skin"],
    "pulse_indication": "Likely irregular, thready, feeble (Vata pulse)",
    "tongue_indication": "Likely dry, rough, possibly cracked, maybe a brownish coating"
},
"recommended_treatments": {
    "dietary": ["Warm, cooked, unctuous foods", "Favor sweet, sour, and salty tastes", "Include ghee and healthy oils", "Avoid cold, dry, light foods", "Warm water/herbal teas"],
    "herbs": ["Ashwagandha (Withania somnifera) - for strength and stress", "Guggulu (Commiphora wightii) - specific for joints", "Shallaki (Boswellia serrata) - for joint inflammation", "Haritaki (Terminalia chebula) - for constipation"],
    "ayurvedic_medicines": ["Yogaraj Guggulu or Mahayogaraj Guggulu - classical formulation for joints", "Mahanarayan Oil - for external massage on joints", "Ashwagandharishta - for nerve strength and stress", "Castor oil (Eranda Taila) - gentle purgative for Vata constipation (use cautiously)"],
    "therapies": ["Abhyanga (regular warm oil massage)", "Swedana (steam therapy, especially Nadi Sweda for joints)", "Basti (medicated enema, particularly Anuvasana or Matra Basti with appropriate oils)"],
    "lifestyle": ["Maintain regular daily routine (Dinacharya)", "Keep warm, avoid cold drafts", "Gentle, grounding yoga and stretching", "Pranayama (e.g., Nadi Shodhana)", "Meditation for anxiety"]
}
}

Example 2:
Patient Symptoms: "I frequently get heartburn and acid reflux, especially after eating spicy foods. I have a reddish complexion, feel hot often, and get irritated easily. I also have some skin rashes that worsen when I'm stressed."
Ayurvedic Analysis:
{
"dominant_dosha": "Pitta",
"imbalances": ["Pitta excess in digestive tract (Annavaha Srotas)", "Pitta affecting skin (Rakta Dhatu, Bhrajaka Pitta)", "Pitta affecting mind (Sadhaka Pitta)"],
"diagnosis": "Amlapitta (Hyperacidity/GERD) with associated Raktaja Kustha (Pitta-type skin issues)",
"supporting_evidence": {
    "symptoms_matching_pitta": ["heartburn", "acid reflux (sour/bitter taste)", "reddish complexion", "feeling hot", "irritability/anger", "skin rashes worsened by stress/heat"],
    "pulse_indication": "Likely moderate strength, sharp, jumping (Pitta pulse)",
    "tongue_indication": "Likely reddish tongue body, possibly with a yellowish coating"
},
"recommended_treatments": {
    "dietary": ["Cooling foods and drinks", "Favor sweet, bitter, and astringent tastes", "Avoid spicy, sour, salty, fermented foods", "Avoid alcohol, caffeine, excessive fried food", "Regular meal times, avoid skipping meals"],
    "herbs": ["Amalaki (Emblica officinalis) - cooling, Vit C rich, balances Pitta", "Guduchi (Tinospora cordifolia) - immunomodulator, Pitta-shamaka", "Shatavari (Asparagus racemosus) - cooling, soothing for GI tract", "Yashtimadhu (Glycyrrhiza glabra) - demulcent for GI lining (use cautiously if BP issues)", "Neem (Azadirachta indica) - bitter, for skin issues"],
    "ayurvedic_medicines": ["Avipattikar Churna - classical formula for hyperacidity", "Kamadudha Rasa (with Mukta) - cooling antacid formulation", "Chandanasava - cooling formulation, helpful for burning sensations", "Sutshekhar Rasa - often used for Pitta conditions including GI issues"],
    "therapies": ["Virechana (therapeutic purgation) - primary Pitta detoxification (under guidance)", "Cooling oil application (e.g., Chandanadi Taila, Coconut oil)", "Shirodhara with cooling liquids (e.g., milk, buttermilk)"],
    "lifestyle": ["Avoid excessive heat and sun exposure", "Moderate exercise, avoid overheating", "Practice stress-reducing techniques (meditation, calming pranayama like Sheetali)", "Spend time in nature, near water", "Moonlight walks"]
}
}
"""
    
    def _get_base_prompt_template(self) -> str:
        """Get the base prompt template."""
        return """You are an expert Ayurvedic physician with deep knowledge of traditional Ayurvedic principles, including the Tridosha theory (Vata, Pitta, Kapha), the seven Dhatus (tissues), and the various Srotas (channels).

Your task is to analyze patient symptoms and provide a comprehensive Ayurvedic diagnosis with treatment recommendations.

{context}

Please analyze the following patient symptoms and provide your assessment in the exact JSON format shown in the examples below:

Patient Symptoms: "{symptoms}"

Provide your analysis in the following JSON structure:
{{
    "dominant_dosha": "Vata/Pitta/Kapha",
    "imbalances": ["specific imbalances identified"],
    "diagnosis": "Ayurvedic diagnosis name",
    "supporting_evidence": {{
        "symptoms_matching_dosha": ["list of symptoms that match the dosha"],
        "pulse_indication": "likely pulse characteristics",
        "tongue_indication": "likely tongue characteristics"
    }},
    "recommended_treatments": {{
        "dietary": ["dietary recommendations"],
        "herbs": ["herbal recommendations with scientific names"],
        "ayurvedic_medicines": ["classical Ayurvedic formulations"],
        "therapies": ["therapeutic recommendations"],
        "lifestyle": ["lifestyle recommendations"]
    }}
}}

Important guidelines:
1. Base your analysis on traditional Ayurvedic principles
2. Use the provided context from Ayurvedic texts when relevant
3. Be specific about dosha imbalances and their locations
4. Provide evidence-based recommendations
5. Include both Sanskrit and English terms where appropriate
6. Ensure all recommendations are safe and practical
7. Format the response as valid JSON only, without any additional text or markdown formatting

Examples of the expected format:
{few_shot_examples}
"""
    
    def create_diagnostic_prompt(self, symptoms: str, context: str = "") -> str:
        """
        Create a diagnostic prompt with symptoms and context.
        
        Args:
            symptoms: Patient symptoms
            context: Retrieved context from knowledge base
            
        Returns:
            Formatted prompt string
        """
        # Format context if provided
        if context:
            formatted_context = f"Relevant Ayurvedic knowledge:\n{context}\n\n"
        else:
            formatted_context = ""
        
        # Create the prompt
        prompt = self.base_prompt_template.format(
            context=formatted_context,
            symptoms=symptoms,
            few_shot_examples=self.few_shot_examples
        )
        
        return prompt
    
    def create_simple_prompt(self, symptoms: str) -> str:
        """
        Create a simple diagnostic prompt without RAG context.
        
        Args:
            symptoms: Patient symptoms
            
        Returns:
            Formatted prompt string
        """
        return f"""You are an expert Ayurvedic physician. Analyze the following symptoms and provide a diagnosis in JSON format:

Patient Symptoms: "{symptoms}"

Provide your analysis in JSON format following the structure from the examples above."""
    
    def get_prompt_variations(self) -> Dict[str, str]:
        """Get different prompt variations for testing."""
        return {
            "detailed": self.base_prompt_template,
            "simple": "Analyze these symptoms: {symptoms}",
            "clinical": "As a clinical Ayurvedic practitioner, diagnose: {symptoms}",
            "research": "Based on Ayurvedic research, analyze: {symptoms}"
        }
    
    def validate_prompt(self, prompt: str) -> bool:
        """
        Validate that a prompt contains required elements.
        
        Args:
            prompt: Prompt to validate
            
        Returns:
            True if valid, False otherwise
        """
        required_elements = [
            "Ayurvedic",
            "symptoms",
            "JSON",
            "dosha"
        ]
        
        prompt_lower = prompt.lower()
        for element in required_elements:
            if element not in prompt_lower:
                logger.warning(f"Prompt missing required element: {element}")
                return False
        
        return True 