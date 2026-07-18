from app.scripts._helpers import queue_admin_widget
from app.core import hubscape_adk

@hubscape_adk.require_tool_privilege
@hubscape_adk.tool_scope(["hub"])
async def open_hub_discovery() -> str:
    """Opens the Hub Discovery panel to view or edit search and visibility settings."""
    return await queue_admin_widget("hub_discovery", "hub.discovery.edit")
