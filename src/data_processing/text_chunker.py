"""
Text chunking utilities for RAG implementation.
"""

import re
import logging
from typing import List, Dict, Any
from langchain.text_splitter import RecursiveCharacterTextSplitter
from src.config.settings import settings

logger = logging.getLogger(__name__)


class TextChunker:
    """Split documents into chunks for vector storage and retrieval."""
    
    def __init__(self, chunk_size: int = None, chunk_overlap: int = None):
        """
        Initialize text chunker.
        
        Args:
            chunk_size: Size of each text chunk
            chunk_overlap: Overlap between consecutive chunks
        """
        self.chunk_size = chunk_size or settings.chunk_size
        self.chunk_overlap = chunk_overlap or settings.chunk_overlap
        
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", ". ", " ", ""]
        )
    
    def chunk_documents(self, documents: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Split documents into chunks.
        
        Args:
            documents: List of document dictionaries
            
        Returns:
            List of chunk dictionaries with metadata
        """
        chunks = []
        
        for doc in documents:
            try:
                doc_chunks = self._chunk_document(doc)
                chunks.extend(doc_chunks)
            except Exception as e:
                logger.error(f"Error chunking document {doc.get('file_name', 'unknown')}: {e}")
        
        logger.info(f"Created {len(chunks)} chunks from {len(documents)} documents")
        return chunks
    
    def _chunk_document(self, document: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Split a single document into chunks.
        
        Args:
            document: Document dictionary
            
        Returns:
            List of chunk dictionaries
        """
        content = document.get("content", "")
        if not content.strip():
            return []
        
        # Split text into chunks
        text_chunks = self.text_splitter.split_text(content)
        
        chunks = []
        for i, chunk_text in enumerate(text_chunks):
            if chunk_text.strip():
                chunk = {
                    "chunk_id": f"{document['file_name']}_chunk_{i}",
                    "content": chunk_text.strip(),
                    "metadata": {
                        "source_file": document["file_name"],
                        "file_path": document["file_path"],
                        "file_type": document["file_type"],
                        "chunk_index": i,
                        "total_chunks": len(text_chunks),
                        **document.get("metadata", {})
                    }
                }
                chunks.append(chunk)
        
        return chunks
    
    def chunk_text(self, text: str, metadata: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """
        Split a single text into chunks.
        
        Args:
            text: Text to split
            metadata: Optional metadata for chunks
            
        Returns:
            List of chunk dictionaries
        """
        if not text.strip():
            return []
        
        text_chunks = self.text_splitter.split_text(text)
        chunks = []
        
        for i, chunk_text in enumerate(text_chunks):
            if chunk_text.strip():
                chunk = {
                    "chunk_id": f"text_chunk_{i}",
                    "content": chunk_text.strip(),
                    "metadata": {
                        "chunk_index": i,
                        "total_chunks": len(text_chunks),
                        **(metadata or {})
                    }
                }
                chunks.append(chunk)
        
        return chunks
    
    def get_chunk_statistics(self, chunks: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Get statistics about created chunks.
        
        Args:
            chunks: List of chunk dictionaries
            
        Returns:
            Dictionary with chunk statistics
        """
        if not chunks:
            return {"total_chunks": 0, "average_chunk_length": 0}
        
        total_length = sum(len(chunk["content"]) for chunk in chunks)
        source_files = set(chunk["metadata"]["source_file"] for chunk in chunks)
        
        return {
            "total_chunks": len(chunks),
            "total_content_length": total_length,
            "average_chunk_length": total_length / len(chunks),
            "unique_source_files": len(source_files),
            "chunk_size": self.chunk_size,
            "chunk_overlap": self.chunk_overlap
        }
    
    def filter_chunks_by_length(self, chunks: List[Dict[str, Any]], 
                               min_length: int = 50, 
                               max_length: int = None) -> List[Dict[str, Any]]:
        """
        Filter chunks by content length.
        
        Args:
            chunks: List of chunk dictionaries
            min_length: Minimum chunk length
            max_length: Maximum chunk length
            
        Returns:
            Filtered list of chunks
        """
        filtered_chunks = []
        
        for chunk in chunks:
            content_length = len(chunk["content"])
            
            if content_length < min_length:
                continue
                
            if max_length and content_length > max_length:
                continue
                
            filtered_chunks.append(chunk)
        
        logger.info(f"Filtered {len(chunks)} chunks to {len(filtered_chunks)} chunks")
        return filtered_chunks
    
    def merge_small_chunks(self, chunks: List[Dict[str, Any]], 
                          min_length: int = 100) -> List[Dict[str, Any]]:
        """
        Merge small chunks with adjacent chunks.
        
        Args:
            chunks: List of chunk dictionaries
            min_length: Minimum length threshold
            
        Returns:
            List of merged chunks
        """
        if not chunks:
            return []
        
        merged_chunks = []
        current_chunk = chunks[0].copy()
        
        for i in range(1, len(chunks)):
            chunk = chunks[i]
            
            # Check if current chunk is too small and can be merged
            if (len(current_chunk["content"]) < min_length and 
                chunk["metadata"]["source_file"] == current_chunk["metadata"]["source_file"]):
                
                # Merge with next chunk
                current_chunk["content"] += "\n\n" + chunk["content"]
                current_chunk["metadata"]["total_chunks"] = chunk["metadata"]["total_chunks"]
            else:
                # Add current chunk to results and start new chunk
                merged_chunks.append(current_chunk)
                current_chunk = chunk.copy()
        
        # Add the last chunk
        merged_chunks.append(current_chunk)
        
        logger.info(f"Merged {len(chunks)} chunks to {len(merged_chunks)} chunks")
        return merged_chunks 