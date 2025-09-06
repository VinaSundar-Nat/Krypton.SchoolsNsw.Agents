from config import config
from fastmcp import FastMCP
from provider import logprovider
from server.health_check import health_mcp
from server.db_server import graphdb_mcp , register_db_tools
import asyncio
import contextlib
from starlette.applications import Starlette
from starlette.routing import Mount

Coremcp = FastMCP(name='core-app',
               instructions="""
                    This server provides data analysis tools.
                """,
               version="1.0",
               dependencies=["neo4j", "pydantic" ,"dspy"], 
               stateless_http=True)

logger = logprovider.get_logger()


async def setup():
    await Coremcp.import_server(health_mcp, prefix="core")
    await Coremcp.import_server(graphdb_mcp, prefix="database")


@contextlib.asynccontextmanager
async def lifespan(app: Starlette):
    async with contextlib.AsyncExitStack() as stack:
        await stack.enter_async_context(health_mcp.session_manager.run())
        await stack.enter_async_context(graphdb_mcp.session_manager.run())
        yield

def serverOps():
    transport=config['MCP_TRANSPORT']
    logger.info(f"Starting MCP ..")
    if transport == "streamable-http" or transport == "https":
        host = config['API_ENDPOINT']

        app = Starlette(
            routes=[
                Mount("/app", health_mcp.streamable_http_app()),
                Mount("/database", graphdb_mcp.streamable_http_app()),
            ],
            lifespan=lifespan,
        )

        Coremcp.app = app
        Coremcp.run(host=host, transport=transport, port=8200)
        logger.info(f"MCP is running on {transport.upper()} at {host}")
    else:
        asyncio.run(setup())
        Coremcp.run(transport="stdio")


if __name__ == "__main__":
    serverOps()