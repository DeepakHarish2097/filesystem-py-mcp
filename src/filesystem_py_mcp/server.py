import asyncio
import base64
import os
import shutil
import stat
from datetime import datetime
from pathlib import Path

from fastmcp import FastMCP

mcp = FastMCP("File System MCP")

@mcp.tool
def read_text_file(path: Path) -> str:
    """Read Text File"""
    try:
        with open(path, "r") as file:
            text_file = file.read()
        if type(text_file) == str:
            return text_file
    except Exception: # noqa
        return "Error Opening file"
    return "Not a valid Text File."


@mcp.tool
def read_media_file(path: Path) -> str:
    """Read Media File which return a base64 string"""
    try:
        with open(path, "rb") as file:
            media_file = file.read()
        return base64.b64encode(media_file).decode("utf-8")
    except Exception: # noqa
        return "Error Opening file"


@mcp.tool
def write_file(path: Path, content: str) -> str:
    """Create a new file"""
    try:
        with open(path, "w") as file:
            file.write(content)
        return "File created successfully"
    except Exception: # noqa
        return "Error creating file"


@mcp.tool
def create_directory(path: Path) -> str:
    """Create directory"""
    try:
        os.makedirs(path, exist_ok=True)
        return "Created directory"
    except Exception: # noqa
        return "Error creating directory"


@mcp.tool
def list_directory(path: Path) -> str:
    """List Directory"""
    try:
        files = os.listdir(path)
        data = []
        for file in files:
            if os.path.isdir(path / file):
                data.append(f"[DIR] {file}")
            else:
                data.append(f"[FILE] {file}")
        return "\n".join(data)
    except Exception: # noqa
        return "Error Listing Directory"


@mcp.tool
def directory_tree(path: Path) -> str:
    """Get directory tree"""
    try:
        files = [str(file) for file in path.rglob("*")]
        files.sort()
        return "\n".join(files)
    except Exception: # noqa
        return "Error getting directory Tree"


@mcp.tool
def move_file(src: Path, dst: Path) -> str:
    """Move file from one directory to another"""
    try:
        shutil.move(src, dst)
        return f"Moved file from {src} to {dst}"
    except Exception: # noqa
        return f"Error moving file from {src} to {dst}"


@mcp.tool
def copy_file(src: Path, dst: Path) -> str:
    """Copy file from one directory to another"""
    try:
        shutil.copy(src, dst)
        return f"Coppied file from {src} to {dst}"
    except Exception: # noqa
        return f"Error copying file from {src} to {dst}"


@mcp.tool
def search_files(path: Path, file: str) -> str:
    """Search Files"""
    try:
        files = [str(file) for file in path.rglob(file, case_sensitive=False)]
        if files:
            return "\n".join(files)
        else:
            return "No Matches found"
    except Exception: # noqa
        return f"Error while searching file {file}"


@mcp.tool
def get_file_info(path: Path) -> str:
    """Get file information"""
    try:
        file_stat = path.stat()
        return f"""Size: {file_stat.st_size}
Created: {datetime.fromtimestamp(file_stat.st_birthtime)}
Modified: {datetime.fromtimestamp(file_stat.st_mtime)}
Accessed: {datetime.fromtimestamp(file_stat.st_atime)}
Is Directory: {path.is_dir()}
Is File: {path.is_file()}
Permissions: {stat.S_IMODE(file_stat.st_mode):03o}"""
    except Exception: # noqa
        return "Error getting file info"


if __name__ == "__main__":
    asyncio.run(main())
