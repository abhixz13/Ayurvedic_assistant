"""
Retriever for fetching relevant Ayurvedic knowledge from vector store.
"""

import logging
from typing import List, Dict, Any, Optional
# FAISSRetriever is not available in current LangChain version
# Using vector store search directly instead
from src.rag.vector_store import VectorStore
from src.config.settings import settings

logger = logging.getLogger(__name__)


class AyurvedicRetriever:
    """Retriever for Ayurvedic knowledge base."""
    
    def __init__(self, vector_store: VectorStore = None):
        """
        Initialize Ayurvedic retriever.
        
        Args:
            vector_store: Vector store instance
        """
        self.vector_store = vector_store or VectorStore()
        self.retriever = None
        self._initialize_retriever()
    
    def _initialize_retriever(self):
        """Initialize the retriever (using vector store directly)."""
        try:
            if self.vector_store.faiss_index is not None:
                # Using vector store search directly instead of FAISSRetriever
                self.retriever = self.vector_store
                logger.info("Initialized retriever using vector store")
            else:
                logger.warning("Vector store is empty. Retriever not initialized.")
        except Exception as e:
            logger.error(f"Error initializing retriever: {e}")
    
    def retrieve(self, query: str, top_k: int = None) -> List[Dict[str, Any]]:
        """
        Retrieve relevant documents for a query.
        
        Args:
            query: Search query
            top_k: Number of top results to return
            
        Returns:
            List of retrieved documents with content and metadata
        """
        try:
            if self.retriever is None:
                logger.warning("Retriever not initialized. Please add documents to vector store first.")
                return []
            
            # Use vector store search directly for more control
            results = self.vector_store.search(query, top_k)
            
            # Format results for consistency
            formatted_results = []
            for result in results:
                formatted_result = {
                    "content": result["content"],
                    "metadata": result["metadata"],
                    "score": result["similarity_score"],
                    "source": result["metadata"].get("source_file", "unknown")
                }
                formatted_results.append(formatted_result)
            
            logger.info(f"Retrieved {len(formatted_results)} documents for query: {query[:50]}...")
            return formatted_results
            
        except Exception as e:
            logger.error(f"Error retrieving documents: {e}")
            return []
    
    def get_relevant_context(self, query: str, top_k: int = None) -> str:
        """
        Get relevant context as a formatted string.
        
        Args:
            query: Search query
            top_k: Number of top results to return
            
        Returns:
            Formatted context string
        """
        try:
            results = self.retrieve(query, top_k)
            
            if not results:
                return "No relevant context found."
            
            context_parts = []
            for i, result in enumerate(results, 1):
                source = result["source"]
                content = result["content"]
                score = result["score"]
                
                context_part = f"Document {i} (Source: {source}, Relevance: {score:.3f}):\n{content}\n"
                context_parts.append(context_part)
            
            return "\n".join(context_parts)
            
        except Exception as e:
            logger.error(f"Error getting relevant context: {e}")
            return "Error retrieving context."
    
    def retrieve_with_filters(self, query: str, 
                            source_filter: str = None,
                            min_score: float = 0.0,
                            top_k: int = None) -> List[Dict[str, Any]]:
        """
        Retrieve documents with additional filters.
        
        Args:
            query: Search query
            source_filter: Filter by source file name
            min_score: Minimum similarity score
            top_k: Number of top results to return
            
        Returns:
            List of filtered retrieved documents
        """
        try:
            results = self.retrieve(query, top_k)
            
            # Apply filters
            filtered_results = []
            for result in results:
                # Score filter
                if result["score"] < min_score:
                    continue
                
                # Source filter
                if source_filter and source_filter.lower() not in result["source"].lower():
                    continue
                
                filtered_results.append(result)
            
            logger.info(f"Filtered {len(results)} results to {len(filtered_results)} results")
            return filtered_results
            
        except Exception as e:
            logger.error(f"Error retrieving with filters: {e}")
            return []
    
    def get_retrieval_statistics(self, query: str) -> Dict[str, Any]:
        """
        Get statistics about retrieval performance.
        
        Args:
            query: Search query
            
        Returns:
            Dictionary with retrieval statistics
        """
        try:
            results = self.retrieve(query)
            
            if not results:
                return {
                    "query": query,
                    "total_results": 0,
                    "average_score": 0.0,
                    "score_range": (0.0, 0.0),
                    "sources": []
                }
            
            scores = [result["score"] for result in results]
            sources = list(set(result["source"] for result in results))
            
            return {
                "query": query,
                "total_results": len(results),
                "average_score": sum(scores) / len(scores),
                "score_range": (min(scores), max(scores)),
                "sources": sources,
                "unique_sources": len(sources)
            }
            
        except Exception as e:
            logger.error(f"Error getting retrieval statistics: {e}")
            return {
                "query": query,
                "error": str(e)
            }
    
    def is_initialized(self) -> bool:
        """Check if retriever is properly initialized."""
        return self.retriever is not None and self.vector_store.faiss_index is not None
    
    def get_vector_store_info(self) -> Dict[str, Any]:
        """Get information about the underlying vector store."""
        return self.vector_store.get_statistics() 