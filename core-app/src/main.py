
from config import config
from fastmcp import FastMCP
from neo4j import GraphDatabase
from provider import logprovider
from server.health_check import health_mcp
from server.db_server import graphdb_mcp
import asyncio 

Coremcp = FastMCP(name='core-app',
               instructions="""
                    This server provides data analysis tools.
                    Call fetch_from_db() to fetch graph data.
                """,
               version="1.0",
               dependencies=["neo4j", "pydantic" ,"dspy"], 
               stateless_http=True)

logger = logprovider.get_logger()

driver = GraphDatabase.driver(
    config['NEO4J_URI'],
    auth=(
        config['NEO4J_USERNAME'],
        config['NEO4J_PASSWORD']
    )
)

async def setup():
    await Coremcp.import_server(health_mcp, prefix="core")
    await Coremcp.import_server(graphdb_mcp, prefix="database")

def main():
    transport=config['MCP_TRANSPORT']
    logger.info(f"Starting MCP ..")
    if transport == "http" or transport == "https":
        host = config['API_ENDPOINT']
        Coremcp.run(host=host, transport=transport, port=8200)
        logger.info(f"MCP is running on {transport.upper()} at {host}")
    else:
        Coremcp.run(transport="stdio")


if __name__ == "__main__":
    asyncio.run(setup())
    main()
