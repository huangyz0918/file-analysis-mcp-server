# File Analysis MCP Server

This Model Context Protocol (MCP) server provides tools for reading and writing files, analyzing data (especially CSV files), generating visualizations, and reading PDF files - all accessible to any MCP client like Claude Desktop.

## Features

### File Operations
- Read and write text files securely
- List files in directories matching patterns
- Get detailed file information (size, creation time, etc.)
- Extract text content from PDF files

### Data Analysis
- Read and sample CSV files
- Analyze CSV data with detailed statistics
- Visualize data with various plot types (bar, line, scatter, histogram, boxplot)

### Included Prompts
- Analyze Data File - Comprehensive data analysis
- Data Cleaning Steps - Identifying and fixing data issues
- Generate Summary Report - Executive summary for stakeholders
- Exploratory Data Analysis - Detailed EDA workflow

## Installation

### Prerequisites
- Python 3.10 or higher
- Claude Desktop or another MCP client

### Setup

1. Install dependencies:
```bash
pip install "mcp[cli]" pandas numpy matplotlib PyPDF2
```

2. Set up safe directories (optional):
```bash
# Default directories are ~/Documents and ~/Downloads
# To customize, set this environment variable:
export MCP_FILE_ROOTS="~/Documents:~/Desktop:~/Downloads"
```

3. Install in Claude Desktop:
```bash
mcp install file_analysis_server.py
```

## Usage with Claude Desktop

Once installed, you can ask Claude questions like:

- "Can you list the files in my Documents folder?"
- "Read the content of ~/Documents/example.txt for me"
- "Extract text from my ~/Documents/report.pdf file"
- "Read page 5 of my PDF document"
- "Analyze the data in ~/Downloads/sample.csv"
- "Create a bar chart of the 'Sales' column from my CSV file"
- "Write a summary report of my quarterly_sales.csv file"

## Security

The server enforces strict path validation to ensure only files within authorized directories can be accessed. By default, these are limited to ~/Documents and ~/Downloads.

## Configuration

You can adjust the allowed directories by setting the `MCP_FILE_ROOTS` environment variable. Multiple directories should be separated by colons, for example:

```bash
mcp install file_analysis_server.py -v MCP_FILE_ROOTS="~/Documents:~/Desktop:~/projects/data"
```

## Development

For development and testing:

```bash
mcp dev file_analysis_server.py
```

This will start the server with the MCP Inspector interface for interactive testing.

## Examples

### Reading a file
```
Could you read the content of ~/Documents/notes.txt?
```

### Reading a PDF file
```
Can you extract the text from ~/Documents/report.pdf?
```

### Reading specific pages from a PDF
```
Please read pages 3 and 5 from ~/Downloads/manual.pdf
```

### Analyzing CSV data
```
I have a CSV file at ~/Downloads/sales_data.csv. Could you analyze it and tell me about the 'Revenue' column?
```

### Creating a visualization
```
Using my ~/Documents/monthly_data.csv file, can you create a bar chart showing 'Month' vs 'Profit'?
```

### Using prompts
```
Can you run an exploratory data analysis on ~/Downloads/customer_data.csv?
```