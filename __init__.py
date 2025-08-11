"""
Orchestrator package for the AI portfolio assistant.

This package defines the FastAPI application with a CrewAI‑based
orchestrator and stubbed agents/tools.  The orchestrator can be run
locally or deployed to a service such as Google Cloud Run.  It exposes
an HTTP endpoint that triggers a multi‑agent process to build a
comprehensive investment brief.

The module structure is intentionally simple so that you can replace
stub implementations with real data sources when you're ready.  See
README.md in this directory for usage and deployment details.
"""

__all__ = ["main", "agents", "tools"]