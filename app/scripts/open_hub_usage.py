from app.scripts._helpers import queue_admin_widget
from app.core import hubscape_adk

@hubscape_adk.require_tool_privilege
@hubscape_adk.tool_scope(["hub"])
async def open_hub_usage() -> str:
    """Opens the Hub Usage panel to view consumption metrics, token counts, and analytics."""
    return await queue_admin_widget("hub_usage", None)
