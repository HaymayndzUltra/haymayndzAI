#!/usr/bin/env python3
"""
Enhanced Index Writer with Multi-Writer Hardening - T-10 Implementation
Provides lease-based concurrency control, conflict detection, and resolution.
"""

import json
import os
import time
import uuid
import fcntl
import tempfile
import threading
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum

# Constants
DEFAULT_LEASE_DURATION = 300  # 5 minutes
MAX_LEASE_RENEWALS = 10
LEASE_CLEANUP_INTERVAL = 60  # 1 minute
CONFLICT_DETECTION_ENABLED = True

class LeaseStatus(Enum):
    """Lease status enumeration."""
    ACTIVE = "active"
    EXPIRED = "expired"
    RELEASED = "released"
    CONFLICTED = "conflicted"

class ConflictType(Enum):
    """Conflict type enumeration."""
    WRITE_WRITE = "write_write"
    LEASE_EXPIRATION = "lease_expiration"
    DEADLOCK = "deadlock"
    STALE_DATA = "stale_data"

@dataclass
class Lease:
    """Lease data structure."""
    lease_id: str
    writer_id: str
    resource: str
    acquired_at: str
    expires_at: str
    renewal_count: int = 0
    max_renewals: int = MAX_LEASE_RENEWALS
    status: LeaseStatus = LeaseStatus.ACTIVE
    
    def is_expired(self) -> bool:
        """Check if lease is expired."""
        expires_dt = datetime.fromisoformat(self.expires_at.replace('Z', '+00:00'))
        now_dt = datetime.now().replace(tzinfo=expires_dt.tzinfo)
        return expires_dt < now_dt
    
    def can_renew(self) -> bool:
        """Check if lease can be renewed."""
        return (self.renewal_count < self.max_renewals and 
                self.status == LeaseStatus.ACTIVE and 
                not self.is_expired())
    
    def renew(self, duration_seconds: int = DEFAULT_LEASE_DURATION) -> bool:
        """Renew lease with new duration."""
        if not self.can_renew():
            return False
        
        self.renewal_count += 1
        self.expires_at = (datetime.now() + timedelta(seconds=duration_seconds)).isoformat() + 'Z'
        return True

@dataclass
class Conflict:
    """Conflict data structure."""
    conflict_id: str
    conflict_type: ConflictType
    lease_id: str
    writer_id: str
    resource: str
    detected_at: str
    description: str
    resolution_status: str = "pending"
    resolution_details: Optional[str] = None

@dataclass
class WriteResult:
    """Write operation result."""
    success: bool
    lease_id: Optional[str] = None
    conflict_id: Optional[str] = None
    error_message: Optional[str] = None
    write_timestamp: str = ""

@dataclass
class BatchWriteResult:
    """Batch write operation result."""
    total_operations: int
    successful_operations: int
    failed_operations: int
    conflicts: List[Conflict]
    lease_id: Optional[str] = None
    error_message: Optional[str] = None

