from fastmcp import FastMCP


def register_db_resources(mcp:FastMCP):
    @mcp.resource(
        uri="data://schools-schema",
        name="get DB Schema",
        description="Provides the current schema of schools db.", 
        tags={"data", "schema", "nsw", "schools"}, 
        meta={"version": "1.0", "team": "data-team", "contact": "kr_data_admin@hotmail.com"}  
    )
    def get_db_schema():
        raise NotImplementedError("This function is not yet implemented.")