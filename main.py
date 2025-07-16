import os
import json
import asyncio
from typing import List, Dict, Any
from fastmcp import FastMCP
from openai import OpenAI
import httpx
from dotenv import load_dotenv

load_dotenv()

mcp = FastMCP("Supabase Page Search MCP")

class RoamPageSearcher:
    def __init__(self):
        self.openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.supabase_url = os.getenv("SUPABASE_URL")
        self.supabase_key = os.getenv("SUPABASE_KEY")
        
    async def get_embedding(self, text: str) -> List[float]:
        """Get embedding for text using OpenAI text-embedding-3-small"""
        try:
            response = self.openai_client.embeddings.create(
                model="text-embedding-3-small",
                input=text,
                encoding_format="float"
            )
            return response.data[0].embedding
        except Exception as e:
            raise Exception(f"Failed to get embedding: {str(e)}")
    
    async def search_similar_pages(self, query_embedding: List[float], match_count: int = 5, threshold: float = 0.7) -> List[Dict[str, Any]]:
        """Search for similar pages using Supabase stored procedure"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.supabase_url}/rest/v1/rpc/match_notes_by_embedding",
                    json={
                        "match_count": match_count,
                        "query_embedding": query_embedding,
                        "threshold": threshold
                    },
                    headers={
                        "Content-Type": "application/json",
                        "apikey": self.supabase_key,
                        "Authorization": f"Bearer {self.supabase_key}"
                    }
                )
                response.raise_for_status()
                return response.json()
        except Exception as e:
            raise Exception(f"Failed to search pages: {str(e)}")

searcher = RoamPageSearcher()

@mcp.tool()
async def search_roam_pages(query: str, match_count: int = 5, threshold: float = 0.7) -> str:
    """
    Search for Roam Research pages by semantic similarity using OpenAI embeddings and Supabase.
    
    Args:
        query: The search query to find similar pages
        match_count: Number of similar pages to return (default: 5)
        threshold: Similarity threshold for matching (default: 0.7)
    
    Returns:
        JSON string with similar page titles and their similarity scores
    """
    try:
        # Get embedding for the query
        query_embedding = await searcher.get_embedding(query)
        
        # Search for similar pages
        similar_pages = await searcher.search_similar_pages(
            query_embedding=query_embedding,
            match_count=match_count,
            threshold=threshold
        )
        
        # Format results
        result = {
            "query": query,
            "results": similar_pages,
            "total_matches": len(similar_pages)
        }
        
        return json.dumps(result, indent=2, ensure_ascii=False)
        
    except Exception as e:
        error_result = {
            "error": str(e),
            "query": query
        }
        return json.dumps(error_result, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    mcp.run()