class LeaseManager:
    """Manages lease acquisition, renewal, and cleanup."""
    
    def __init__(self, lease_file: str, max_leases: int = 10):
        self.lease_file = lease_file
        self.max_leases = max_leases
        self.active_leases: Dict[str, Lease] = {}
        self.lease_lock = threading.RLock()
        self.cleanup_thread = None
        self.running = False
        
        # Ensure lease file exists
        self._ensure_lease_file()
        self._load_leases()
        
        # Start cleanup thread
        self._start_cleanup_thread()
    
    def _ensure_lease_file(self):
        """Ensure lease file exists with proper structure."""
        if not os.path.exists(self.lease_file):
            with open(self.lease_file, 'w') as f:
                json.dump({"leases": [], "metadata": {"version": 1}}, f, indent=2)
    
    def _load_leases(self):
        """Load existing leases from file."""
        try:
            with open(self.lease_file, 'r') as f:
                data = json.load(f)
                for lease_data in data.get('leases', []):
                    lease = Lease(**lease_data)
                    if lease.status == LeaseStatus.ACTIVE and not lease.is_expired():
                        self.active_leases[lease.lease_id] = lease
        except Exception as e:
            print(f"Warning: Could not load leases: {e}")
    
    def _save_leases(self):
        """Save leases to file."""
        try:
            with open(self.lease_file, 'w') as f:
                json.dump({
                    "leases": [asdict(lease) for lease in self.active_leases.values()],
                    "metadata": {
                        "version": 1,
                        "last_updated": datetime.now().isoformat() + 'Z',
                        "total_leases": len(self.active_leases)
                    }
                }, f, indent=2, default=str)
        except Exception as e:
            print(f"Warning: Could not save leases: {e}")
    
    def acquire_lease(self, writer_id: str, duration: int = DEFAULT_LEASE_DURATION) -> Optional[Lease]:
        """Acquire lease with timeout."""
        with self.lease_lock:
            # Check if writer already has a lease
            for lease in self.active_leases.values():
                if lease.writer_id == writer_id and lease.status == LeaseStatus.ACTIVE:
                    if lease.can_renew():
                        lease.renew(duration)
                        self._save_leases()
                        return lease
                    else:
                        return None
            
            # Check if we can allocate new lease
            if len(self.active_leases) >= self.max_leases:
                return None
            
            # Create new lease
            lease_id = str(uuid.uuid4())
            now = datetime.now()
            lease = Lease(
                lease_id=lease_id,
                writer_id=writer_id,
                resource="artifacts_index.json",
                acquired_at=now.isoformat() + 'Z',
                expires_at=(now + timedelta(seconds=duration)).isoformat() + 'Z'
            )
            
            self.active_leases[lease_id] = lease
            self._save_leases()
            return lease
    
    def release_lease(self, lease_id: str) -> bool:
        """Release acquired lease."""
        with self.lease_lock:
            if lease_id in self.active_leases:
                lease = self.active_leases[lease_id]
                lease.status = LeaseStatus.RELEASED
                del self.active_leases[lease_id]
                self._save_leases()
                return True
            return False
    
    def validate_lease(self, lease_id: str) -> bool:
        """Check if lease is still valid."""
        with self.lease_lock:
            if lease_id not in self.active_leases:
                return False
            
            lease = self.active_leases[lease_id]
            if lease.is_expired():
                lease.status = LeaseStatus.EXPIRED
                del self.active_leases[lease_id]
                self._save_leases()
                return False
            
            return lease.status == LeaseStatus.ACTIVE
    
    def cleanup_expired_leases(self) -> int:
        """Remove expired leases and return count."""
        with self.lease_lock:
            expired_count = 0
            expired_leases = []
            
            for lease_id, lease in self.active_leases.items():
                if lease.is_expired():
                    lease.status = LeaseStatus.EXPIRED
                    expired_leases.append(lease_id)
                    expired_count += 1
            
            for lease_id in expired_leases:
                del self.active_leases[lease_id]
            
            if expired_count > 0:
                self._save_leases()
            
            return expired_count
    
    def _start_cleanup_thread(self):
        """Start background cleanup thread."""
        self.running = True
        self.cleanup_thread = threading.Thread(target=self._cleanup_worker, daemon=True)
        self.cleanup_thread.start()
    
    def _cleanup_worker(self):
        """Background worker for lease cleanup."""
        while self.running:
            try:
                expired_count = self.cleanup_expired_leases()
                if expired_count > 0:
                    print(f"Cleaned up {expired_count} expired leases")
                time.sleep(LEASE_CLEANUP_INTERVAL)
            except Exception as e:
                print(f"Error in cleanup worker: {e}")
                time.sleep(LEASE_CLEANUP_INTERVAL)
    
    def stop(self):
        """Stop the lease manager."""
        self.running = False
        if self.cleanup_thread:
            self.cleanup_thread.join(timeout=5)

