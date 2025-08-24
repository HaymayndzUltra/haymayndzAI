#!/usr/bin/env python3
"""
Enhanced Snapshot CLI for T-06 Promotion Governance
Provides comprehensive snapshot management with metadata support.
"""

import argparse
import hashlib
import json
import os
import sys
import glob
import time
from datetime import datetime
from typing import Dict, List, Optional, Tuple

ROOT = os.path.dirname(__file__)
INDEX = os.path.abspath(os.path.join(ROOT, "..", "sync", "artifacts_index.json"))
SNAP_DIR = os.path.join(ROOT, "snapshots")
METADATA_DIR = os.path.join(ROOT, "metadata")

def sha256_bytes(b: bytes) -> str:
    """Generate SHA-256 digest of bytes."""
    return hashlib.sha256(b).hexdigest()

def ensure_directories():
    """Ensure required directories exist."""
    os.makedirs(SNAP_DIR, exist_ok=True)
    os.makedirs(METADATA_DIR, exist_ok=True)

def get_index_info() -> Dict:
    """Get current index information for metadata."""
    try:
        with open(INDEX, 'r') as f:
            data = json.load(f)
        return {
            'artifacts_count': len(data.get('artifacts', [])),
            'statuses': {},
            'kinds': set(),
            'framework': data.get('artifacts', [{}])[0].get('framework', 'unknown') if data.get('artifacts') else 'unknown'
        }
    except Exception as e:
        return {'error': str(e)}

def analyze_artifacts(data: Dict) -> Dict:
    """Analyze artifacts for metadata generation."""
    artifacts = data.get('artifacts', [])
    statuses = {}
    kinds = set()
    
    for artifact in artifacts:
        status = artifact.get('status', 'unknown')
        kind = artifact.get('kind', 'unknown')
        statuses[status] = statuses.get(status, 0) + 1
        kinds.add(kind)
    
    return {
        'statuses': statuses,
        'kinds': list(kinds)
    }

def create_metadata(digest: str, trigger: str = "manual", environment: str = "development") -> Dict:
    """Create comprehensive metadata for snapshot."""
    try:
        with open(INDEX, 'r') as f:
            index_data = json.load(f)
        
        artifact_analysis = analyze_artifacts(index_data)
        
        metadata = {
            "snapshot": {
                "digest": digest,
                "createdAt": datetime.utcnow().isoformat() + "Z",
                "creator": os.environ.get('USER', 'unknown'),
                "trigger": trigger,
                "environment": environment
            },
            "artifacts": {
                "count": len(index_data.get('artifacts', [])),
                "statuses": artifact_analysis['statuses'],
                "kinds": artifact_analysis['kinds']
            },
            "promotion": {
                "gate": "verification_gate",
                "checksum": sha256_bytes(json.dumps(index_data, sort_keys=True).encode()),
                "timestamp": datetime.utcnow().isoformat() + "Z"
            },
            "notes": f"Snapshot created via CLI - {trigger} trigger"
        }
        
        return metadata
    except Exception as e:
        return {"error": f"Failed to create metadata: {str(e)}"}

def create(args):
    """Create a new snapshot with metadata."""
    ensure_directories()
    
    try:
        # Read current index
        with open(INDEX, "rb") as f:
            data = f.read()
        
        # Generate digest
        digest = sha256_bytes(data)
        
        # Create snapshot file
        snapshot_path = os.path.join(SNAP_DIR, f"{digest}.json")
        with open(snapshot_path, "wb") as f:
            f.write(data)
        
        # Create metadata
        metadata = create_metadata(digest, args.trigger, args.environment)
        metadata_path = os.path.join(METADATA_DIR, f"{digest}.json")
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        print(f"✅ CREATED: {snapshot_path}")
        print(f"📋 METADATA: {metadata_path}")
        print(f"🔍 DIGEST: {digest}")
        
        return 0
    except Exception as e:
        print(f"❌ ERROR: Failed to create snapshot: {e}")
        return 1

