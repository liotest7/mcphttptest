from mcp.server.fastmcp import FastMCP
import logging
mcp = FastMCP("server",port=8000,host="0.0.0.0")
logging.basicConfig(level=logging.DEBUG)

@mcp.tool()
def greeting(name: str) -> str:
    "Send a greeting"
    return f"Hi {name}"

# @mcp.on_event("session_start")
# async def on_session_start(session_id: str):
#     print(f"✅ Nueva sesión iniciada: {session_id}")

# @mcp.on_event("session_end")
# async def on_session_end(session_id: str):
#     print(f"❌ Sesión terminada: {session_id}")


if __name__ == "__main__":
    mcp.run(transport="streamable-http")