from app.scripts._helpers import queue_admin_widget
from app.core import hubscape_adk

@hubscape_adk.require_tool_privilege
async def open_hub_name() -> str:
    """Opens the Hub Name management panel to view or change the hub's name."""
    return await queue_admin_widget("hub_name", "hub.details.edit")