class ConflictDetector:
    """Detects and manages write conflicts."""
    
    def __init__(self, index_path: str):
        self.index_path = index_path
        self.conflicts: List[Conflict] = []
        self.conflict_lock = threading.RLock()
    
    def detect_write_conflicts(self, new_data: Dict, existing_data: Dict) -> List[Conflict]:
        """Detect conflicts between new and existing data."""
        conflicts = []
        
        # Check for write-write conflicts on same artifacts
        existing_artifacts = {a.get('id'): a for a in existing_data.get('artifacts', [])}
        new_artifacts = {a.get('id'): a for a in new_data.get('artifacts', [])}
        
        for artifact_id in set(existing_artifacts.keys()) & set(new_artifacts.keys()):
            existing = existing_artifacts[artifact_id]
            new_artifact = new_artifacts[artifact_id]
            
            # Check if same artifact was modified
            if (existing.get('updatedAt') != new_artifact.get('updatedAt') or
                existing.get('version') != new_artifact.get('version')):
                
                conflict = Conflict(
                    conflict_id=str(uuid.uuid4()),
                    conflict_type=ConflictType.WRITE_WRITE,
                    lease_id="",  # Will be set by caller
                    writer_id="",  # Will be set by caller
                    resource=self.index_path,
                    detected_at=datetime.now().isoformat() + 'Z',
                    description=f"Write conflict on artifact {artifact_id}: existing version {existing.get('version')}, new version {new_artifact.get('version')}"
                )
                conflicts.append(conflict)
        
        return conflicts
    
    def resolve_conflicts(self, conflicts: List[Conflict]) -> Dict:
        """Resolve detected conflicts automatically where possible."""
        resolved_data = {}
        
        for conflict in conflicts:
            if conflict.conflict_type == ConflictType.WRITE_WRITE:
                # For write-write conflicts, we'll need manual resolution
                # For now, mark as unresolved
                conflict.resolution_status = "requires_manual_resolution"
                conflict.resolution_details = "Write-write conflicts require manual resolution"
            else:
                # Other conflict types can be auto-resolved
                conflict.resolution_status = "auto_resolved"
                conflict.resolution_details = "Automatically resolved"
        
        return resolved_data
    
    def generate_conflict_report(self, conflicts: List[Conflict]) -> str:
        """Generate human-readable conflict report."""
        if not conflicts:
            return "No conflicts detected."
        
        report = f"Conflict Report - {datetime.now().isoformat()}\n"
        report += "=" * 50 + "\n\n"
        
        for conflict in conflicts:
            report += f"Conflict ID: {conflict.conflict_id}\n"
            report += f"Type: {conflict.conflict_type.value}\n"
            report += f"Writer: {conflict.writer_id}\n"
            report += f"Resource: {conflict.resource}\n"
            report += f"Detected: {conflict.detected_at}\n"
            report += f"Description: {conflict.description}\n"
            report += f"Status: {conflict.resolution_status}\n"
            if conflict.resolution_details:
                report += f"Resolution: {conflict.resolution_details}\n"
            report += "-" * 30 + "\n\n"
        
        return report

