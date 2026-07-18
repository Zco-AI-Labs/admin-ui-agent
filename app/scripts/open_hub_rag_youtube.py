from app.scripts._helpers import queue_admin_widget
from app.core import hubscape_adk

@hubscape_adk.require_tool_privilege
@hubscape_adk.tool_scope(["hub"])
async def open_hub_rag_youtube() -> str:
    """Opens the Hub YouTube RAG panel to view or ingest videos into the knowledge base."""
    return await queue_admin_widget("hub_rag_youtube", "hub.knowledge.edit")
