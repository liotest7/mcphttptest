from mcp.server.fastmcp import FastMCP
import logging
mcp = FastMCP("server",port=8000,host="0.0.0.0",stateless_http=True)
logging.basicConfig(level=logging.DEBUG)

@mcp.tool()
def greeting(name: str) -> str:
    "Send a greeting"
    return f"Hi {name}"

@mcp.tool()
def get_known_ui_templates() -> dict:
    """
    Returns an updated list of UI templates that are available in the ninjamock application.
    """
    return {
        "templates": [
        "Button",
        "Text",
        "Image",
        "Icon",
        "Video",
        "Rectangle",
        "Line",
        "Ellipse",
        "Polygon",
        "Star",
        "Android Compact",
        "iPhone 16",
        "Desktop",
        "iPad Pro 11"
    ]}

@mcp.tool()
def get_ui_templates(template_names: list) -> dict:
    """
    Returns the requested UI templates in JSON format to create new elements.
    """
    return {
        "templates": [
            '{"id": "452e45e9-db6f-fcc3-c0e6-f6cc05b00057", "name": "Android Compact", "tags": [], "type": "device", "scope": "", "states": [], "category": "frame", "children": [], "properties": {"top": 50, "clip": true, "fill": {"type": "solid", "alpha": 1, "color": "#ffffff"}, "left": 129, "width": 412, "height": 915, "deviceWidth": 412, "deviceHeight": 915}}',
         '{"id":"0d37f7b1-b133-bc92-f94f-73316dbe64ec","name":"Button","type":"button-basic","states":[],"children":[{"id":"ec2137a4-3b11-3a3b-04c7-4f4005a4d6ed","name":"Icon","tags":["trailingicon"],"type":"icon-svg","scope":"content","states":[],"children":[{"id":"7c9addb1-eb45-72e1-3795-4aa9df9ff2cf","name":"Path","type":"path","states":[],"children":[],"properties":{"top":0,"fill":{"type":"solid","alpha":1,"color":"#ffffff"},"left":0,"path":"M240-160q-33 0-56.5-23.5T160-240v-80q0-17 11.5-28.5T200-360q17 0 28.5 11.5T240-320v80h480v-80q0-17 11.5-28.5T760-360q17 0 28.5 11.5T800-320v80q0 33-23.5 56.5T720-160H240Zm200-486-75 75q-12 12-28.5 11.5T308-572q-11-12-11.5-28t11.5-28l144-144q6-6 13-8.5t15-2.5q8 0 15 2.5t13 8.5l144 144q12 12 11.5 28T652-572q-12 12-28.5 12.5T595-571l-75-75v286q0 17-11.5 28.5T480-320q-17 0-28.5-11.5T440-360v-286Z","width":18,"height":18}}],"properties":{"icon":"icon-upload","width":18,"height":18,"viewBox":"0 -960 960 960","visible":false,"position":"static"}},{"id":"956e78df-a883-39ec-7768-3ab5475b6309","name":"Icon","tags":["leadingicon"],"type":"icon-svg","scope":"content","states":[],"children":[{"id":"fa4fab9e-9688-2dc1-7d6b-1e13faf1b3cb","name":"Path","type":"path","states":[],"children":[],"properties":{"top":0,"fill":{"type":"solid","alpha":1,"color":"#ffffff"},"left":0,"path":"M240-160q-33 0-56.5-23.5T160-240v-80q0-17 11.5-28.5T200-360q17 0 28.5 11.5T240-320v80h480v-80q0-17 11.5-28.5T760-360q17 0 28.5 11.5T800-320v80q0 33-23.5 56.5T720-160H240Zm200-486-75 75q-12 12-28.5 11.5T308-572q-11-12-11.5-28t11.5-28l144-144q6-6 13-8.5t15-2.5q8 0 15 2.5t13 8.5l144 144q12 12 11.5 28T652-572q-12 12-28.5 12.5T595-571l-75-75v286q0 17-11.5 28.5T480-320q-17 0-28.5-11.5T440-360v-286Z","width":18,"height":18}}],"properties":{"icon":"icon-upload","width":18,"height":18,"zIndex":1,"viewBox":"0 -960 960 960","visible":false,"position":"static"}},{"id":"a0065bca-2789-ab3e-5b07-4bfe59628a66","name":"Label","type":"text","scope":"content","states":[],"children":[],"properties":{"top":13,"left":13,"text":"Button","color":{"type":"solid","alpha":1,"color":"#ffffff"},"width":47,"height":19,"zIndex":2,"fontSize":16,"position":"static"}}],"properties":{"top":146,"fill":{"type":"solid","alpha":1,"color":"#1d4ed8"},"gapX":8,"gapY":8,"left":169.5,"width":73,"height":45,"stroke":{"type":"solid","alpha":1,"color":"#1d4ed8"},"zIndex":1,"alignItems":"center","leadingIcon":"icon-upload","strokeWidth":1,"borderRadius":8,"trailingIcon":"icon-upload","justifyContent":"center"}}'
        ]}


if __name__ == "__main__":
    mcp.run(transport="streamable-http")