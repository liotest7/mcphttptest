from mcp.server.fastmcp import FastMCP
import requests
import logging
mcp = FastMCP("server",port=8000,host="0.0.0.0",stateless_http=True)
logging.basicConfig(level=logging.DEBUG)
baseUrl = "https://plugins.ninjamock.com"

@mcp.tool()
def list_available_ui_templates() -> dict:
    """
    Retrieves all available UI templates from the Ninjamock tool.
    Use this to get context about which templates can be used or created in the application.
    Returns a dictionary with a 'templates' property containing an array of template objects.
    """
    api_url = f"{baseUrl}/api/v1/ui_templates"  
    try:
        response = requests.get(api_url, timeout=5)
        response.raise_for_status()
        templates = response.json()  
        return {"templates": templates}
    except Exception as e:
        return {
            "templates": [],
            "error": str(e)
        }
@mcp.tool()
def get_ui_template_by_id(template_id: str) -> dict:
    """
    Retrieves the full data of a UI template from the Ninjamock tool by its ID.
    Use this to get the complete JSON definition of a specific template, since the list endpoint only provides metadata.
    Returns a dictionary with the template data or an error message.
    """
    api_url = f"{baseUrl}/api/v1/ui_templates/{template_id}"  
    try:
        response = requests.get(api_url, timeout=5)
        response.raise_for_status()
        template_data = response.json()  
        return {"template": template_data}
    except Exception as e:
        return {
            "template": None,
            "error": str(e)
        }
@mcp.tool()
def search_ui_templates_by_name(name: str) -> dict:
    """
    Searches for UI templates in the Ninjamock tool by name.
    Use this to find templates that match a given name or keyword.
    Returns a dictionary with a 'templates' property containing an array of matching template objects.
    """
    api_url = f"{baseUrl}/api/v1/ui_templates/search"  
    try:
        response = requests.get(api_url, params={"name": name}, timeout=5)
        response.raise_for_status()
        templates = response.json()
        return {"templates": templates}
    except Exception as e:
        return {
            "templates": [],
            "error": str(e)
        }
@mcp.tool()
def get_multiple_templates_by_names(template_names: list) -> dict:
    """
    Retrieves multiple UI templates from the Ninjamock tool by their names.
    Searches for each template name and returns the complete data for all found templates.
    Returns a dictionary with a 'templates' property containing an array of template objects.
    """
    all_templates = []
    errors = []
    
    for name in template_names:
        try:
            # First search for templates by name
            search_url = f"{baseUrl}/api/v1/ui_templates/search"
            search_response = requests.get(search_url, params={"name": name}, timeout=5)
            search_response.raise_for_status()
            search_results = search_response.json()
            all_templates.append(search_results)
            # Get full data for each found template
            # if search_results:
            #     for template_meta in search_results:
            #         if 'id' in template_meta:
            #             detail_url = f"{baseUrl}/api/v1/ui_templates/{template_meta['id']}"
            #             detail_response = requests.get(detail_url, timeout=5)
            #             detail_response.raise_for_status()
            #             template_data = detail_response.json()
            #             all_templates.append(template_data)
            
        except Exception as e:
            errors.append(f"Error fetching template '{name}': {str(e)}")
    
    return {
        "templates": all_templates,
        "errors": errors if errors else None,
        "total_found": len(all_templates)
    }
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