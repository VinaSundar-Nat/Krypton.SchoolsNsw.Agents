from fastmcp import FastMCP
from starlette.requests import Request
from starlette.responses import PlainTextResponse
from managers.tools_manager import ToolManager 
from server_farm.graph_db.dbtools import DBToolHandler
from neo4j import Driver
from provider import logprovider
from typing import Optional
import uuid

graphdb_mcp = FastMCP(name="Neo4JService",
                 instructions="This NEO4J MCP provides database search and CRUD functionalities.",
                 version="1.0"
                 )
 
logger = logprovider.get_logger()

def register_db_tools(driver: Driver, correlation_id: Optional[str] = uuid.uuid4()) :
    """Register all DB tools with the manager."""
    
    db_handler = DBToolHandler(driver, str(correlation_id))
    tool_manager = ToolManager(graphdb_mcp)
    tool_manager.register_handler("database", db_handler)
    
    logger.info("Database tools registered successfully")
