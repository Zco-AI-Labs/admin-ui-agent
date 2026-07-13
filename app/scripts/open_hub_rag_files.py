from app.scripts._helpers import queue_admin_widget
from app.core import hubscape_adk

@hubscape_adk.require_tool_privilege
async def open_hub_rag_files() -> str:
    """Opens the Hub File RAG panel to view, delete, or upload text and PDF documents."""
    return await queue_admin_widget("hub_rag_files", "hub.knowledge.edit")
