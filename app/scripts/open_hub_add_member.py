from app.scripts._helpers import queue_admin_widget
from app.core import hubscape_adk

@hubscape_adk.require_tool_privilege
async def open_hub_add_member() -> str:
    """Opens the Hub Member Invite panel to add new members."""
    return await queue_admin_widget("hub_add_member", "hub.members.create")
