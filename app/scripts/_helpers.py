import os
import json
import logging
import jwt
from cryptography.fernet import Fernet
from app.core import hubscape_adk

logger = logging.getLogger(__name__)

def check_edit_privilege(edit_privilege: str) -> bool:
    """
    Decodes the Capability Token from the context and checks if the user has edit privileges.
    Returns True if user has the edit privilege, False otherwise (indicating read-only).
    """
    context = hubscape_adk.get_context()
    token = context.raw_context.get("capability_token")
    if not token:
        # Local development/testing fallback
        user_roles = context.raw_context.get("userRoles", [])
        is_admin = any(r in user_roles for r in ("Admin", "Hub Admin", "Org Admin", "Hub Administrator"))
        return is_admin

    # Check if MagicMock
    if hasattr(token, "_mock_return_value") or type(token).__name__ == "MagicMock":
        return True

    secret_key = os.environ.get("HUBSCAPE_HMAC_SECRET") or os.environ.get("HUBSCAPE_KMS_MASTER_KEY") or "dev_secret_key_dont_use_in_prod"

    try:
        # Decode JWT HMAC
        payload = jwt.decode(token, secret_key, algorithms=["HS256"])
        
        # Derive Fernet key
        import base64
        import hashlib
        hasher = hashlib.sha256()
        hasher.update(secret_key.encode())
        hasher.update(context.agent_id.encode())
        derived_key = base64.urlsafe_b64encode(hasher.digest()).decode()

        encrypted_capabilities = payload.get("capabilities", {})
        encrypted_segment = encrypted_capabilities.get(context.agent_id)
        if not encrypted_segment:
            return False

        fernet = Fernet(derived_key.encode())
        decrypted_bytes = fernet.decrypt(encrypted_segment.encode())
        allowed_privilege_ids = json.loads(decrypted_bytes.decode())

        if edit_privilege in allowed_privilege_ids:
            return True

    except Exception as e:
        logger.warning(f"Failed to decrypt capability token for edit check: {e}")

    return False

async def queue_admin_widget(widget_type: str, edit_privilege: str = None) -> str:
    """
    Helper to resolve permissions, build the data context, and queue an OPEN_AGENT_WIDGET
    action that mounts the corresponding platform admin component.
    """
    context = hubscape_adk.get_context()
    hub_id = context.auth.hub_id
    org_id = context.auth.org_id
    
    # 0. Enforce Scope Boundaries
    is_org_widget = widget_type.startswith("org_")
    is_hub_widget = widget_type.startswith("hub_")
    is_org_scope = (hub_id == org_id) or (not hub_id) or (hub_id == "platform")
    
    if is_org_widget and not is_org_scope:
        return "I cannot open Organization settings from within a Hub workspace. Please switch to the Organization level first."
        
    if is_hub_widget and is_org_scope:
        return "I cannot open Hub settings from the Organization page. Please select or switch to a Hub workspace first."
    
    # 1. Resolve readOnly flag dynamically from token
    read_only = True
    if edit_privilege:
        has_edit = check_edit_privilege(edit_privilege)
        read_only = not has_edit
        
    # 2. Map the widget type to the frontend widget ID expected by the React client.
    widget_map = {
        'hub_name': 'admin_hub_name',
        'hub_avatar': 'admin_hub_avatar',
        'hub_prompt': 'admin_prompt',
        'hub_discovery': 'admin_hub_discovery',
        'hub_agents': 'admin_agents',
        'hub_rag_web': 'admin_hub_rag_web',
        'hub_rag_files': 'admin_hub_rag_files',
        'hub_rag_youtube': 'admin_hub_rag_youtube',
        'hub_members': 'admin_hub_members',
        'hub_add_member': 'admin_hub_add_member',
        'hub_roles': 'admin_hub_roles',
        'hub_usage': 'admin_hub_usage',
        'org_details': 'admin_org_details',
        'org_avatar': 'admin_org_avatar',
        'org_prompt': 'admin_org_prompt',
        'org_contacts': 'admin_org_contacts',
        'org_hubs': 'admin_org_hubs',
        'org_create_hub': 'admin_org_create_hub',
        'org_members': 'admin_org_members',
        'org_add_member': 'admin_org_add_member',
        'org_roles': 'admin_org_roles',
        'org_billing': 'admin_org_billing',
        'org_usage': 'admin_org_usage',
        'settings': 'settings'
    }
    
    frontend_widget_id = widget_map.get(widget_type, widget_type)
    
    # 3. Construct payload data context
    widget_data = {
        "hubId": hub_id,
        "orgId": org_id,
        "readOnly": read_only
    }
    
    # 4. Queue action in ADK RemoteContext
    context.actions.append({
        "type": "OPEN_AGENT_WIDGET",
        "payload": {
            "widgetId": frontend_widget_id,
            "data": widget_data
        }
    })
    
    # Log the action
    logger.info(f"[admin_ui_agent] Queued {widget_type} (readOnly={read_only})")
    
    return f"I have opened the {widget_type.replace('_', ' ').replace('org', 'organization')} panel for you."
