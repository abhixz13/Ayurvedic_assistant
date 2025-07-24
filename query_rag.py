#!/usr/bin/env python3
"""
Interactive RAG Query Tool
Test the RAG system with your own queries.
"""

import sys
import os

# Add src to path
sys.path.append('src')

def query_rag_system():
    """Interactive query tool for RAG system."""
    print("🔍 Ayurvedic RAG Query Tool")
    print("=" * 50)
    
    try:
        # Import required modules
        from rag.retriever import AyurvedicRetriever
        from rag.vector_store import VectorStore
        from utils.helpers import setup_logging
        
        # Setup logging
        setup_logging('INFO')
        
        print("📚 Loading vector store...")
        vector_store = VectorStore()
        
        # Check if vector store exists
        if not vector_store.exists():
            print("❌ Vector store not found. Please run the document processing first.")
            print("   Add documents to data/raw/ and run the system setup.")
            return False
        
        # Load existing vector store
        if not vector_store.load():
            print("❌ Failed to load vector store.")
            return False
        
        print("✅ Vector store loaded successfully")
        
        # Initialize retriever
        retriever = AyurvedicRetriever(vector_store)
        
        if not retriever.is_initialized():
            print("❌ Retriever not initialized. Vector store may be empty.")
            return False
        
        print("✅ Retriever initialized")
        
        # Get statistics
        stats = vector_store.get_statistics()
        print(f"📊 Vector store contains {stats['total_documents']} documents")
        
        print("\n🔍 Ready for queries! (Type 'quit' to exit)")
        print("-" * 50)
        
        while True:
            try:
                # Get user query
                query = input("\n❓ Enter your query: ").strip()
                
                if query.lower() in ['quit', 'exit', 'q']:
                    print("👋 Goodbye!")
                    break
                
                if not query:
                    print("⚠️  Please enter a query.")
                    continue
                
                # Get number of results
                try:
                    top_k = input("📊 Number of results (default 3): ").strip()
                    top_k = int(top_k) if top_k else 3
                except ValueError:
                    top_k = 3
                
                print(f"\n🔎 Searching for: '{query}'")
                print(f"📊 Retrieving top {top_k} results...")
                
                # Perform search
                results = retriever.retrieve(query, top_k=top_k)
                
                if results:
                    print(f"\n✅ Found {len(results)} relevant documents:")
                    print("-" * 60)
                    
                    for i, result in enumerate(results, 1):
                        score = result['score']
                        content = result['content']
                        source = result['source']
                        
                        print(f"\n📄 Result {i}:")
                        print(f"   📊 Relevance Score: {score:.3f}")
                        print(f"   📁 Source: {source}")
                        print(f"   📝 Content:")
                        
                        # Format content for better readability
                        lines = content.split('\n')
                        for line in lines[:10]:  # Show first 10 lines
                            if line.strip():
                                print(f"      {line}")
                        
                        if len(lines) > 10:
                            print(f"      ... ({len(lines) - 10} more lines)")
                        
                        print("-" * 40)
                    
                    # Show context summary
                    print(f"\n📋 Context Summary:")
                    context = retriever.get_relevant_context(query, top_k=min(2, len(results)))
                    print(f"   Length: {len(context)} characters")
                    print(f"   Preview: {context[:200]}...")
                    
                else:
                    print("❌ No relevant documents found.")
                    print("💡 Try different keywords or a broader query.")
                
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error processing query: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error initializing RAG system: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main function."""
    print("🚀 Ayurvedic RAG Query Tool")
    print("=" * 50)
    
    success = query_rag_system()
    
    if success:
        print("\n✅ Query tool completed successfully!")
    else:
        print("\n❌ Query tool failed. Check the errors above.")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 