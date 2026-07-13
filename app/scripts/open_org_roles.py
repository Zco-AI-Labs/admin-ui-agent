from app.scripts._helpers import queue_admin_widget
from app.core import hubscape_adk

@hubscape_adk.require_tool_privilege
async def open_org_roles() -> str:
    """Opens the Organization Roles panel to configure organization roles and privileges."""
    return await queue_admin_widget("org_roles", "org.roles.edit")
