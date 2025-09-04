from neo4j import Driver
from provider import logprovider
from fastmcp import FastMCP
from neo4j import Driver
from mcp.types import Tool, TextContent
from common.base_tool_handler import BaseToolHandler
from typing import List, Any, Dict, Optional
import uuid

logger = logprovider.get_logger()

class DBToolHandler(BaseToolHandler):
    def __init__(self, driver: Driver, correlation_id: Optional[str] = None):
        self.driver = driver
        self.correlation_id = correlation_id or str(uuid.uuid4())

    @property
    def tools(self) -> List[Tool]:
        return [
            Tool(
                name="insert_into_db",
                description="Insert data into the database executing cypher command.",
                input_type=object,
                output_type=TextContent,
                inputSchema={
                    "type": "object",
                    "properties": {
                        "data": {"type": "string", "description": "data value to be added"},
                        "node": {"type": "string", "description": "Cypher Node ID to link data"}
                    },
                    "required": ["data", "node"]
                }
            ),
            Tool(
                name="fetch_from_db",
                description="Fetch data from the database executing cypher query.",
                input_type=TextContent,
                output_type=TextContent
            )
        ]
    
    async def execute(self, arguments: Dict[str, Any]) -> List[TextContent]:
        tool_name = arguments["tool_name"]
        input_data = arguments["input_data"]
        if tool_name == "fetch_from_db":
            return [TextContent(type="text", text= await self.fetch_from_db(input_data))]
        elif tool_name == "insert_into_db":
            return [TextContent(type="text", text= await self.insert_into_db(input_data))] 
        else:
            raise ValueError(f"Unknown tool: {tool_name}")

    async def fetch_from_db(self, query: str) -> str:
        """Fetch data from the database executing cypher query."""
        with self.driver.session() as session:
            logger.info(f"Executing query - correlation_id: {self.correlation_id}")
            result = session.run(query)
            logger.info(f"Query fetched - correlation_id: {self.correlation_id}")
            records = [dict(r) for r in result]
            return str(records)

    async def insert_into_db(self, command: str) -> str:
        """Insert data into the database executing cypher command."""
        raise NotImplementedError("This function is not yet implemented.")
