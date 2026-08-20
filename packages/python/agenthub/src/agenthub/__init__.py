"""Agent Hub — catalog SDK for skills, agents, rules, and prompts."""

from agenthub._auth import AccessKeyError
from agenthub._cache import ResourceCache, discover_cache_path
from agenthub._remote import DEFAULT_SOURCE, parse_github_source, resolve_install_source
from agenthub.catalog import Catalog, RagDocument, Resource, ResourceMeta
from agenthub.connect import mcp_config_stdio, mcp_config_http
from agenthub.install import InstallResult, install

__all__ = [
    "AccessKeyError",
    "Catalog",
    "ResourceCache",
    "discover_cache_path",
    "DEFAULT_SOURCE",
    "parse_github_source",
    "resolve_install_source",
    "Resource",
    "ResourceMeta",
    "RagDocument",
    "install",
    "InstallResult",
    "mcp_config_stdio",
    "mcp_config_http",
]

__version__ = "0.1.0"