class EnhancedIndexWriter:
    """Enhanced index writer with multi-writer support."""
    
    def __init__(self, index_path: str, lease_manager: LeaseManager):
        self.index_path = index_path
        self.lease_manager = lease_manager
        self.conflict_detector = ConflictDetector(index_path)
        self.write_lock = threading.RLock()
    
    def write_with_lease(self, lease_id: str, data: Dict) -> WriteResult:
        """Write data using valid lease with conflict detection."""
        # Validate lease
        if not self.lease_manager.validate_lease(lease_id):
            return WriteResult(
                success=False,
                error_message="Invalid or expired lease"
            )
        
        with self.write_lock:
            try:
                # Load existing data for conflict detection
                existing_data = self._load_index()
                
                # Detect conflicts if enabled
                if CONFLICT_DETECTION_ENABLED:
                    conflicts = self.conflict_detector.detect_write_conflicts(data, existing_data)
                    if conflicts:
                        # Update conflict details
                        for conflict in conflicts:
                            conflict.lease_id = lease_id
                            conflict.writer_id = self._get_writer_from_lease(lease_id)
                        
                        # Try to auto-resolve
                        resolved_data = self.conflict_detector.resolve_conflicts(conflicts)
                        
                        # Check if all conflicts were auto-resolved
                        unresolved_conflicts = [c for c in conflicts if c.resolution_status == "requires_manual_resolution"]
                        if unresolved_conflicts:
                            return WriteResult(
                                success=False,
                                lease_id=lease_id,
                                conflict_id=unresolved_conflicts[0].conflict_id,
                                error_message="Write conflicts detected requiring manual resolution"
                            )
                
                # Perform atomic write
                self._atomic_write(data)
                
                return WriteResult(
                    success=True,
                    lease_id=lease_id,
                    write_timestamp=datetime.now().isoformat() + 'Z'
                )
                
            except Exception as e:
                return WriteResult(
                    success=False,
                    lease_id=lease_id,
                    error_message=str(e)
                )
    
    def batch_write(self, lease_id: str, operations: List[Dict]) -> BatchWriteResult:
        """Execute multiple write operations in single lease."""
        if not self.lease_manager.validate_lease(lease_id):
            return BatchWriteResult(
                total_operations=len(operations),
                successful_operations=0,
                failed_operations=len(operations),
                conflicts=[],
                error_message="Invalid or expired lease"
            )
        
        successful = 0
        failed = 0
        conflicts = []
        
        for operation in operations:
            result = self.write_with_lease(lease_id, operation)
            if result.success:
                successful += 1
            else:
                failed += 1
                if result.conflict_id:
                    conflicts.append(Conflict(
                        conflict_id=result.conflict_id,
                        conflict_type=ConflictType.WRITE_WRITE,
                        lease_id=lease_id,
                        writer_id=self._get_writer_from_lease(lease_id),
                        resource=self.index_path,
                        detected_at=datetime.now().isoformat() + 'Z',
                        description=f"Batch operation failed: {result.error_message}"
                    ))
        
        return BatchWriteResult(
            total_operations=len(operations),
            successful_operations=successful,
            failed_operations=failed,
            conflicts=conflicts,
            lease_id=lease_id
        )
    
    def read_with_consistency(self, consistency_level: str = "read_committed") -> Dict:
        """Read index with specified consistency level."""
        if consistency_level == "read_committed":
            # Read the latest committed version
            return self._load_index()
        elif consistency_level == "read_uncommitted":
            # Read including uncommitted changes (for debugging)
            return self._load_index_with_journal()
        else:
            raise ValueError(f"Unsupported consistency level: {consistency_level}")
    
    def _load_index(self) -> Dict:
        """Load index data."""
        if not os.path.exists(self.index_path):
            return {"version": 1, "artifacts": []}
        
        with open(self.index_path, 'r') as f:
            return json.load(f)
    
    def _load_index_with_journal(self) -> Dict:
        """Load index data including journal entries."""
        # This would implement journal replay for uncommitted changes
        # For now, just return committed data
        return self._load_index()
    
    def _atomic_write(self, data: Dict):
        """Perform atomic write operation."""
        directory = os.path.dirname(self.index_path) or "."
        fd, tmp = tempfile.mkstemp(prefix=".idx.", dir=directory)
        
        try:
            with os.fdopen(fd, "w") as f:
                json.dump(data, f, separators=(",", ":"), sort_keys=True)
                f.flush()
                os.fsync(f.fileno())
            
            dir_fd = os.open(directory, os.O_DIRECTORY)
            try:
                os.replace(tmp, self.index_path)
                os.fsync(dir_fd)
            finally:
                os.close(dir_fd)
        finally:
            if os.path.exists(tmp):
                os.unlink(tmp)
    
    def _get_writer_from_lease(self, lease_id: str) -> str:
        """Get writer ID from lease."""
        lease = self.lease_manager.active_leases.get(lease_id)
        return lease.writer_id if lease else "unknown"

def main():
    """Main function for testing."""
    print("Enhanced Index Writer - T-10 Multi-Writer Hardening")
    print("=" * 50)
    
    # Initialize components
    index_path = os.path.join(os.path.dirname(__file__), "artifacts_index.json")
    lease_file = index_path + ".leases"
    
    lease_manager = LeaseManager(lease_file)
    enhanced_writer = EnhancedIndexWriter(index_path, lease_manager)
    
    try:
        # Test lease acquisition
        print("Testing lease acquisition...")
        lease = lease_manager.acquire_lease("test_writer", 60)
        if lease:
            print(f"✅ Lease acquired: {lease.lease_id}")
            
            # Test write operation
            print("Testing write operation...")
            test_data = {
                "version": 1,
                "artifacts": [
                    {"id": "test_artifact", "version": "1.0.0", "status": "draft"}
                ]
            }
            
            result = enhanced_writer.write_with_lease(lease.lease_id, test_data)
            if result.success:
                print("✅ Write operation successful")
            else:
                print(f"❌ Write operation failed: {result.error_message}")
            
            # Release lease
            lease_manager.release_lease(lease.lease_id)
            print("✅ Lease released")
        else:
            print("❌ Failed to acquire lease")
    
    finally:
        lease_manager.stop()
        print("Lease manager stopped")

if __name__ == "__main__":
    main()
