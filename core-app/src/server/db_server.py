from fastmcp import FastMCP
from starlette.requests import Request
from starlette.responses import PlainTextResponse
from managers.tools_manager import ToolManager 
from server_farm.graph_db.dbtools import DBToolHandler
from neo4j import Driver
from provider import logprovider
from typing import Optional
import uuid
from config import config
from neo4j import GraphDatabase
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from context.dbcontext import DbContext 

@asynccontextmanager
async def app_lifespan(server: FastMCP) -> AsyncIterator[DbContext]:
    """Manage application lifecycle with type-safe context."""
    # Initialize on startup
    driver = GraphDatabase.driver(
        config['NEO4J_URI'],
        auth=(
            config['NEO4J_USERNAME'],
            config['NEO4J_PASSWORD']
        )
    )
    try:
        register_db_tools(uuid.uuid4())
        yield DbContext(driver=driver)
    finally:
        # Cleanup on shutdown
        await driver.close()
 
logger = logprovider.get_logger()
graphdb_mcp = FastMCP(name="Neo4JService",
                 instructions="This NEO4J MCP provides database search and CRUD functionalities.",
                 version="1.0",
                 lifespan=app_lifespan
                 )

def register_db_tools(correlation_id: Optional[str] = uuid.uuid4()) :
    """Register all DB tools with the manager."""

    db_handler = DBToolHandler(str(correlation_id))
    tool_manager = ToolManager(graphdb_mcp)
    tool_manager.register_handler("database", db_handler)
    
    logger.info("Database tools registered successfully")
