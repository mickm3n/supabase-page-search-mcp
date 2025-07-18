# Supabase Page Search MCP

A Model Context Protocol (MCP) server for semantic search of Roam Research pages using OpenAI embeddings and Supabase.

## Features

- **Semantic Search**: Find relevant Roam Research pages using natural language queries
- **OpenAI Embeddings**: Uses `text-embedding-3-small` model for high-quality embeddings
- **Supabase Integration**: Leverages Supabase's vector similarity search capabilities
- **FastMCP**: Built with FastMCP for easy MCP server development

## Prerequisites

- Python 3.11+
- OpenAI API key
- Supabase project with:
  - A `pages` table with columns: `uid`, `text` (title), `embeddings`
  - A stored procedure `match_notes_by_embedding` for similarity search

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd supabase-page-search-mcp
```

2. Install dependencies with uv:
```bash
uv sync
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your API keys
```

## Configuration

Create a `.env` file with the following variables:

```env
# OpenAI API Key
OPENAI_API_KEY=your_openai_api_key_here

# Supabase Configuration
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your_supabase_key_here
```

## Usage

### As MCP Server

Run the MCP server:
```bash
uv run main.py
```

### Available Tools

#### `search_roam_pages`

Search for Roam Research pages by semantic similarity.

**Parameters:**
- `query` (str): The search query to find similar pages
- `match_count` (int, optional): Number of similar pages to return (default: 5)
- `threshold` (float, optional): Similarity threshold for matching (default: 0.7)

**Returns:**
JSON string with similar page titles and their similarity scores.

**Example:**
```python
# Search for pages related to "machine learning"
result = await search_roam_pages("machine learning", match_count=10, threshold=0.6)
```

## Architecture

The MCP server consists of:

1. **RoamPageSearcher**: Core class handling OpenAI and Supabase interactions
2. **search_roam_pages**: MCP tool for semantic search
3. **Environment Configuration**: Secure API key management

## Development

### Project Structure

```
supabase-page-search-mcp/
├── main.py                 # MCP server implementation
├── pyproject.toml          # Project configuration
├── .env.example           # Environment variables template
├── README.md              # This file
└── .env                   # Your environment variables (not in git)
```

### Running Tests

```bash
# Test the MCP server
uv run main.py
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Use gitmoji for commit messages
5. Create a pull request

## License

This project is open source and available under the MIT License.