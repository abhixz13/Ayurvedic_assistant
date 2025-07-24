"""
Tests for RAG (Retrieval-Augmented Generation) components.
"""

import unittest
from unittest.mock import Mock, patch
from src.rag.embeddings import EmbeddingManager
from src.rag.vector_store import VectorStore
from src.rag.retriever import AyurvedicRetriever


class TestEmbeddingManager(unittest.TestCase):
    """Test cases for EmbeddingManager."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Mock sentence transformers
        with patch('src.rag.embeddings.SentenceTransformer'):
            with patch('src.rag.embeddings.HuggingFaceEmbeddings'):
                self.embedding_manager = EmbeddingManager()
    
    def test_generate_embedding(self):
        """Test single embedding generation."""
        # Mock the model
        mock_embedding = [0.1, 0.2, 0.3, 0.4, 0.5]
        mock_result = Mock()
        mock_result[0].tolist.return_value = mock_embedding
        self.embedding_manager.model.encode.return_value = mock_result
        
        result = self.embedding_manager.generate_embedding("test text")
        
        # Assertions
        self.assertEqual(result, mock_embedding)
        self.embedding_manager.model.encode.assert_called_once()
    
    def test_generate_embeddings_batch(self):
        """Test batch embedding generation."""
        # Mock the model
        mock_embeddings = [[0.1, 0.2], [0.3, 0.4]]
        self.embedding_manager.model.encode.return_value = Mock(tolist=lambda: mock_embeddings)
        
        texts = ["text1", "text2"]
        result = self.embedding_manager.generate_embeddings(texts)
        
        # Assertions
        self.assertEqual(result, mock_embeddings)
        self.embedding_manager.model.encode.assert_called_once_with(texts, convert_to_tensor=False)
    
    def test_similarity_calculation(self):
        """Test similarity calculation."""
        embedding1 = [1.0, 0.0, 0.0]
        embedding2 = [0.0, 1.0, 0.0]
        
        # Mock sklearn cosine similarity
        with patch('src.rag.embeddings.cosine_similarity') as mock_cosine:
            mock_cosine.return_value = [[0.5]]
            
            similarity = self.embedding_manager.similarity(embedding1, embedding2)
            
            # Assertions
            self.assertEqual(similarity, 0.5)
    
    def test_get_model_info(self):
        """Test getting model information."""
        info = self.embedding_manager.get_model_info()
        
        # Assertions
        self.assertIn("model_name", info)
        self.assertIn("embedding_dimension", info)
        self.assertIn("device", info)


class TestVectorStore(unittest.TestCase):
    """Test cases for VectorStore."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Mock dependencies
        with patch('src.rag.vector_store.EmbeddingManager'):
            with patch('src.rag.vector_store.FAISS'):
                self.vector_store = VectorStore()
    
    def test_add_documents(self):
        """Test adding documents to vector store."""
        chunks = [
            {
                "content": "Sample text 1",
                "metadata": {"source": "test1.txt"}
            },
            {
                "content": "Sample text 2", 
                "metadata": {"source": "test2.txt"}
            }
        ]
        
        # Mock embedding generation
        self.vector_store.embedding_manager.generate_embeddings.return_value = [
            [0.1, 0.2, 0.3], [0.4, 0.5, 0.6]
        ]
        
        # Mock FAISS index creation
        self.vector_store.faiss_index = Mock()
        
        result = self.vector_store.add_documents(chunks)
        
        # Assertions
        self.assertTrue(result)
        self.vector_store.embedding_manager.generate_embeddings.assert_called_once()
    
    def test_search_documents(self):
        """Test searching documents."""
        # Mock FAISS index
        mock_doc1 = Mock(page_content="Sample content 1", metadata={"source": "test1.txt"})
        mock_doc2 = Mock(page_content="Sample content 2", metadata={"source": "test2.txt"})
        
        self.vector_store.faiss_index = Mock()
        self.vector_store.faiss_index.similarity_search_with_score.return_value = [
            (mock_doc1, 0.8),
            (mock_doc2, 0.6)
        ]
        
        results = self.vector_store.search("test query")
        
        # Assertions
        self.assertEqual(len(results), 2)
        self.assertIn("content", results[0])
        self.assertIn("similarity_score", results[0])
    
    def test_save_and_load(self):
        """Test saving and loading vector store."""
        # Mock FAISS index
        self.vector_store.faiss_index = Mock()
        
        # Test save
        save_result = self.vector_store.save()
        self.assertTrue(save_result)
        self.vector_store.faiss_index.save_local.assert_called_once()
        
        # Test load
        with patch('src.rag.vector_store.FAISS.load_local'):
            load_result = self.vector_store.load()
            self.assertTrue(load_result)
    
    def test_get_statistics(self):
        """Test getting vector store statistics."""
        # Mock FAISS index
        mock_index = Mock()
        mock_index.ntotal = 100
        self.vector_store.faiss_index = mock_index
        
        stats = self.vector_store.get_statistics()
        
        # Assertions
        self.assertIn("total_documents", stats)
        self.assertEqual(stats["total_documents"], 100)


