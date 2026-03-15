from fastmcp import FastMCP
import httpx
import os
from typing import Any, Mapping

mcp = FastMCP("backend-tools")

BACKEND_URL = os.getenv("BACKEND_URL", "http://backend:8000")


client = httpx.AsyncClient(timeout=20.0)

async def _get_json(path: str, params: Mapping[str, str] | None = None) -> Any:
    try:
        response = await client.get(f"{BACKEND_URL}{path}", params=params)
        response.raise_for_status()
        return response.json()
    except httpx.HTTPError as e:
        return {"error": str(e)}


@mcp.tool()
async def get_system_status():
    """
    Returns backend health status.
    """
    return await _get_json("/")

@mcp.tool()
async def ping():
    """Simple connectivity test."""
    return {"message": "pong"}

@mcp.tool()
async def bla():
    """Simple connectivity test."""
    return {"message": "blablablabla"}

@mcp.tool()
async def list_packages():
    """
    Retrieve all packages currently being tracked.
    """
    return await _get_json("/packages")

@mcp.tool()
async def get_delayed_milestones():
    """
    Returns delayed milestones for active packages.
    """
    return await _get_json("/analytics/delayed-milestones")


@mcp.tool()
async def summarize_delayed_packages():
    """
    Returns a summary of delayed packages.
    """
    return await _get_json("/analytics/delayed-packages")


@mcp.tool()
async def summarize_delay_by_category():
    """
    Returns delay aggregation grouped by package category.
    """
    return await _get_json("/analytics/delay-by", params={"dimension": "category"})


@mcp.tool()
async def sumarize_delay_by_milestone():
    """
    Returns delay aggregation grouped by milestone.
    """
    return await _get_json("/analytics/delay-by", params={"dimension": "milestone"})


@mcp.tool()
async def sumarize_delay_by_package():
    """
    Returns delay aggregation grouped by package.
    """
    return await _get_json("/analytics/delay-by", params={"dimension": "package"})


@mcp.tool()
async def sumarize_package_status(package_id: int):
    """
    Returns status and progress details for a package.
    """
    return await _get_json(f"/analytics/package-status/{package_id}")



app = mcp.http_app(path="/mcp/")