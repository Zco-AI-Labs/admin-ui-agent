from app.scripts._helpers import queue_admin_widget
from app.core import hubscape_adk

@hubscape_adk.require_tool_privilege
@hubscape_adk.tool_scope(["hub"])
async def open_hub_avatar() -> str:
    """Opens the Hub Avatar management panel to view or edit the hub's profile image."""
    return await queue_admin_widget("hub_avatar", "hub.avatar.edit")
