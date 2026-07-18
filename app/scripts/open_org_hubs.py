from app.scripts._helpers import queue_admin_widget
from app.core import hubscape_adk

@hubscape_adk.require_tool_privilege
@hubscape_adk.tool_scope(["org"])
async def open_org_hubs() -> str:
    """Opens the Organization Hubs management panel to view active hub workspaces."""
    return await queue_admin_widget("org_hubs", "org.hubs.create")
