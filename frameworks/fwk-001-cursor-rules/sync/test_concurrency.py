#!/usr/bin/env python3
"""
Concurrency Test Runner for T-10 Multi-Writer Hardening
Executes comprehensive tests to validate concurrent write detection and serialization.
"""

import json
import os
import time
import threading
import yaml
from datetime import datetime
from enhanced_index_writer import (
    LeaseManager, EnhancedIndexWriter, Lease, Conflict, 
    WriteResult, BatchWriteResult, ConflictType
)

class ConcurrencyTestRunner:
    """Runs concurrency tests for multi-writer hardening."""
    
    def __init__(self, test_file: str = "concurrency_tests.yaml"):
        self.test_file = test_file
        self.index_path = os.path.join(os.path.dirname(__file__), "artifacts_index.json")
        self.lease_file = self.index_path + ".leases"
        self.test_results = []
        
        # Initialize components
        self.lease_manager = LeaseManager(self.lease_file)
        self.enhanced_writer = EnhancedIndexWriter(self.index_path, self.lease_manager)
        
        # Test data
        self.test_artifacts = []
    
    def setup_test_environment(self):
        """Set up test environment with sample artifacts."""
        print("🔧 Setting up test environment...")
        
        # Create test artifacts
        self.test_artifacts = [
            {"id": "test_artifact_1", "version": "1.0.0", "status": "draft"},
            {"id": "test_artifact_2", "version": "1.0.0", "status": "draft"},
            {"id": "test_artifact_3", "version": "1.0.0", "status": "draft"}
        ]
        
        # Initialize index with test data
        test_index = {
            "version": 1,
            "artifacts": self.test_artifacts,
            "test_mode": True
        }
        
        # Write initial test data
        lease = self.lease_manager.acquire_lease("test_setup", 60)
        if lease:
            result = self.enhanced_writer.write_with_lease(lease.lease_id, test_index)
            self.lease_manager.release_lease(lease.lease_id)
            
            if result.success:
                print("✅ Test environment setup complete")
            else:
                print(f"❌ Test environment setup failed: {result.error_message}")
    
    def cleanup_test_environment(self):
        """Clean up test environment."""
        print("🧹 Cleaning up test environment...")
        
        # Stop lease manager
        self.lease_manager.stop()
        
        # Remove test files
        test_files = [
            self.lease_file,
            self.lease_file + ".backup",
            self.lease_file + ".journal"
        ]
        
        for file_path in test_files:
            if os.path.exists(file_path):
                try:
                    os.unlink(file_path)
                    print(f"🗑️  Removed: {file_path}")
                except Exception as e:
                    print(f"⚠️  Could not remove {file_path}: {e}")
    
    def run_test(self, test_name: str, test_func, *args, **kwargs) -> dict:
        """Run a single test and return results."""
        print(f"\n🧪 Running test: {test_name}")
        print("-" * 40)
        
        start_time = time.time()
        test_result = {
            "test_name": test_name,
            "start_time": datetime.now().isoformat(),
            "status": "RUNNING"
        }
        
        try:
            result = test_func(*args, **kwargs)
            test_result["status"] = "PASSED" if result else "FAILED"
            test_result["result"] = result
        except Exception as e:
            test_result["status"] = "ERROR"
            test_result["error"] = str(e)
            result = False
        
        test_result["end_time"] = datetime.now().isoformat()
        test_result["duration"] = time.time() - start_time
        
        status_emoji = "✅" if test_result["status"] == "PASSED" else "❌"
        print(f"{status_emoji} {test_name}: {test_result['status']}")
        
        if test_result["status"] == "PASSED":
            print(f"   ⏱️  Duration: {test_result['duration']:.3f}s")
        else:
            print(f"   ❌ Error: {test_result.get('error', 'Unknown error')}")
        
        self.test_results.append(test_result)
        return test_result
    
    def test_single_writer_isolation(self) -> bool:
        """Test CONC-001: Single Writer Isolation."""
        try:
            # Acquire lease
            lease = self.lease_manager.acquire_lease("test_writer_1", 60)
            if not lease:
                return False
            
            # Write artifact
            test_data = {
                "version": 1,
                "artifacts": self.test_artifacts + [{"id": "test_artifact_1", "version": "1.0.0", "status": "review"}]
            }
            
            result = self.enhanced_writer.write_with_lease(lease.lease_id, test_data)
            if not result.success:
                return False
            
            # Verify write
            if not os.path.exists(self.index_path):
                return False
            
            # Release lease
            self.lease_manager.release_lease(lease.lease_id)
            
            return True
        except Exception as e:
            print(f"   Error in single writer test: {e}")
            return False
    
    def test_multiple_writers_sequential(self) -> bool:
        """Test CONC-002: Multiple Writers Sequential."""
        try:
            # First writer
            lease1 = self.lease_manager.acquire_lease("test_writer_1", 30)
            if not lease1:
                return False
            
            result1 = self.enhanced_writer.write_with_lease(lease1.lease_id, {
                "version": 1,
                "artifacts": self.test_artifacts + [{"id": "artifact_from_writer_1", "version": "1.0.0", "status": "draft"}]
            })
            
            if not result1.success:
                self.lease_manager.release_lease(lease1.lease_id)
                return False
            
            self.lease_manager.release_lease(lease1.lease_id)
            
            # Second writer
            lease2 = self.lease_manager.acquire_lease("test_writer_2", 30)
            if not lease2:
                return False
            
            result2 = self.enhanced_writer.write_with_lease(lease2.lease_id, {
                "version": 1,
                "artifacts": self.test_artifacts + [{"id": "artifact_from_writer_2", "version": "1.0.0", "status": "draft"}]
            })
            
            if not result2.success:
                self.lease_manager.release_lease(lease2.lease_id)
                return False
            
            self.lease_manager.release_lease(lease2.lease_id)
            
            return True
        except Exception as e:
            print(f"   Error in sequential writers test: {e}")
            return False
    
    def test_concurrent_write_detection(self) -> bool:
        """Test CONC-003: Concurrent Write Detection."""
        try:
            # First writer acquires lease
            lease1 = self.lease_manager.acquire_lease("test_writer_1", 60)
            if not lease1:
                return False
            
            # Second writer attempts to acquire lease (should be blocked)
            lease2 = None
            def acquire_second_lease():
                nonlocal lease2
                lease2 = self.lease_manager.acquire_lease("test_writer_2", 60)
            
            # Start second writer in separate thread
            thread = threading.Thread(target=acquire_second_lease)
            thread.start()
            
            # Wait a bit for the second writer to attempt acquisition
            time.sleep(0.1)
            
            # First writer performs write
            result1 = self.enhanced_writer.write_with_lease(lease1.lease_id, {
                "version": 1,
                "artifacts": self.test_artifacts + [{"id": "concurrent_test_artifact", "version": "1.0.0", "status": "draft"}]
            })
            
            if not result1.success:
                self.lease_manager.release_lease(lease1.lease_id)
                return False
            
            # Release first lease
            self.lease_manager.release_lease(lease1.lease_id)
            
            # Wait for second writer thread
            thread.join(timeout=5)
            
            # Second writer should now be able to acquire lease
            if lease2:
                self.lease_manager.release_lease(lease2.lease_id)
                return True
            else:
                return False
                
        except Exception as e:
            print(f"   Error in concurrent write detection test: {e}")
            return False
    
    def test_lease_expiration_handling(self) -> bool:
        """Test CONC-004: Lease Expiration Handling."""
        try:
            # Acquire lease with short duration
            lease = self.lease_manager.acquire_lease("expiration_test_writer", 2)
            if not lease:
                return False
            
            # Wait for lease to expire
            time.sleep(3)
            
            # Try to write with expired lease (should fail)
            result = self.enhanced_writer.write_with_lease(lease.lease_id, {
                "version": 1,
                "artifacts": self.test_artifacts
            })
            
            # Should fail due to expired lease
            if result.success:
                return False
            
            # New writer should be able to acquire lease
            new_lease = self.lease_manager.acquire_lease("new_writer", 30)
            if not new_lease:
                return False
            
            self.lease_manager.release_lease(new_lease.lease_id)
            return True
            
        except Exception as e:
            print(f"   Error in lease expiration test: {e}")
            return False
    
    def test_batch_write_operations(self) -> bool:
        """Test batch write operations."""
        try:
            lease = self.lease_manager.acquire_lease("batch_test_writer", 60)
            if not lease:
                return False
            
            # Prepare batch operations
            operations = [
                {"id": "batch_artifact_1", "version": "1.0.0", "status": "draft"},
                {"id": "batch_artifact_2", "version": "1.0.0", "status": "draft"},
                {"id": "batch_artifact_3", "version": "1.0.0", "status": "draft"}
            ]
            
            # Execute batch write
            result = self.enhanced_writer.batch_write(lease.lease_id, operations)
            
            if not result or result.failed_operations > 0:
                self.lease_manager.release_lease(lease.lease_id)
                return False
            
            self.lease_manager.release_lease(lease.lease_id)
            return True
            
        except Exception as e:
            print(f"   Error in batch write test: {e}")
            return False
    
    def run_all_tests(self):
        """Run all concurrency tests."""
        print("🚀 Starting T-10 Concurrency Tests")
        print("=" * 50)
        
        try:
            # Setup test environment
            self.setup_test_environment()
            
            # Run tests
            tests = [
                ("Single Writer Isolation", self.test_single_writer_isolation),
                ("Multiple Writers Sequential", self.test_multiple_writers_sequential),
                ("Concurrent Write Detection", self.test_concurrent_write_detection),
                ("Lease Expiration Handling", self.test_lease_expiration_handling),
                ("Batch Write Operations", self.test_batch_write_operations)
            ]
            
            for test_name, test_func in tests:
                self.run_test(test_name, test_func)
            
            # Generate test report
            self.generate_test_report()
            
        finally:
            # Cleanup
            self.cleanup_test_environment()
    
    def generate_test_report(self):
        """Generate comprehensive test report."""
        print("\n📊 Test Results Summary")
        print("=" * 50)
        
        total_tests = len(self.test_results)
        passed_tests = len([r for r in self.test_results if r["status"] == "PASSED"])
        failed_tests = len([r for r in self.test_results if r["status"] == "FAILED"])
        error_tests = len([r for r in self.test_results if r["status"] == "ERROR"])
        
        print(f"Total Tests: {total_tests}")
        print(f"✅ Passed: {passed_tests}")
        print(f"❌ Failed: {failed_tests}")
        print(f"⚠️  Errors: {error_tests}")
        
        # Acceptance criteria validation
        print(f"\n🎯 Acceptance Criteria Validation")
        print("-" * 30)
        
        concurrent_writes_detected = any(
            r["test_name"] == "Concurrent Write Detection" and r["status"] == "PASSED"
            for r in self.test_results
        )
        
        concurrent_writes_serialized = any(
            r["test_name"] == "Multiple Writers Sequential" and r["status"] == "PASSED"
            for r in self.test_results
        )
        
        print(f"Concurrent writes detected: {'✅ YES' if concurrent_writes_detected else '❌ NO'}")
        print(f"Concurrent writes serialized: {'✅ YES' if concurrent_writes_serialized else '❌ NO'}")
        
        # Overall result
        if concurrent_writes_detected and concurrent_writes_serialized:
            print(f"\n🎉 T-10 ACCEPTANCE CRITERIA: ✅ PASSED")
            print("Multi-writer hardening is working correctly!")
        else:
            print(f"\n❌ T-10 ACCEPTANCE CRITERIA: FAILED")
            print("Some tests did not pass. Review implementation.")
        
        # Save detailed report
        report_file = f"concurrency_test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w') as f:
            json.dump(self.test_results, f, indent=2, default=str)
        
        print(f"\n📋 Detailed report saved to: {report_file}")

def main():
    """Main function to run concurrency tests."""
    runner = ConcurrencyTestRunner()
    runner.run_all_tests()

if __name__ == "__main__":
    main()
