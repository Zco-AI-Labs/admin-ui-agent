from app.scripts._helpers import queue_admin_widget
from app.core import hubscape_adk

@hubscape_adk.require_tool_privilege
async def open_org_avatar() -> str:
    """Opens the Organization Avatar panel to view or edit the organization's logo."""
    return await queue_admin_widget("org_avatar", "org.avatar.edit")
