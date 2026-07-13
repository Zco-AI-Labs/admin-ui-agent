from app.scripts._helpers import queue_admin_widget
from app.core import hubscape_adk

@hubscape_adk.require_tool_privilege
async def open_org_contacts() -> str:
    """Opens the Organization Contacts panel to view or edit contact details."""
    return await queue_admin_widget("org_contacts", "org.contacts.edit")
