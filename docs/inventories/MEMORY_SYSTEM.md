## Folder: /memory_system

Purpose: Python-based subsystem for AI memory, MCP bridging, and CLI integrations.

Key modules:
- ai_cursor_intelligence.py: Core intelligence routines (331 lines).
- ai_cursor_plugin.py: Cursor plugin integration.
- mcp_bridge.py: Model Context Protocol bridge.
- cli.py: Command-line interface for memory operations.
- monitor.py, logger.py: Monitoring and logging utilities.
- domain/, interface/, services/, scripts/: Domain models, service layer, and helper scripts.

Integration Notes:
- Works with `/memory-bank` artifacts (state, session) and `/storage/memory` persisted KB indexes.
- Bridge components are referenced by `framework_memory_bridge.mdc` for synchronization.