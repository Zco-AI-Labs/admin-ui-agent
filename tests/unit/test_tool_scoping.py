import pytest
from app.core import hubscape_adk
from app.core.hubscape_adk import tool_scope, filter_tools_for_scope

def test_tool_scope_decorator_stores_scopes():
    # Define simple tools
    @tool_scope(["hub"])
    def hub_tool():
        pass
        
    @tool_scope(["org"])
    def org_tool():
        pass
        
    def global_tool():
        pass
        
    assert getattr(hub_tool, "_allowed_scopes") == ["hub"]
    assert getattr(org_tool, "_allowed_scopes") == ["org"]
    assert getattr(global_tool, "_allowed_scopes", None) is None


def test_tool_scope_stacked_with_privilege_decorator():
    # Verify __wrapped__ chain resolution
    @hubscape_adk.require_tool_privilege
    @tool_scope(["hub"])
    def stacked_tool():
        pass
        
    # Check if the wraps decorator keeps or passes it, or if filter_tools_for_scope finds it
    tools = [stacked_tool]
    filtered = filter_tools_for_scope(tools, hub_id="hub-123", org_id="org-123")
    assert len(filtered) == 1
    
    filtered_org = filter_tools_for_scope(tools, hub_id="org-123", org_id="org-123")
    assert len(filtered_org) == 0


def test_filter_tools_for_scope_logic():
    @tool_scope(["hub"])
    def hub_only():
        pass
        
    @tool_scope(["org"])
    def org_only():
        pass
        
    def global_tool():
        pass
        
    tools = [hub_only, org_only, global_tool]
    
    # Org Scope Cases
    # Case A: hub_id == org_id
    filtered_org_1 = filter_tools_for_scope(tools, hub_id="org-123", org_id="org-123")
    assert org_only in filtered_org_1
    assert global_tool in filtered_org_1
    assert hub_only not in filtered_org_1
    
    # Case B: hub_id is None
    filtered_org_2 = filter_tools_for_scope(tools, hub_id=None, org_id="org-123")
    assert org_only in filtered_org_2
    assert global_tool in filtered_org_2
    assert hub_only not in filtered_org_2
    
    # Case C: hub_id == "platform"
    filtered_org_3 = filter_tools_for_scope(tools, hub_id="platform", org_id="org-123")
    assert org_only in filtered_org_3
    assert global_tool in filtered_org_3
    assert hub_only not in filtered_org_3
    
    # Hub Scope Case: hub_id != org_id
    filtered_hub = filter_tools_for_scope(tools, hub_id="hub-123", org_id="org-123")
    assert hub_only in filtered_hub
    assert global_tool in filtered_hub
    assert org_only not in filtered_hub
