
from fastmcp import FastMCP,Context
from fastmcp.server.dependencies import get_http_headers
from rag_search import search_rag
import requests
import logging
from rag_qa import get_context_from_query
mcp = FastMCP("server",port=8000,host="0.0.0.0",stateless_http=True)
logging.basicConfig(level=logging.DEBUG)
baseUrl = "https://plugins.ninjamock.com"

# # MCP tools para interactuar con la API de Ninjamock usando token en header
def _get_auth_headers():
    headers = get_http_headers()
    token = headers.get("authorization") or headers.get("x-api-key")
    if token:
        return {"Authorization": token}
    return  {}

    """
    Extract headers from the current HTTP request if available.

    Never raises an exception, even if there is no active HTTP request (in which case
    an empty dict is returned).

    By default, strips problematic headers like `content-length` that cause issues if forwarded to downstream clients.
    If `include_all` is True, all headers are returned.
    """
    if include_all:
        exclude_headers = set()
    else:
        exclude_headers = {
            "host",
            "content-length",
            "connection",
            "transfer-encoding",
            "upgrade",
            "te",
            "keep-alive",
            "expect",
            "accept",
            # Proxy-related headers
            "proxy-authenticate",
            "proxy-authorization",
            "proxy-connection",
            # MCP-related headers
            "mcp-session-id",
        }
        # (just in case)
        if not all(h.lower() == h for h in exclude_headers):
            raise ValueError("Excluded headers must be lowercase")
    headers = {}

    try:
        request = get_http_request()
        for name, value in request.headers.items():
            lower_name = name.lower()
            if lower_name not in exclude_headers:
                headers[lower_name] = str(value)
        return headers
    except RuntimeError:
        return {}
@mcp.tool()
def get_ninjamock_project_metadata(project_id: str, mcp_ctx: Context = None) -> dict:
    """
    Retrieves the metadata of a Ninjamock project by its ID.
    Requires authentication via token in the 'Authorization' header.
    """
    api_url = f"{baseUrl}/api/v1/projects/{project_id}/metadata"
    headers = _get_auth_headers()
    try:
        response = requests.get(api_url, headers=headers, timeout=5)
        response.raise_for_status()
        return {"metadata": response.json()}
    except Exception as e:
        return {"metadata": None, "error": str(e)}

@mcp.tool()
def get_ninjamock_project_full(project_id: str, mcp_ctx: Context) -> dict:
    """
    Retrieves the full Ninjamock project by its ID in JSON format.
    Requires authentication via token in the 'Authorization' header.
    """
    api_url = f"{baseUrl}/api/v1/projects/{project_id}"

    headers = _get_auth_headers()
    logging.info(f"Fetching project {project_id} from Ninjamock API with headers: {headers} context: {mcp_ctx}")
    #  mcp_ctx.info(f"Fetching project {project_id} from Ninjamock API with headers: {headers} context: {mcp_ctx}")
    try:
        response = requests.get(api_url, headers=headers, timeout=10)
        response.raise_for_status()
        return {"project": response.json()}
    except Exception as e:
        return {"project": None, "error": str(e)}

@mcp.tool()
def get_ninjamock_project_element_by_id(project_id: str, element_id: str, mcp_ctx=None) -> dict:
    """
    Retrieves a specific element of a Ninjamock project by its ID in JSON format.
    Requires authentication via token in the 'Authorization' header.
    """
    api_url = f"{baseUrl}/api/v1/projects/{project_id}/element/{element_id}"
    headers = _get_auth_headers()
    try:
        response = requests.get(api_url, headers=headers, timeout=5)
        response.raise_for_status()
        return {"element": response.json()}
    except Exception as e:
        return {"element": None, "error": str(e)}
     
@mcp.tool()
def search_ninjamock_docs(query: str) -> dict:
    """
    Searches the Ninjamock documentation for a specific query.
    """
    context = get_context_from_query(query)
    if not context:
        return {
            "answer": "No relevant information found in the Ninjamock documentation.",
            "context": ""
        }
    # Use the context to generate an answer
    answer = f"Based on the Ninjamock documentation, here is the information related to your query:\n\n{context}"
    
    return {
        "context": answer
    }

@mcp.tool()
def search_ui_templates(query: str, top_k: int = 5) -> dict:
    """
    Search and retrieve the most relevant UI templates for the query using RAG.
    Returns templates that the agent can use to create new elements by templateId.
    """
    index_path = "indices/ui_templates/faiss_index.index"
    metadata_path = "indices/ui_templates/metadata.json"
    try:
        results = search_rag(query, index_path, metadata_path, top_k=top_k)
        if not results:
            return {"answer": "No relevant UI templates found for the query.", "results": []}
        # Summarize for the agent: only show key fields
        summary = [
            {
                "title": r["title"],
                "templateId": r["templateId"],
                "type": r["type"],
                "category": r["category"],
                "description": r.get("text", ""),
                "properties": r.get("properties", {}),
                "defaultProperties": r.get("defaultProperties", {}),
            }
            for r in results
        ]
        return {
            "answer": f"Found {len(summary)} relevant UI templates.",
            "results": summary
        }
    except Exception as e:
        return {"answer": "Error searching UI templates.", "error": str(e), "results": []}
    
if __name__ == "__main__":
    mcp.run(transport="streamable-http")

