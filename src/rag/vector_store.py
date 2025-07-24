"""
Vector store for storing and retrieving document embeddings.
"""

import os
import pickle
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional
import faiss
import numpy as np
from langchain_community.vectorstores import FAISS
from langchain.schema import Document
from src.rag.embeddings import EmbeddingManager
from src.config.settings import settings

logger = logging.getLogger(__name__)


class VectorStore:
    """Vector store for storing and retrieving document embeddings."""
    
    def __init__(self, store_path: str = None, embedding_manager: EmbeddingManager = None):
        """
        Initialize vector store.
        
        Args:
            store_path: Path to store vector database
            embedding_manager: Embedding manager instance
        """
        self.store_path = store_path or settings.vector_store_path
        self.embedding_manager = embedding_manager or EmbeddingManager()
        
        # Create store directory if it doesn't exist
        Path(self.store_path).parent.mkdir(parents=True, exist_ok=True)
        
        self.faiss_index = None
        self.documents = []
        self.metadata = []
        
        logger.info(f"Initialized vector store at {self.store_path}")
    
    def add_documents(self, chunks: List[Dict[str, Any]]) -> bool:
        """
        Add document chunks to the vector store.
        
        Args:
            chunks: List of document chunks with content and metadata
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if not chunks:
                logger.warning("No chunks provided to add to vector store")
                return False
            
            # Extract texts and metadata
            texts = [chunk["content"] for chunk in chunks]
            metadatas = [chunk["metadata"] for chunk in chunks]
            
            # Generate embeddings
            logger.info(f"Generating embeddings for {len(texts)} chunks...")
            embeddings = self.embedding_manager.generate_embeddings(texts)
            
            # Create LangChain documents
            documents = [
                Document(page_content=text, metadata=metadata)
                for text, metadata in zip(texts, metadatas)
            ]
            
            # Create or update FAISS index
            if self.faiss_index is None:
                # Create new index
                embedding_dim = self.embedding_manager.get_embedding_dimension()
                self.faiss_index = FAISS.from_documents(
                    documents, 
                    self.embedding_manager.get_langchain_embeddings()
                )
                logger.info(f"Created new FAISS index with {len(documents)} documents")
            else:
                # Add to existing index
                self.faiss_index.add_documents(documents)
                logger.info(f"Added {len(documents)} documents to existing index")
            
            # Update internal tracking
            self.documents.extend(documents)
            self.metadata.extend(metadatas)
            
            return True
            
        except Exception as e:
            logger.error(f"Error adding documents to vector store: {e}")
            return False
    
    def search(self, query: str, top_k: int = None) -> List[Dict[str, Any]]:
        """
        Search for similar documents.
        
        Args:
            query: Search query
            top_k: Number of top results to return
            
        Returns:
            List of search results with content and metadata
        """
        try:
            if self.faiss_index is None:
                logger.warning("Vector store is empty. Please add documents first.")
                return []
            
            top_k = top_k or settings.top_k_retrieval
            
            # Perform similarity search
            results = self.faiss_index.similarity_search_with_score(query, k=top_k)
            
            # Format results
            formatted_results = []
            for doc, score in results:
                result = {
                    "content": doc.page_content,
                    "metadata": doc.metadata,
                    "similarity_score": float(score)
                }
                formatted_results.append(result)
            
            logger.info(f"Found {len(formatted_results)} results for query: {query[:50]}...")
            return formatted_results
            
        except Exception as e:
            logger.error(f"Error searching vector store: {e}")
            return []
    
    def save(self, path: str = None) -> bool:
        """
        Save the vector store to disk.
        
        Args:
            path: Path to save the vector store
            
        Returns:
            True if successful, False otherwise
        """
        try:
            save_path = path or self.store_path
            
            if self.faiss_index is not None:
                self.faiss_index.save_local(save_path)
                logger.info(f"Saved vector store to {save_path}")
                return True
            else:
                logger.warning("No vector store to save")
                return False
                
        except Exception as e:
            logger.error(f"Error saving vector store: {e}")
            return False
    
    def load(self, path: str = None) -> bool:
        """
        Load the vector store from disk.
        
        Args:
            path: Path to load the vector store from
            
        Returns:
            True if successful, False otherwise
        """
        try:
            load_path = path or self.store_path
            
            if os.path.exists(load_path):
                self.faiss_index = FAISS.load_local(
                    load_path, 
                    self.embedding_manager.get_langchain_embeddings(),
                    allow_dangerous_deserialization=True
                )
                logger.info(f"Loaded vector store from {load_path}")
                return True
            else:
                logger.warning(f"Vector store not found at {load_path}")
                return False
                
        except Exception as e:
            logger.error(f"Error loading vector store: {e}")
            return False
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get statistics about the vector store.
        
        Returns:
            Dictionary with vector store statistics
        """
        if self.faiss_index is None:
            return {
                "total_documents": 0,
                "embedding_dimension": self.embedding_manager.get_embedding_dimension(),
                "model_info": self.embedding_manager.get_model_info()
            }
        
        try:
            # Get index statistics
            index = self.faiss_index.index
            total_docs = index.ntotal if hasattr(index, 'ntotal') else len(self.documents)
            
            return {
                "total_documents": total_docs,
                "embedding_dimension": self.embedding_manager.get_embedding_dimension(),
                "model_info": self.embedding_manager.get_model_info(),
                "store_path": self.store_path
            }
            
        except Exception as e:
            logger.error(f"Error getting vector store statistics: {e}")
            return {
                "total_documents": len(self.documents),
                "embedding_dimension": self.embedding_manager.get_embedding_dimension(),
                "model_info": self.embedding_manager.get_model_info(),
                "error": str(e)
            }
    
    def clear(self):
        """Clear the vector store."""
        self.faiss_index = None
        self.documents = []
        self.metadata = []
        logger.info("Cleared vector store")
    
    def exists(self) -> bool:
        """Check if vector store exists on disk."""
        return os.path.exists(self.store_path)
    
    def get_document_count(self) -> int:
        """Get the number of documents in the vector store."""
        if self.faiss_index is None:
            return 0
        
        try:
            index = self.faiss_index.index
            return index.ntotal if hasattr(index, 'ntotal') else len(self.documents)
        except:
            return len(self.documents) 