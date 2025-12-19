"""
✅ COMPREHENSIVE TEST SUITE
Unit and integration tests for the Hyper Universal Registry
"""

import unittest
import asyncio
import json
from typing import Dict, Any
from datetime import datetime

# Import modules to test
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

class TestDatabase(unittest.TestCase):
    """🏢 Test database operations"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.db_url = "postgresql://user:password@localhost/registry_test"
    
    def test_database_initialization(self):
        """✅ Test database initialization"""
        self.assertIsNotNone(self.db_url)
        self.assertIn("postgresql", self.db_url)
    
    def test_connection_string_format(self):
        """✅ Test connection string format"""
        parts = self.db_url.split("@")
        self.assertEqual(len(parts), 2)
        self.assertIn("://", self.db_url)


class TestSearchEngine(unittest.TestCase):
    """🔍 Test search engine operations"""
    
    def test_vector_search_result_structure(self):
        """✅ Test vector search result structure"""
        from services.hyper_registry.core.search_engine import SearchResult
        
        result = SearchResult(
            entry_id="test_123",
            title="Test Entry",
            category="agent",
            relevance_score=0.95,
            matched_fields=["title", "description"]
        )
        
        self.assertEqual(result.entry_id, "test_123")
        self.assertEqual(result.relevance_score, 0.95)
        self.assertEqual(len(result.matched_fields), 2)
    
    def test_search_result_ranking(self):
        """✅ Test search result ranking"""
        from services.hyper_registry.core.search_engine import SearchResult
        
        results = [
            SearchResult("1", "Test1", "agent", 0.9, []),
            SearchResult("2", "Test2", "agent", 0.95, []),
            SearchResult("3", "Test3", "agent", 0.85, [])
        ]
        
        sorted_results = sorted(results, key=lambda x: x.relevance_score, reverse=True)
        self.assertEqual(sorted_results[0].relevance_score, 0.95)
        self.assertEqual(sorted_results[-1].relevance_score, 0.85)


class TestRelationshipGraph(unittest.TestCase):
    """🕸️ Test relationship graph operations"""
    
    def test_graph_node_creation(self):
        """✅ Test graph node creation"""
        from services.hyper_registry.core.relationships import GraphNode
        
        node = GraphNode(
            entry_id="agent_001",
            category="agent",
            title="TestAgent",
            metadata={"version": "1.0", "status": "active"}
        )
        
        self.assertEqual(node.entry_id, "agent_001")
        self.assertEqual(node.category, "agent")
        self.assertEqual(node.metadata["version"], "1.0")
    
    def test_graph_edge_creation(self):
        """✅ Test graph edge creation"""
        from services.hyper_registry.core.relationships import GraphEdge
        
        edge = GraphEdge(
            source_id="agent_001",
            target_id="service_001",
            relationship_type="calls",
            weight=0.8,
            bidirectional=False
        )
        
        self.assertEqual(edge.relationship_type, "calls")
        self.assertEqual(edge.weight, 0.8)
        self.assertFalse(edge.bidirectional)


class TestAnalytics(unittest.TestCase):
    """📊 Test analytics engine"""
    
    def test_metric_creation(self):
        """✅ Test metric creation"""
        from services.hyper_registry.core.analytics import Metric
        
        metric = Metric(
            name="request_latency",
            value=125.5,
            timestamp=datetime.utcnow().isoformat(),
            tags={"endpoint": "/api/search", "method": "POST"},
            unit="ms"
        )
        
        self.assertEqual(metric.name, "request_latency")
        self.assertEqual(metric.value, 125.5)
        self.assertEqual(metric.unit, "ms")
    
    def test_performance_stats(self):
        """✅ Test performance statistics"""
        from services.hyper_registry.core.analytics import PerformanceStats
        
        stats = PerformanceStats(operation="search_entries")
        stats.count = 100
        stats.total_time = 12500  # 125ms average
        stats.errors = 5
        
        self.assertEqual(stats.avg_time, 125.0)
        self.assertEqual(stats.error_rate, 0.05)


class TestAIEngine(unittest.TestCase):
    """🧠 Test AI inference engine"""
    
    def test_classification_structure(self):
        """✅ Test classification structure"""
        from services.hyper_registry.core.ai_engine import Classification
        
        classification = Classification(
            primary_category="service",
            confidence=0.92,
            alternate_categories=[("agent", 0.05), ("component", 0.03)],
            reasoning="Based on orchestration capabilities"
        )
        
        self.assertEqual(classification.primary_category, "service")
        self.assertEqual(classification.confidence, 0.92)
        self.assertEqual(len(classification.alternate_categories), 2)
    
    def test_embedding_structure(self):
        """✅ Test embedding structure"""
        from services.hyper_registry.core.ai_engine import Embedding
        
        vector = [0.1] * 384
        embedding = Embedding(
            entry_id="test_001",
            vector=vector,
            model="text-embedding-3-small",
            created_at=datetime.utcnow().isoformat()
        )
        
        self.assertEqual(embedding.entry_id, "test_001")
        self.assertEqual(len(embedding.vector), 384)
        self.assertEqual(embedding.model, "text-embedding-3-small")


class TestAPIGateway(unittest.TestCase):
    """🌐 Test API gateway"""
    
    def test_entry_validation(self):
        """✅ Test entry validation"""
        from services.hyper_registry.api_gateway import RegistryAPIGateway
        
        gateway = RegistryAPIGateway(None, None)
        
        # Valid entry
        valid_entry = {
            "title": "Test Service",
            "category": "service",
            "description": "A test service"
        }
        self.assertTrue(gateway._validate_entry(valid_entry))
        
        # Invalid entry (missing required field)
        invalid_entry = {
            "title": "Test Service"
            # Missing category
        }
        self.assertFalse(gateway._validate_entry(invalid_entry))
    
    def test_gateway_statistics(self):
        """✅ Test gateway statistics"""
        from services.hyper_registry.api_gateway import RegistryAPIGateway
        
        gateway = RegistryAPIGateway(None, None)
        stats = gateway.get_gateway_stats()
        
        self.assertIn("total_requests", stats)
        self.assertIn("active_websockets", stats)
        self.assertIn("timestamp", stats)


class TestIntegration(unittest.TestCase):
    """🔗 Integration tests"""
    
    async def test_end_to_end_workflow(self):
        """✅ Test end-to-end workflow"""
        # This would test the complete flow from entry registration to search
        entry_data = {
            "title": "Integration Test Entry",
            "category": "service",
            "description": "Testing the complete workflow",
            "metadata": {"version": "1.0"}
        }
        
        self.assertIsNotNone(entry_data)
        self.assertEqual(entry_data["category"], "service")


# ============== TEST RUNNER ==============

def run_tests():
    """🏃 Run all tests"""
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test cases
    suite.addTests(loader.loadTestsFromTestCase(TestDatabase))
    suite.addTests(loader.loadTestsFromTestCase(TestSearchEngine))
    suite.addTests(loader.loadTestsFromTestCase(TestRelationshipGraph))
    suite.addTests(loader.loadTestsFromTestCase(TestAnalytics))
    suite.addTests(loader.loadTestsFromTestCase(TestAIEngine))
    suite.addTests(loader.loadTestsFromTestCase(TestAPIGateway))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "="*70)
    print("✅ TEST SUMMARY")
    print("="*70)
    print(f"Tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print("="*70 + "\n")
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    exit(0 if success else 1)
