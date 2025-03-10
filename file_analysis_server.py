import os
import glob
import json
import sys
from typing import List, Dict, Optional, Union, Any
from datetime import datetime

from mcp.server.fastmcp import FastMCP, Context

# Create a server instance
mcp = FastMCP("FileSystemServer")

# Define safe root directories to access
DEFAULT_ROOTS = [os.path.expanduser("~/Documents"), os.path.expanduser("~/Downloads")]
SAFE_ROOTS = os.environ.get("MCP_FILE_ROOTS", ":".join(DEFAULT_ROOTS)).split(":")

# Print debug information to stderr so it appears in logs
print(f"Starting FileSystemServer with safe roots: {SAFE_ROOTS}", file=sys.stderr)

# Validate and sanitize file paths
def safe_path(path: str) -> str:
    """Ensure a path is within allowed directories"""
    abs_path = os.path.abspath(os.path.expanduser(path))
    
    for root in SAFE_ROOTS:
        root_path = os.path.abspath(os.path.expanduser(root))
        if abs_path.startswith(root_path):
            return abs_path
    
    raise ValueError(f"Path '{path}' is outside of allowed directories: {SAFE_ROOTS}")

# File reading tools
@mcp.tool()
def read_file(path: str) -> str:
    """
    Read and return the contents of a text file.
    
    Args:
        path: Path to the file to read
        
    Returns:
        The file contents as text
    """
    print(f"Attempting to read file: {path}", file=sys.stderr)
    file_path = safe_path(path)
    
    if not os.path.exists(file_path):
        return f"Error: File '{path}' not found."
    
    try:
        with open(file_path, 'r') as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {str(e)}"

@mcp.tool()
def write_file(path: str, content: str) -> str:
    """
    Write content to a text file.
    
    Args:
        path: Path where the file should be written
        content: Text content to write to the file
        
    Returns:
        Confirmation message
    """
    print(f"Attempting to write file: {path}", file=sys.stderr)
    try:
        file_path = safe_path(path)
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        with open(file_path, 'w') as f:
            f.write(content)
            
        return f"Successfully wrote {len(content)} characters to {path}"
    except Exception as e:
        return f"Error writing file: {str(e)}"

@mcp.tool()
def list_files(directory: str, pattern: str = "*") -> str:
    """
    List files in a directory matching a pattern.
    
    Args:
        directory: Directory to list files from
        pattern: Glob pattern to match files (default: "*")
        
    Returns:
        List of matching files
    """
    print(f"Listing files in: {directory} with pattern: {pattern}", file=sys.stderr)
    try:
        dir_path = safe_path(directory)
        
        if not os.path.isdir(dir_path):
            return f"Error: '{directory}' is not a directory."
        
        matched_files = glob.glob(os.path.join(dir_path, pattern))
        
        if not matched_files:
            return f"No files matching '{pattern}' found in {directory}"
        
        file_list = "\n".join([os.path.basename(f) for f in matched_files])
        return f"Files in {directory} matching '{pattern}':\n{file_list}"
    except Exception as e:
        return f"Error listing files: {str(e)}"

@mcp.tool()
def file_info(path: str) -> str:
    """
    Get information about a file.
    
    Args:
        path: Path to the file
        
    Returns:
        File information (size, creation time, modification time)
    """
    print(f"Getting file info for: {path}", file=sys.stderr)
    try:
        file_path = safe_path(path)
        
        if not os.path.exists(file_path):
            return f"Error: File '{path}' not found."
        
        stat_info = os.stat(file_path)
        
        created = datetime.fromtimestamp(stat_info.st_ctime).strftime('%Y-%m-%d %H:%M:%S')
        modified = datetime.fromtimestamp(stat_info.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
        size_bytes = stat_info.st_size
        
        if size_bytes < 1024:
            size_str = f"{size_bytes} bytes"
        elif size_bytes < 1024 * 1024:
            size_str = f"{size_bytes/1024:.2f} KB"
        else:
            size_str = f"{size_bytes/(1024*1024):.2f} MB"
        
        return f"File: {path}\nSize: {size_str}\nCreated: {created}\nModified: {modified}"
    except Exception as e:
        return f"Error getting file info: {str(e)}"

# Resources for filesystem access
@mcp.resource("file://{path}")
def file_resource(path: str) -> str:
    """
    Access file contents as a resource.
    
    Args:
        path: Path to the file
        
    Returns:
        File contents
    """
    print(f"Accessing file resource: {path}", file=sys.stderr)
    try:
        file_path = safe_path(path)
        
        if not os.path.exists(file_path):
            return f"Error: File '{path}' not found."
        
        with open(file_path, 'r') as f:
            return f.read()
    except Exception as e:
        return f"Error accessing file resource: {str(e)}"

@mcp.resource("dir://{directory}")
def directory_resource(directory: str) -> str:
    """
    List directory contents as a resource.
    
    Args:
        directory: Directory path
        
    Returns:
        Directory listing
    """
    print(f"Accessing directory resource: {directory}", file=sys.stderr)
    try:
        dir_path = safe_path(directory)
        
        if not os.path.isdir(dir_path):
            return f"Error: '{directory}' is not a directory."
        
        files = os.listdir(dir_path)
        
        result = [f"Directory: {directory}"]
        for file in files:
            full_path = os.path.join(dir_path, file)
            if os.path.isdir(full_path):
                result.append(f"📁 {file}/")
            else:
                size = os.path.getsize(full_path)
                if size < 1024:
                    size_str = f"{size} bytes"
                elif size < 1024 * 1024:
                    size_str = f"{size/1024:.1f} KB"
                else:
                    size_str = f"{size/(1024*1024):.1f} MB"
                result.append(f"📄 {file} ({size_str})")
        
        return "\n".join(result)
    except Exception as e:
        return f"Error accessing directory resource: {str(e)}"

# Prompt for file operations
@mcp.prompt()
def organize_files(directory: str) -> str:
    """
    Create a prompt for organizing files in a directory.
    
    Args:
        directory: Directory path containing files to organize
    """
    return f"""Please help me organize the files in "{directory}". For this task:

1. List all files in the directory
2. Suggest a logical grouping or categorization for the files
3. Create a plan for where each file should go
4. Help me implement the organization plan

You can use the list_files tool to see what's in the directory, and write_file to create any new files needed."""

if __name__ == "__main__":
    # You can run the server directly
    print("Starting FileSystemServer...", file=sys.stderr)
    mcp.run()