def verify(args):
    """Verify all snapshots for integrity."""
    ok = True
    verified_count = 0
    total_count = 0
    
    print("🔍 Verifying snapshots...")
    
    for path in glob.glob(os.path.join(SNAP_DIR, "*.json")):
        total_count += 1
        try:
            with open(path, "rb") as f:
                b = f.read()
            
            filename = os.path.basename(path)
            expected_digest = os.path.splitext(filename)[0]
            actual_digest = sha256_bytes(b)
            
            if actual_digest == expected_digest:
                verified_count += 1
                print(f"  ✅ {filename}")
            else:
                ok = False
                print(f"  ❌ {filename} - DIGEST MISMATCH")
                print(f"     Expected: {expected_digest}")
                print(f"     Got:      {actual_digest}")
        except Exception as e:
            ok = False
            print(f"  ❌ {os.path.basename(path)} - ERROR: {e}")
    
    print(f"\n📊 Verification Results:")
    print(f"  Total snapshots: {total_count}")
    print(f"  Verified: {verified_count}")
    print(f"  Failed: {total_count - verified_count}")
    
    if ok:
        print("🎉 All snapshots verified successfully!")
    else:
        print("⚠️  Some snapshots failed verification!")
    
    return 0 if ok else 1

def lst(args):
    """List all snapshots with metadata."""
    print("📋 Available Snapshots:")
    print("-" * 80)
    
    snapshots = []
    for path in sorted(glob.glob(os.path.join(SNAP_DIR, "*.json"))):
        filename = os.path.basename(path)
        digest = os.path.splitext(filename)[0]
        
        # Get file info
        stat = os.stat(path)
        size = stat.st_size
        mtime = datetime.fromtimestamp(stat.st_mtime)
        
        # Try to get metadata
        metadata_path = os.path.join(METADATA_DIR, f"{digest}.json")
        metadata = {}
        if os.path.exists(metadata_path):
            try:
                with open(metadata_path, 'r') as f:
                    metadata = json.load(f)
            except:
                pass
        
        snapshots.append({
            'digest': digest,
            'path': path,
            'size': size,
            'mtime': mtime,
            'metadata': metadata
        })
    
    # Sort by modification time (newest first)
    snapshots.sort(key=lambda x: x['mtime'], reverse=True)
    
    for snapshot in snapshots:
        print(f"🔍 {snapshot['digest'][:16]}...")
        print(f"   📁 File: {os.path.basename(snapshot['path'])}")
        print(f"   📏 Size: {snapshot['size']} bytes")
        print(f"   🕒 Created: {snapshot['mtime'].strftime('%Y-%m-%d %H:%M:%S')}")
        
        if snapshot['metadata']:
            meta = snapshot['metadata']
            if 'snapshot' in meta:
                print(f"   👤 Creator: {meta['snapshot'].get('creator', 'unknown')}")
                print(f"   🎯 Trigger: {meta['snapshot'].get('trigger', 'unknown')}")
                print(f"   🌍 Environment: {meta['snapshot'].get('environment', 'unknown')}")
            
            if 'artifacts' in meta:
                print(f"   📦 Artifacts: {meta['artifacts'].get('count', 0)}")
        
        print()

def rollback(args):
    """Rollback to a specific snapshot."""
    target = os.path.join(SNAP_DIR, f"{args.digest}.json")
    
    if not os.path.exists(target):
        print(f"❌ Snapshot not found: {target}")
        return 1
    
    try:
        # Create backup of current index
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = f"{INDEX}.backup.{timestamp}"
        with open(INDEX, "rb") as f:
            backup_data = f.read()
        with open(backup_path, "wb") as f:
            f.write(backup_data)
        
        print(f"💾 Backup created: {backup_path}")
        
        # Restore from snapshot
        with open(target, "rb") as f:
            snapshot_data = f.read()
        with open(INDEX, "wb") as f:
            f.write(snapshot_data)
        
        print(f"✅ RESTORED index from {target}")
        print(f"🔍 Target digest: {args.digest}")
        
        return 0
    except Exception as e:
        print(f"❌ ERROR: Failed to rollback: {e}")
        return 1

def prune(args):
    """Prune old snapshots, keeping the specified number."""
    keep = int(args.keep)
    
    if keep < 1:
        print("❌ ERROR: Must keep at least 1 snapshot")
        return 1
    
    # Get all snapshots sorted by modification time (oldest first)
    snaps = sorted(glob.glob(os.path.join(SNAP_DIR, "*.json")), 
                   key=os.path.getmtime)
    
    if len(snaps) <= keep:
        print(f"ℹ️  Only {len(snaps)} snapshots exist, keeping all")
        return 0
    
    to_delete = snaps[:-keep]
    print(f"🗑️  Pruning {len(to_delete)} old snapshots, keeping {keep} newest...")
    
    deleted_count = 0
    for path in to_delete:
        try:
            # Delete snapshot
            os.unlink(path)
            
            # Delete corresponding metadata if it exists
            filename = os.path.basename(path)
            digest = os.path.splitext(filename)[0]
            metadata_path = os.path.join(METADATA_DIR, f"{digest}.json")
            if os.path.exists(metadata_path):
                os.unlink(metadata_path)
            
            print(f"  🗑️  DELETED: {filename}")
            deleted_count += 1
        except Exception as e:
            print(f"  ❌ Failed to delete {os.path.basename(path)}: {e}")
    
    print(f"✅ Pruning complete: {deleted_count} snapshots deleted")

