"""Small deterministic dataset and byte-limited pages for MCP resource experiments."""
import json

ROWS = [
    {"id": f"Q{i:04d}", "name": f"Query {i}", "description": f"Public metadata description for query {i}."}
    for i in range(1, 1001)
]
ROWS[-1] = {"id": "Q1000", "name": "Active checking accounts", "description": "Retrieve active checking accounts for a customer using customer identifier."}


def page(offset: int = 0, max_bytes: int = 4096) -> dict:
    if offset < 0 or offset > len(ROWS):
        raise ValueError("invalid offset")
    if not 256 <= max_bytes <= 16384:
        raise ValueError("max_bytes must be 256..16384")
    items = []
    next_offset = offset
    while next_offset < len(ROWS):
        candidate = items + [ROWS[next_offset]]
        next_cursor = next_offset + 1 if next_offset + 1 < len(ROWS) else None
        body = {"items": candidate, "next_cursor": next_cursor, "total": len(ROWS)}
        if len(json.dumps(body, ensure_ascii=False).encode("utf-8")) > max_bytes:
            break
        items = candidate
        next_offset += 1
    if not items and offset < len(ROWS):
        raise ValueError("single record exceeds response limit")
    return {"items": items, "next_cursor": next_offset if next_offset < len(ROWS) else None, "total": len(ROWS)}
