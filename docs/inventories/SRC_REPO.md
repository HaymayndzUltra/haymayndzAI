## Folder: /src/repo

Purpose: Core Python utilities used by the orchestration and memory tooling.

Files:
- atomic_io.py: Safe read/write operations with atomic semantics.
- auto_sync_manager.py: Synchronization workflow for artifacts and state.
- exec_logging.py: Execution logging helpers.
- tz_utils.py: Timezone utilities.
- __init__.py: Package marker.

Integration Notes:
- Utilities are invoked by tools under `/tools` and bridge components.