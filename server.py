"""Test whether Copilot automatically follows MCP resource links.

Run: python server.py (stdio), or python server.py --http (Streamable HTTP).
"""
import json
import sys

from fastmcp import FastMCP
from catalog_store import ROWS, page

mcp = FastMCP("resource-link-e2e")
URI = "catalog://queries/all"


@mcp.tool()
def discover_catalog() -> dict:
    """EXPERIMENT: Return a resource URI, not catalog data. Ask the agent to read the linked MCP resource directly; do not use terminal commands. If unable, explain that limitation. Do not call the fallback unless asked to test it."""
    return {
        "message": "The catalog contains 1000 queries. Please read the MCP resource URI below using native MCP resource access, then identify the query for active checking accounts. Do not use terminal commands.",
        "resource_uri": URI,
        "total": len(ROWS),
        "target_hint": "The matching record is near the end of the catalog.",
    }


@mcp.resource(URI, mime_type="application/json")
def catalog_resource() -> str:
    """Full resource deliberately tests large-resource behavior; not a production response."""
    return json.dumps({"items": ROWS}, ensure_ascii=False)


@mcp.resource("catalog://queries/page/{offset}", mime_type="application/json")
def catalog_page_resource(offset: str) -> str:
    """Optional page resources; client must explicitly read them."""
    return json.dumps(page(int(offset)), ensure_ascii=False)


@mcp.tool()
def read_catalog_page(offset: int = 0, max_bytes: int = 4096) -> dict:
    """FALLBACK: retrieve a byte-limited catalog page if the client cannot read MCP resources automatically."""
    return page(offset, max_bytes)


if __name__ == "__main__":
    if "--http" in sys.argv:
        mcp.run(transport="http", host="127.0.0.1", port=8000)
    else:
        mcp.run()
