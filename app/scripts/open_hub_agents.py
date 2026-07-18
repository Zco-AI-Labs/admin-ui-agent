from app.scripts._helpers import queue_admin_widget
from app.core import hubscape_adk

@hubscape_adk.require_tool_privilege
@hubscape_adk.tool_scope(["hub"])
async def open_hub_agents() -> str:
    """Opens the Hub Agents library to enable, disable, or configure subagents."""
    return await queue_admin_widget("hub_agents", "hub.agents.edit")
