from app.scripts._helpers import queue_admin_widget
from app.core import hubscape_adk

@hubscape_adk.require_tool_privilege
async def open_hub_rag_web() -> str:
    """Opens the Hub Web RAG ingestion panel to add or manage website links."""
    return await queue_admin_widget("hub_rag_web", "hub.knowledge.edit")
