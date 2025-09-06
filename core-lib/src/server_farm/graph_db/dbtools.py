from click import command
from neo4j import Driver
from provider import logprovider
from neo4j import Driver
from mcp.types import Tool, TextContent
from common.base_tool_handler import BaseToolHandler
from typing import List, Any, Dict, Optional
import uuid
from fastmcp.server import Context 

logger = logprovider.get_logger()

class DBToolHandler(BaseToolHandler):
    def __init__(self,  correlation_id: Optional[str] = None):
        self.correlation_id = correlation_id or str(uuid.uuid4())

    @property
    def tools(self) -> List[Tool]:
        return [
            Tool(
                name="insert_into_db",
                description="Insert data into the database executing cypher command.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "command": {"type": "string", "description": "Cypher command to execute for inserting data"},
                        "ctx": {"type": "object", "description": "Context for the operation"}
                    },
                    "required": ["command"]
                }
            ),
            Tool(
                name="fetch_from_db",
                description="Fetch data from the database executing cypher query.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "Cypher query to execute for fetching data"},
                        "ctx": {"type": "object", "description": "Context for the operation"}
                    },
                    "required": ["query"]
                }
            )
        ]
    
    async def execute(self, arguments: Dict[str, Any]) -> List[TextContent]:
        tool_name = arguments["tool_name"]
        input_data = arguments["input_data"]
        ctx = Context(input_data.get("ctx"))
        
        if tool_name == "fetch_from_db":
            query = str(input_data.get("query"))
            return [TextContent(type="text", text= await self.fetch_from_db(query, ctx))]
        elif tool_name == "insert_into_db":
            command = str(input_data.get("command"))
            return [TextContent(type="text", text= await self.insert_into_db(command, ctx))]
        else:
            raise ValueError(f"Unknown tool: {tool_name}")

    async def fetch_from_db(self, query: str,  ctx: Context) -> str:
        """Fetch data from the database executing cypher query."""
        driver: Driver = ctx.request_context.lifespan_context.driver
        with driver.session() as session:
            logger.info(f"Executing query - correlation_id: {self.correlation_id}")
            result = session.run(query)
            logger.info(f"Query fetched - correlation_id: {self.correlation_id}")
            records = [dict(r) for r in result]
            return str(records)

    async def insert_into_db(self, command: str, ctx: Context) -> str:
        """Insert data into the database executing cypher command."""
        raise NotImplementedError("This function is not yet implemented.")