def info(args):
    """Show detailed information about a specific snapshot."""
    target = os.path.join(SNAP_DIR, f"{args.digest}.json")
    
    if not os.path.exists(target):
        print(f"❌ Snapshot not found: {target}")
        return 1
    
    try:
        # Read snapshot data
        with open(target, 'r') as f:
            snapshot_data = json.load(f)
        
        # Get metadata
        metadata_path = os.path.join(METADATA_DIR, f"{args.digest}.json")
        metadata = {}
        if os.path.exists(metadata_path):
            with open(metadata_path, 'r') as f:
                metadata = json.load(f)
        
        print(f"🔍 Snapshot Information: {args.digest}")
        print("=" * 60)
        
        # File information
        stat = os.stat(target)
        print(f"📁 File: {os.path.basename(target)}")
        print(f"📏 Size: {stat.st_size} bytes")
        print(f"🕒 Modified: {datetime.fromtimestamp(stat.st_mtime)}")
        
        # Snapshot content
        print(f"\n📦 Content:")
        print(f"  Artifacts: {len(snapshot_data.get('artifacts', []))}")
        print(f"  Framework: {snapshot_data.get('artifacts', [{}])[0].get('framework', 'unknown')}")
        print(f"  Version: {snapshot_data.get('version', 'unknown')}")
        
        # Metadata
        if metadata:
            print(f"\n📋 Metadata:")
            if 'snapshot' in metadata:
                meta = metadata['snapshot']
                print(f"  Creator: {meta.get('creator', 'unknown')}")
                print(f"  Trigger: {meta.get('trigger', 'unknown')}")
                print(f"  Environment: {meta.get('environment', 'unknown')}")
                print(f"  Created: {meta.get('createdAt', 'unknown')}")
            
            if 'artifacts' in metadata:
                artifacts = metadata['artifacts']
                print(f"  Total Count: {artifacts.get('count', 0)}")
                if 'statuses' in artifacts:
                    print(f"  Statuses: {artifacts['statuses']}")
                if 'kinds' in artifacts:
                    print(f"  Kinds: {artifacts['kinds']}")
        
        return 0
    except Exception as e:
        print(f"❌ ERROR: Failed to read snapshot info: {e}")
        return 1

def main():
    """Main CLI entry point."""
    ap = argparse.ArgumentParser(
        description="Enhanced Snapshot CLI for T-06 Promotion Governance",
        epilog="Use --help with any subcommand for detailed options"
    )
    
    sub = ap.add_subparsers(dest="cmd", required=True)
    
    # Create command
    create_cmd = sub.add_parser("create", help="Create a new snapshot")
    create_cmd.add_argument("--trigger", default="manual", 
                           choices=["manual", "scheduled", "promotion", "emergency"],
                           help="Trigger for snapshot creation")
    create_cmd.add_argument("--environment", default="development",
                           choices=["development", "staging", "production"],
                           help="Environment context")
    create_cmd.set_defaults(func=create)
    
    # Verify command
    sub.add_parser("verify", help="Verify all snapshots for integrity").set_defaults(func=verify)
    
    # List command
    sub.add_parser("list", help="List all snapshots with metadata").set_defaults(func=lst)
    
    # Rollback command
    rollback_cmd = sub.add_parser("rollback", help="Rollback to a specific snapshot")
    rollback_cmd.add_argument("digest", help="SHA-256 digest of target snapshot")
    rollback_cmd.set_defaults(func=rollback)
    
    # Prune command
    prune_cmd = sub.add_parser("prune", help="Prune old snapshots")
    prune_cmd.add_argument("keep", type=int, help="Number of snapshots to keep")
    prune_cmd.set_defaults(func=prune)
    
    # Info command
    info_cmd = sub.add_parser("info", help="Show detailed snapshot information")
    info_cmd.add_argument("digest", help="SHA-256 digest of snapshot")
    info_cmd.set_defaults(func=info)
    
    args = ap.parse_args()
    
    try:
        code = args.func(args)
        if code is None:
            code = 0
        sys.exit(code)
    except KeyboardInterrupt:
        print("\n⚠️  Operation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()


