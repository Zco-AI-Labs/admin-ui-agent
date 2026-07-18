from app.scripts._helpers import queue_admin_widget
from app.core import hubscape_adk

@hubscape_adk.require_tool_privilege
@hubscape_adk.tool_scope(["org"])
async def open_org_billing() -> str:
    """Opens the Organization Billing panel to manage subscription plans, credit card, and invoices."""
    return await queue_admin_widget("org_billing", "org.billing.manage")
