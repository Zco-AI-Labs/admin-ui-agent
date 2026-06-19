import logging
from services.host_core.tools.impl.widgets import WidgetTools
import hubscape_adk

logger = logging.getLogger(__name__)

async def determine_widget(user_intent: str) -> dict:
    """Determines the correct admin panel to open based on the user's intent and hub/org context, then opens it directly.

    Args:
        user_intent: The user's query or intent describing what they want to manage.
    """
    context = hubscape_adk.get_context()
    user_intent_lower = user_intent.lower()
    hub_id = context.auth.hub_id
    org_id = context.auth.org_id

    logger.info(f"[admin_ui_agent] Resolving widget for intent: '{user_intent_lower}' | hub_id: {hub_id} | org_id: {org_id}")

    # 1. Determine if we are at ORG level
    is_org_context = False
    if hub_id:
        try:
            org_doc = context.db.collection('organizations').document(hub_id).get()
            if org_doc.exists:
                is_org_context = True
        except Exception as e:
            logger.warning(f"[admin_ui_agent] Failed to check org context: {e}")

    # 2. Map user intent to widget
    widget_type = None

    if is_org_context:
        if any(w in user_intent_lower for w in ['member', 'staff', 'invite', 'people', 'team', 'user']):
            widget_type = 'org_members'
        elif any(w in user_intent_lower for w in ['billing', 'payment', 'subscription', 'credit', 'invoice', 'financial', 'price', 'plan']):
            widget_type = 'org_billing'
        elif any(w in user_intent_lower for w in ['create hub', 'add hub', 'new hub']):
            widget_type = 'org_create_hub'
        elif any(w in user_intent_lower for w in ['hub', 'hubs', 'manage hubs']):
            widget_type = 'org_hubs'
        elif any(w in user_intent_lower for w in ['detail', 'info', 'address', 'phone', 'contact', 'name', 'general']):
            widget_type = 'org_contacts' if 'contact' in user_intent_lower else 'org_details'
        elif any(w in user_intent_lower for w in ['avatar', 'logo', 'profile image', 'picture', 'icon']):
            widget_type = 'org_avatar'
        elif any(w in user_intent_lower for w in ['prompt', 'personality', 'behavior', 'system prompt']):
            widget_type = 'org_prompt'
        elif any(w in user_intent_lower for w in ['role', 'privilege', 'permission']):
            widget_type = 'org_roles'
        elif any(w in user_intent_lower for w in ['usage', 'metric', 'statistic', 'analytic', 'limit']):
            widget_type = 'org_usage'
    else:
        if any(w in user_intent_lower for w in ['member', 'staff', 'invite', 'people', 'team', 'user']):
            widget_type = 'hub_add_member' if any(w in user_intent_lower for w in ['add', 'invite', 'create']) else 'hub_members'
        elif any(w in user_intent_lower for w in ['prompt', 'personality', 'behavior', 'system prompt', 'instruction']):
            widget_type = 'hub_prompt'
        elif any(w in user_intent_lower for w in ['agent', 'library', 'enable', 'disable', 'subagent']):
            widget_type = 'hub_agents'
        elif any(w in user_intent_lower for w in ['web', 'site', 'website', 'crawl', 'scrape', 'link']):
            widget_type = 'hub_rag_web'
        elif any(w in user_intent_lower for w in ['file', 'document', 'pdf', 'upload', 'text file']):
            widget_type = 'hub_rag_files'
        elif any(w in user_intent_lower for w in ['youtube', 'video', 'watch', 'play']):
            widget_type = 'hub_rag_youtube'
        elif any(w in user_intent_lower for w in ['avatar', 'logo', 'profile image', 'picture', 'icon']):
            widget_type = 'hub_avatar'
        elif any(w in user_intent_lower for w in ['name', 'detail', 'info', 'general']):
            widget_type = 'hub_name'
        elif any(w in user_intent_lower for w in ['role', 'privilege', 'permission']):
            widget_type = 'hub_roles'
        elif any(w in user_intent_lower for w in ['usage', 'metric', 'statistic', 'analytic', 'limit']):
            widget_type = 'hub_usage'
        elif any(w in user_intent_lower for w in ['discovery', 'find', 'explore']):
            widget_type = 'hub_discovery'

    if not widget_type:
        logger.warning(f"[admin_ui_agent] No matching widget for intent: '{user_intent_lower}'")
        return {
            "status": "error",
            "message": "I couldn't find an admin panel matching your request. Please check if you are in the correct context."
        }

    # 3. Build the context dict WidgetTools.open_admin_widget expects.
    hub_data_for_context = context.db.collection('organizations').document(org_id).collection('hubs').document(hub_id).get().to_dict() if (org_id and hub_id) else {}
    if hub_data_for_context and 'id' not in hub_data_for_context:
        hub_data_for_context['id'] = hub_id
    tool_context = {
        "hubId": hub_id,
        "userId": context.auth.get_user_id() if context.auth else None,
        "hubData": hub_data_for_context if hub_data_for_context else ({"orgId": org_id, "id": hub_id} if org_id else {})
    }

    widget_args = {
        "widgetType": widget_type,
        "confirmation_obtained": True
    }

    logger.info(f"[admin_ui_agent] Directly opening widget: '{widget_type}'")
    result = await WidgetTools.open_admin_widget(widget_args, tool_context)

    if "❌" in result.get("result", "") or "⛔" in result.get("result", ""):
        return {
            "status": "error",
            "message": result["result"]
        }

    return {
        "status": "success",
        "message": f"Opening the {widget_type.replace('_', ' ')} panel for you.",
        "system_action": result.get("system_action")
    }
