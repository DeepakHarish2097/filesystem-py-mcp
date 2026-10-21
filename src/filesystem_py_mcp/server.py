import asyncio
from pathlib import Path

from fastmcp import Client, FastMCP

mcp = FastMCP("File System MCP")


@mcp.tool
def read_text_file(path: Path) -> str:
    """Read Text File"""
    try:
        with open(path, "r") as file:
            text_file = file.read()
        if type(text_file) == str:
            return text_file
    except Exception as e: # noqa
        pass
    return "Not a valid Text File."


@mcp.tool
def read_media_file(path: Path) -> str:
    """Read Media File"""
    try:
        with open(path, "rb") as file:
            media_file = file.read()
        return f"{media_file}"
    except Exception as e: # noqa
        print(e)
        return "Error Opening file"


async def main():
    async with Client(mcp) as client:
        result = await client.call_tool(
            "read_media_file",
            {"path": r"C:\MyProjects\MyBlenderProjects\Newfolder\download.jpg"},
        )
        print(result.data)


asyncio.run(main())
