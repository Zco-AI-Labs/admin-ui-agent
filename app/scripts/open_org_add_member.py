from app.scripts._helpers import queue_admin_widget
from app.core import hubscape_adk

@hubscape_adk.require_tool_privilege
async def open_org_add_member() -> str:
    """Opens the Organization Member Invite panel to invite new users to the organization."""
    return await queue_admin_widget("org_add_member", "org.members.invite")
