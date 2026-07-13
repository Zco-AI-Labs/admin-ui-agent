from app.scripts._helpers import queue_admin_widget
from app.core import hubscape_adk

@hubscape_adk.require_tool_privilege
async def open_org_usage() -> str:
    """Opens the Organization Usage analytics and limits panel."""
    return await queue_admin_widget("org_usage", None)
