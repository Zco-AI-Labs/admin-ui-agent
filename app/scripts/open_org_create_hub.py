from app.scripts._helpers import queue_admin_widget
from app.core import hubscape_adk

@hubscape_adk.require_tool_privilege
@hubscape_adk.tool_scope(["org"])
async def open_org_create_hub() -> str:
    """Opens the Hub Creation panel to add a new hub workspace to the organization."""
    return await queue_admin_widget("org_create_hub", "org.hubs.create")
