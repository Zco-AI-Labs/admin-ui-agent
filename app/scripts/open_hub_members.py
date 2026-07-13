from app.scripts._helpers import queue_admin_widget
from app.core import hubscape_adk

@hubscape_adk.require_tool_privilege
async def open_hub_members() -> str:
    """Opens the Hub Members and staff list."""
    return await queue_admin_widget("hub_members", "hub.members.edit")
