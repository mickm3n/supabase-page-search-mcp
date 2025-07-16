# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

### Running the MCP Server
```bash
# Run the MCP server directly
uv run main.py

# Or use the installed script
supabase-page-search-mcp
```

### Package Management
```bash
# Install dependencies
uv sync

# Add new dependencies
uv add package-name

# Check syntax
uv run python -m py_compile main.py
```

### Environment Setup
```bash
# Copy environment template
cp .env.example .env
# Edit .env with your API keys
```

## Architecture Overview

This is a **single-file MCP server** (`main.py`) that provides semantic search capabilities for Roam Research pages. The architecture follows a simple but effective pattern:

### Core Components

1. **RoamPageSearcher Class** - Main business logic handler
   - `get_embedding()`: Generates embeddings using OpenAI's `text-embedding-3-small` model
   - `search_similar_pages()`: Queries Supabase via REST API using the `match_notes_by_embedding` stored procedure

2. **MCP Tool Registration**
   - `search_roam_pages()`: Async MCP tool that combines embedding generation and similarity search
   - Returns JSON-formatted results with query, results, and total matches

3. **Configuration Management**
   - Environment variables loaded via `python-dotenv`
   - Three required environment variables: `OPENAI_API_KEY`, `SUPABASE_URL`, `SUPABASE_KEY`

### Data Flow
1. User provides search query → 
2. Generate embedding via OpenAI API → 
3. Query Supabase for similar pages → 
4. Return formatted JSON results

### External Dependencies
- **OpenAI API**: Uses `text-embedding-3-small` model for embeddings
- **Supabase**: Requires a `pages` table with `uid`, `text`, `embeddings` columns and a `match_notes_by_embedding` stored procedure
- **FastMCP**: Framework for MCP server implementation

## Required Environment Variables

```env
OPENAI_API_KEY=your_openai_api_key_here
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your_supabase_key_here
```

## Key Files

- `main.py` - Complete MCP server implementation
- `pyproject.toml` - Project configuration with uv package management
- `.env.example` - Environment variables template
- `README.md` - Comprehensive documentation with usage examples

## Development Notes

- **Package Manager**: Uses `uv` instead of pip
- **Python Version**: Requires Python 3.11+
- **Async Pattern**: Full async/await implementation for API calls
- **Error Handling**: Comprehensive exception handling with structured error responses
- **Commit Style**: Uses gitmoji for commit messages
- **Testing**: No formal test framework - test by running the MCP server directly

## Supabase Schema Requirements

The Supabase database must have:
- `pages` table with columns: `uid`, `text` (title), `embeddings`
- `match_notes_by_embedding` stored procedure for vector similarity search
- Proper vector similarity search capabilities enabled