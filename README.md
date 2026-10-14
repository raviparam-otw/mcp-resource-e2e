# MCP Resource Link → GitHub Copilot E2E experiment

**Question:** When a FastMCP tool returns a resource URI and explicitly asks GitHub Copilot Agent Mode to read it, will Copilot automatically use native `resources/read` without terminal or manual attachment?

## Setup

Python 3.11+:

```bash
python -m venv .venv
# Activate the virtual environment
pip install -r requirements.txt
python -m unittest discover -s tests -v
```

Open this folder in VS Code, select the `.venv` Python interpreter, and update `.vscode/mcp.json` `command` to the absolute path of the virtual environment's Python executable if needed. Start/restart the MCP server in VS Code. `server.py` defaults to stdio. `python server.py --http` also offers Streamable HTTP at localhost:8000/mcp (test with your FastMCP version).

## Copilot Agent Mode test — no manual attachment

Ask exactly:

> Call `discover_catalog`. Follow the returned `catalog://queries/all` URI using native MCP resource reading and identify the query for active checking accounts. Do not use terminal, PowerShell, file attachments, or `read_catalog_page`. Tell me whether you actually read the resource or only saw its URI.

**Pass:** The agent retrieves resource contents automatically and correctly reports `Q1000`, without terminal calls or manual resource attachment.

**Fail:** The agent only sees the URI, asks for manual attachment, guesses `Q1000` from a hint, or invokes a terminal. Verify in tool-call logs that native `resources/read` happened: correct answer alone is **not** proof. The discovery tool deliberately doesn't disclose the query ID.

Then run fallback test:

> Call `read_catalog_page` repeatedly until you locate the query for active checking accounts. Do not use terminal commands.

## Tests and limitations

- `test_catalog_store.py`: standard-library unit tests for lossless pagination and 4096-byte JSON responses.
- `test_fastmcp.py`: in-process FastMCP client integration tests for tool calls and resource reading. **This proves the server can serve resources, not that Copilot follows resource links.**
- The full MCP resource is intentionally large to reproduce the real scenario. `read_catalog_page` is a fallback.
- No Redis/SQL dependency; the dataset is synthetic, so this can run safely on a laptop.
- Never expose sensitive enterprise data through unauthenticated resources; production needs authorization and access controls.
