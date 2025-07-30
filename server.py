from mcp.server.fastmcp import FastMCP, Context, ToolError
from mcp.server.auth.provider import AccessToken
from mcp.server.auth.middleware.auth_context import get_access_token

import requests
import logging
from rag_qa import get_context_from_query
mcp = FastMCP("server",port=8000,host="0.0.0.0",stateless_http=True)
logging.basicConfig(level=logging.DEBUG)
baseUrl = "https://plugins.ninjamock.com"

# @mcp.tool()
# def list_available_ui_templates() -> dict:
#     """
#     Retrieves all available UI templates from the Ninjamock tool.
#     Use this to get context about which templates can be used or created in the application.
#     Returns a dictionary with a 'templates' property containing an array of template objects.
#     """
#     api_url = f"{baseUrl}/api/v1/ui_templates"  
#     try:
#         response = requests.get(api_url, timeout=5)
#         response.raise_for_status()
#         templates = response.json()  
#         return {"templates": templates}
#     except Exception as e:
#         return {
#             "templates": [],
#             "error": str(e)
#         }
# @mcp.tool()
# def get_reference_ui_template_by_id(template_id: str) -> dict:
#     """
#     Retrieves a reference UI template from the Ninjamock template library by its ID.
#     Use this to get template examples and context for creating new templates, not for modifying the current project.
#     These are static reference templates that can be used as inspiration or starting points.
#     Returns a dictionary with the reference template data or an error message.
#     """
#     api_url = f"{baseUrl}/api/v1/ui_templates/{template_id}"  
#     try:
#         response = requests.get(api_url, timeout=5)
#         response.raise_for_status()
#         template_data = response.json()  
#         # json_data = template_data.get("jsonData") if template_data else None
#         return {"template": template_data}
#     except Exception as e:
#         return {
#             "template": None,
#             "error": str(e)
#         } 
# # MCP tools para interactuar con la API de Ninjamock usando token en header
def _get_auth_headers():
    token = get_access_token()
    return {"Authorization": token} if token else {}

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
def get_ninjamock_project_full(project_id: str, mcp_ctx: Context = None) -> dict:
    """
    Retrieves the full Ninjamock project by its ID in JSON format.
    Requires authentication via token in the 'Authorization' header.
    """
    api_url = f"{baseUrl}/api/v1/projects/{project_id}"
    headers = _get_auth_headers()
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
    api_url = f"{baseUrl}/api/v1/projects/{project_id}/elements/{element_id}"
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

if __name__ == "__main__":
    mcp.run(transport="streamable-http")

