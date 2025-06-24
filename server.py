from mcp.server.fastmcp import FastMCP

mcp = FastMCP("server",port=8000,host="0.0.0.0")

@mcp.tool()
def greeting(name: str) -> str:
    "Send a greeting"
    return f"Hi {name}"

if __name__ == "__main__":
    mcp.run(transport="streamable-http")