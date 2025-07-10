from mcp.server.fastmcp import FastMCP
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
def search_reference_ui_templates_by_name(name: str) -> dict:
    """
    Searches for reference UI templates in the Ninjamock template library by name.
    Use this to find reference templates that can be used as inspiration or starting points for creating new templates.
    These are static reference templates, not part of the current project.
    Returns a dictionary with a 'reference_templates' property containing an array of matching template objects.
    """
    api_url = f"{baseUrl}/api/v1/ui_templates/search"  
    try:
        response = requests.get(api_url, params={"name": name}, timeout=5)
        response.raise_for_status()
        templates = response.json()
        # json_templates = [template.get("JsonData") for template in templates if template.get("JsonData")]
        return {"templates": templates}
    except Exception as e:
        return {
            "templates": [],
            "error": str(e)
        }
    
# @mcp.tool()
# def get_multiple_reference_templates_by_names(template_names: list) -> dict:
#     """
#     Retrieves multiple reference UI templates from the Ninjamock template library by their names.
#     Use this to get multiple reference templates that can be used as inspiration or starting points.
#     These are static reference templates, not part of the current project.
#     Returns a dictionary with a 'reference_templates' property containing an array of template objects.
#     """
#     all_templates = []
#     errors = []
    
#     for name in template_names:
#         try:
#             # First search for templates by name
#             search_url = f"{baseUrl}/api/v1/ui_templates/search"
#             search_response = requests.get(search_url, params={"name": name}, timeout=5)
#             search_response.raise_for_status()
#             search_results = search_response.json()
#             # Extract JsonData from each template in the array
#             for template in search_results:
#                 if template.get("JsonData"):
#                     all_templates.append(template.get("JsonData"))
            
#         except Exception as e:
#             errors.append(f"Error fetching template '{name}': {str(e)}")
    
#     return {
#         "templates": all_templates,
#         "errors": errors if errors else None,
#         "total_found": len(all_templates),
#         "template_names": template_names
#     }
# @mcp.tool()
# def add_component_to_project(name: str) -> dict:
#     """
#     Adds a component to the current project.
#     """
#     component = {
#         "name": name,
#     }
#     # project_components.append(component)
#     return {
#         "status": "success",
#         "message": f"Componente '{name}' añadido al proyecto.",
#         "component": component
#     }

if __name__ == "__main__":
    mcp.run(transport="streamable-http")