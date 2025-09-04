from fastmcp import FastMCP
from starlette.requests import Request
from starlette.responses import JSONResponse,PlainTextResponse

health_mcp = FastMCP(name="HealthCheckService",
                     instructions="This MCP provides health check functionalities.",
                     version="1.0"
                     )  

@health_mcp.custom_route("/health", methods=["GET"])
async def health_check(request: Request) -> PlainTextResponse:
    return PlainTextResponse("OK")

@health_mcp.custom_route("/health/detailed", methods=["GET"])
async def detailed_health_check(request: Request) -> JSONResponse:
    try:
        # Add any health checks here (database, external services, etc.)
        return JSONResponse({
            "status": "healthy",
            "service": "HealthCheckService",
            "version": "1.0",
            "timestamp": "2024-09-04T22:32:04Z"
        })
    except Exception as e:
        return JSONResponse({
            "status": "unhealthy",
            "error": str(e)
        }, status_code=500)
