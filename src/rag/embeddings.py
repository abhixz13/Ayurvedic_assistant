"""
Embedding management for RAG implementation.
"""

import logging
import torch
from typing import List, Dict, Any, Optional
from sentence_transformers import SentenceTransformer
from langchain_community.embeddings import HuggingFaceEmbeddings
from src.config.settings import settings

logger = logging.getLogger(__name__)


class EmbeddingManager:
    """Manage text embeddings for vector storage and retrieval."""
    
    def __init__(self, model_name: str = None, use_gpu: bool = None):
        """
        Initialize embedding manager.
        
        Args:
            model_name: Name of the embedding model
            use_gpu: Whether to use GPU for embeddings
        """
        self.model_name = model_name or settings.embedding_model
        self.use_gpu = use_gpu if use_gpu is not None else settings.use_gpu
        
        # Check GPU availability
        self.device = "cuda" if self.use_gpu and torch.cuda.is_available() else "cpu"
        
        logger.info(f"Initializing embedding model: {self.model_name} on {self.device}")
        
        try:
            # Initialize the embedding model
            self.model = SentenceTransformer(self.model_name, device=self.device)
            self.embedding_dimension = self.model.get_sentence_embedding_dimension()
            
            # Initialize LangChain embeddings wrapper
            self.langchain_embeddings = HuggingFaceEmbeddings(
                model_name=self.model_name,
                model_kwargs={'device': self.device}
            )
            
            logger.info(f"Embedding model initialized successfully. Dimension: {self.embedding_dimension}")
            
        except Exception as e:
            logger.error(f"Error initializing embedding model: {e}")
            raise
    
    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for a list of texts.
        
        Args:
            texts: List of text strings
            
        Returns:
            List of embedding vectors
        """
        try:
            embeddings = self.model.encode(texts, convert_to_tensor=False)
            return embeddings.tolist()
        except Exception as e:
            logger.error(f"Error generating embeddings: {e}")
            raise
    
    def generate_embedding(self, text: str) -> List[float]:
        """
        Generate embedding for a single text.
        
        Args:
            text: Text string
            
        Returns:
            Embedding vector
        """
        try:
            embedding = self.model.encode([text], convert_to_tensor=False)
            return embedding[0].tolist()
        except Exception as e:
            logger.error(f"Error generating embedding: {e}")
            raise
    
    def get_embedding_dimension(self) -> int:
        """Get the dimension of the embedding vectors."""
        return self.embedding_dimension
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the embedding model."""
        return {
            "model_name": self.model_name,
            "embedding_dimension": self.embedding_dimension,
            "device": self.device,
            "use_gpu": self.use_gpu,
            "gpu_available": torch.cuda.is_available() if self.use_gpu else False
        }
    
    def batch_generate_embeddings(self, texts: List[str], 
                                 batch_size: int = 32) -> List[List[float]]:
        """
        Generate embeddings in batches for large datasets.
        
        Args:
            texts: List of text strings
            batch_size: Size of each batch
            
        Returns:
            List of embedding vectors
        """
        all_embeddings = []
        
        for i in range(0, len(texts), batch_size):
            batch_texts = texts[i:i + batch_size]
            try:
                batch_embeddings = self.generate_embeddings(batch_texts)
                all_embeddings.extend(batch_embeddings)
                logger.info(f"Processed batch {i//batch_size + 1}/{(len(texts) + batch_size - 1)//batch_size}")
            except Exception as e:
                logger.error(f"Error processing batch {i//batch_size + 1}: {e}")
                # Add zero embeddings for failed batch
                all_embeddings.extend([[0.0] * self.embedding_dimension] * len(batch_texts))
        
        return all_embeddings
    
    def similarity(self, embedding1: List[float], embedding2: List[float]) -> float:
        """
        Calculate cosine similarity between two embeddings.
        
        Args:
            embedding1: First embedding vector
            embedding2: Second embedding vector
            
        Returns:
            Similarity score between 0 and 1
        """
        try:
            import numpy as np
            from sklearn.metrics.pairwise import cosine_similarity
            
            # Convert to numpy arrays
            emb1 = np.array(embedding1).reshape(1, -1)
            emb2 = np.array(embedding2).reshape(1, -1)
            
            # Calculate cosine similarity
            similarity = cosine_similarity(emb1, emb2)[0][0]
            return float(similarity)
            
        except Exception as e:
            logger.error(f"Error calculating similarity: {e}")
            return 0.0
    
    def find_most_similar(self, query_embedding: List[float], 
                         candidate_embeddings: List[List[float]], 
                         top_k: int = 5) -> List[tuple]:
        """
        Find the most similar embeddings to a query embedding.
        
        Args:
            query_embedding: Query embedding vector
            candidate_embeddings: List of candidate embedding vectors
            top_k: Number of top similar embeddings to return
            
        Returns:
            List of (index, similarity_score) tuples
        """
        try:
            similarities = []
            for i, candidate_emb in enumerate(candidate_embeddings):
                similarity = self.similarity(query_embedding, candidate_emb)
                similarities.append((i, similarity))
            
            # Sort by similarity (descending)
            similarities.sort(key=lambda x: x[1], reverse=True)
            
            return similarities[:top_k]
            
        except Exception as e:
            logger.error(f"Error finding most similar embeddings: {e}")
            return []
    
    def get_langchain_embeddings(self):
        """Get the LangChain embeddings wrapper."""
        return self.langchain_embeddings 