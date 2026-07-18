from app.scripts._helpers import queue_admin_widget
from app.core import hubscape_adk

@hubscape_adk.require_tool_privilege
@hubscape_adk.tool_scope(["hub"])
async def open_hub_roles() -> str:
    """Opens the Hub Roles panel to view or configure hub-level roles and permissions."""
    return await queue_admin_widget("hub_roles", "hub.roles.edit")
