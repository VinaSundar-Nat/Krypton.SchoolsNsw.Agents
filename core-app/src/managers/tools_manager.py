from neo4j import Driver
from provider import logprovider
from fastmcp import FastMCP
from mcp.types import Tool, TextContent
from common.base_tool_handler import BaseToolHandler
from typing import List, Any, Dict, Optional

class ToolManager:
    """ Tool manager to attach tools to a server."""

    def __init__(self, server: FastMCP):
        self.server = server
        self.logger = logprovider.get_logger()
        self.tool_handlers: Dict[str, BaseToolHandler] = {}
        self.tools_registry: Dict[str, str] = {}  

    def register_handler(self, handler_name: str, handler: BaseToolHandler):
        """Register a tool handler with the manager."""
        self.tool_handlers[handler_name] = handler
        
        # Register all tools from the handler
        for tool in handler.tools:
            self.tools_registry[tool.name] = handler_name
            self._register_tool_with_server(tool, handler)
        
        self.logger.info(f"Registered handler '{handler_name}' with {len(handler.tools)} tools")

    def _register_tool_with_server(self, tool: Tool, handler: BaseToolHandler):
        """Register a single tool with the FastMCP server."""
        @self.server.tool(tool.name, tool.description, tool.inputSchema)
        async def tool_wrapper(**kwargs) -> List[TextContent]:
            return await handler.execute(tool.name, kwargs)
              
        setattr(handler, f"_{tool.name}_wrapper", tool_wrapper)

    def unregister_handler(self, handler_name: str):
        """Unregister a tool handler and all its tools."""
        if handler_name not in self.tool_handlers:
            self.logger.warning(f"Handler '{handler_name}' not found")
            return

        handler = self.tool_handlers[handler_name]
        
        # Remove tools from registry
        tools_to_remove = [name for name, h_name in self.tools_registry.items() if h_name == handler_name]
        for tool_name in tools_to_remove:
            del self.tools_registry[tool_name]
        
        # Remove handler
        del self.tool_handlers[handler_name]
        self.logger.info(f"Unregistered handler '{handler_name}' and {len(tools_to_remove)} tools")

    def get_handler(self, handler_name: str) -> Optional[BaseToolHandler]:
        """Get a registered tool handler by name."""
        return self.tool_handlers.get(handler_name)

    def get_handler_for_tool(self, tool_name: str) -> Optional[BaseToolHandler]:
        """Get the handler responsible for a specific tool."""
        handler_name = self.tools_registry.get(tool_name)
        return self.tool_handlers.get(handler_name) if handler_name else None

    def list_handlers(self) -> List[str]:
        """List all registered handler names."""
        return list(self.tool_handlers.keys())

    def list_tools(self) -> Dict[str, str]:
        """List all registered tools and their associated handlers."""
        return self.tools_registry.copy()

    async def execute_tool(self, tool_name: str, arguments: Dict[str, Any]) -> List[TextContent]:
        """Execute a tool by name with given arguments."""
        handler = self.get_handler_for_tool(tool_name)
        if not handler:
            raise ValueError(f"No handler found for tool: {tool_name}")
        
        return await handler.execute(tool_name, arguments)