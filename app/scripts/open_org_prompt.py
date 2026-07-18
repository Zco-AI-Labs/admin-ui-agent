from app.scripts._helpers import queue_admin_widget
from app.core import hubscape_adk

@hubscape_adk.require_tool_privilege
@hubscape_adk.tool_scope(["org"])
async def open_org_prompt() -> str:
    """Opens the Organization Prompt panel to view or edit the organization's system instruction prompt."""
    return await queue_admin_widget("org_prompt", "org.prompt.edit")
