from app.scripts._helpers import queue_admin_widget
from app.core import hubscape_adk

@hubscape_adk.require_tool_privilege
async def open_org_details() -> str:
    """Opens the Organization Details panel to view or edit organization information."""
    return await queue_admin_widget("org_details", "org.details.edit")
