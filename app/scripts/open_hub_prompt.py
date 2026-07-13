from app.scripts._helpers import queue_admin_widget
from app.core import hubscape_adk

@hubscape_adk.require_tool_privilege
async def open_hub_prompt() -> str:
    """Opens the Hub Prompt panel to view or edit the hub's system instruction/personality prompt."""
    return await queue_admin_widget("hub_prompt", "hub.prompt.edit")
