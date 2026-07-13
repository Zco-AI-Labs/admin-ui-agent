from app.scripts._helpers import queue_admin_widget
from app.core import hubscape_adk

@hubscape_adk.require_tool_privilege
async def open_org_members() -> str:
    """Opens the Organization Members panel to view organization members."""
    return await queue_admin_widget("org_members", "org.members.manage")