class TestAyurvedicRetriever(unittest.TestCase):
    """Test cases for AyurvedicRetriever."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Mock vector store
        self.mock_vector_store = Mock()
        self.retriever = AyurvedicRetriever(vector_store=self.mock_vector_store)
    
    def test_retrieve_documents(self):
        """Test document retrieval."""
        # Mock search results
        mock_results = [
            {
                "content": "Sample content 1",
                "metadata": {"source_file": "test1.txt"},
                "similarity_score": 0.8
            },
            {
                "content": "Sample content 2",
                "metadata": {"source_file": "test2.txt"},
                "similarity_score": 0.6
            }
        ]
        
        self.mock_vector_store.search.return_value = mock_results
        
        results = self.retriever.retrieve("test query")
        
        # Assertions
        self.assertEqual(len(results), 2)
        self.assertIn("content", results[0])
        self.assertIn("score", results[0])
        self.assertIn("source", results[0])
    
    def test_get_relevant_context(self):
        """Test getting relevant context."""
        # Mock search results
        mock_results = [
            {
                "content": "Sample content 1",
                "metadata": {"source_file": "test1.txt"},
                "similarity_score": 0.8
            }
        ]
        
        self.mock_vector_store.search.return_value = mock_results
        
        context = self.retriever.get_relevant_context("test query")
        
        # Assertions
        self.assertIn("Sample content 1", context)
        self.assertIn("test1.txt", context)
    
    def test_retrieve_with_filters(self):
        """Test retrieval with filters."""
        # Mock search results
        mock_results = [
            {
                "content": "Sample content 1",
                "metadata": {"source_file": "test1.txt"},
                "similarity_score": 0.8
            },
            {
                "content": "Sample content 2",
                "metadata": {"source_file": "test2.txt"},
                "similarity_score": 0.3
            }
        ]
        
        self.mock_vector_store.search.return_value = mock_results
        
        # Test with score filter
        filtered_results = self.retriever.retrieve_with_filters(
            "test query", min_score=0.5
        )
        
        # Assertions
        self.assertEqual(len(filtered_results), 1)  # Only one result above threshold
        self.assertEqual(filtered_results[0]["score"], 0.8)
    
    def test_get_retrieval_statistics(self):
        """Test getting retrieval statistics."""
        # Mock search results
        mock_results = [
            {
                "content": "Sample content 1",
                "metadata": {"source_file": "test1.txt"},
                "similarity_score": 0.8
            },
            {
                "content": "Sample content 2",
                "metadata": {"source_file": "test2.txt"},
                "similarity_score": 0.6
            }
        ]
        
        self.mock_vector_store.search.return_value = mock_results
        
        stats = self.retriever.get_retrieval_statistics("test query")
        
        # Assertions
        self.assertEqual(stats["total_results"], 2)
        self.assertEqual(stats["average_score"], 0.7)
        self.assertEqual(len(stats["sources"]), 2)
    
    def test_is_initialized(self):
        """Test initialization check."""
        # Test when initialized
        self.mock_vector_store.faiss_index = Mock()
        self.assertTrue(self.retriever.is_initialized())
        
        # Test when not initialized
        self.mock_vector_store.faiss_index = None
        self.assertFalse(self.retriever.is_initialized())


if __name__ == "__main__":
    unittest.main() 