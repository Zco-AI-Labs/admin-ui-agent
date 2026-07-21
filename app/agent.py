import os
# Force regional Vertex AI routing unconditionally
os.environ.pop("GOOGLE_GENAI_USE_ENTERPRISE", None)
os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "True"
os.environ.pop("GEMINI_API_KEY", None)
os.environ.pop("GOOGLE_API_KEY", None)
import asyncio
import importlib.util
import re
from google.adk import Agent as AdkAgent
from google.adk.runners import Runner
from google.genai import types

from app.core.load_local_tools import load_local_tools

# Statically import scripts and tools to ensure the Vertex AI packaging dependency analyzer bundles them in the cloud deployment
from app.scripts import (
    open_hub_add_member,
    open_hub_agents,
    open_hub_avatar,
    open_hub_discovery,
    open_hub_members,
    open_hub_name,
    open_hub_prompt,
    open_hub_rag_files,
    open_hub_rag_web,
    open_hub_rag_youtube,
    open_hub_roles,
    open_hub_usage,
    open_org_add_member,
    open_org_avatar,
    open_org_billing,
    open_org_contacts,
    open_org_create_hub,
    open_org_details,
    open_org_hubs,
    open_org_members,
    open_org_prompt,
    open_org_roles,
    open_org_usage,
)
from app.core.system_tools import (
    consultAgent,
    discover_agents,
)


# 1. Require SKILL.md as the Single Source of Truth for metadata (name, description) and instructions
runtime_dir = os.path.dirname(os.path.abspath(__file__))
skill_md_path = os.path.join(runtime_dir, "SKILL.md")
if not os.path.exists(skill_md_path):
    raise FileNotFoundError(f"Required agent definition file missing: {skill_md_path}")

with open(skill_md_path, "r", encoding="utf-8") as f:
    skill_content = f.read()

fm_match = re.match(r"^---\s*\n(.*?)\n---\s*\n", skill_content, flags=re.DOTALL)
if not fm_match:
    raise ValueError(f"SKILL.md is missing required YAML frontmatter header (--- ... ---): {skill_md_path}")

fm_text = fm_match.group(1)
name_m = re.search(r'^name:\s*["\']?([^"\'\n]+)["\']?', fm_text, re.MULTILINE)
if not name_m:
    raise ValueError(f"SKILL.md frontmatter is missing required 'name:' field: {skill_md_path}")

desc_m = re.search(r'^description:\s*["\']?([^"\'\n]+)["\']?', fm_text, re.MULTILINE)
if not desc_m:
    raise ValueError(f"SKILL.md frontmatter is missing required 'description:' field: {skill_md_path}")

agent_name = name_m.group(1).strip().replace('-', '_')
agent_description = desc_m.group(1).strip()
system_instruction = skill_content[fm_match.end():].strip()

scripts_dir = os.path.join(runtime_dir, "scripts")
system_tools_dir = os.path.join(runtime_dir, "core", "system_tools")
tools = load_local_tools(system_tools_dir) + load_local_tools(scripts_dir)

from app.app_utils.vertex_gemini import get_model

root_agent = AdkAgent(
    model=get_model("gemini-2.5-flash"),
    name=agent_name,
    description=agent_description,
    instruction=system_instruction,
    tools=tools
)

from app.core.geap_agent_wrapper import GEAPAgentWrapper

# Singleton instance used as the serialization target
agent_app = GEAPAgentWrapper(root_agent)

from google.adk.apps import App
app = App(
    root_agent=root_agent,
    name="app",
)
