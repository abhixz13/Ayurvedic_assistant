#!/usr/bin/env python3
"""
Quick script to rebuild vector store from documents.
"""

import sys
sys.path.append('src')

from data_processing.document_loader import DocumentLoader
from data_processing.text_chunker import TextChunker
from rag.vector_store import VectorStore
from utils.helpers import setup_logging

def rebuild_vector_store():
    """Rebuild vector store from documents."""
    print("🔧 Rebuilding Vector Store")
    print("=" * 40)
    
    setup_logging('INFO')
    
    # Load documents
    print("📚 Loading documents...")
    loader = DocumentLoader()
    documents = loader.load_documents_from_directory("data/raw")
    print(f"✅ Loaded {len(documents)} documents")
    
    # Chunk documents
    print("✂️  Chunking documents...")
    chunker = TextChunker()
    chunks = chunker.chunk_documents(documents)
    print(f"✅ Created {len(chunks)} chunks")
    
    # Build vector store
    print("🗄️  Building vector store...")
    vector_store = VectorStore()
    success = vector_store.add_documents(chunks)
    
    if success:
        print("✅ Vector store built successfully")
        
        # Save vector store
        if vector_store.save():
            print("✅ Vector store saved to disk")
        else:
            print("❌ Failed to save vector store")
    else:
        print("❌ Failed to build vector store")
    
    return success

if __name__ == "__main__":
    rebuild_vector_store() 