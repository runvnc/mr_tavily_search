print("Loading mod.py for Tavily Search")

import os
from lib.providers.services import service
from lib.providers.commands import command
import nanoid
from langchain_tavily import TavilySearch
import traceback
import sys

@service()
async def web_search(query, num_results=5, search_depth="basic", include_images=False):
    """Perform a web search using Tavily API.

    Args:
        query (str): The search query.
        num_results (int, optional): The number of results to return. Defaults to 5.

    Returns:
        list: A list of dictionaries containing search results.
    """
    try:

        include_image_descriptions = False
        if include_images:
            include_image_descriptions = True
        
        tool = TavilySearch(
            max_results=num_results,
            search_depth=search_depth,
            include_images=include_images,
            include_image_descriptions=include_image_descriptions
        )
        id = nanoid.generate()
        tool_results = await tool.arun(tool_input = {"query": query}, tool_call_id = id)
 
        results = tool_results.content
        print(results)
        print("returning ok")
        return results
    except Exception as e:
        trace = traceback.format_exc()
        print(f"Error in web search: {str(e)} \n\n{trace}")
        print("error occurred, returning empty list")
        return []

@command()
async def search_web(query, num_results=15, fetch_first=False, search_depth="basic", include_images=False, context=None):
    """Perform a web search and return the results.

    Note: For webpage content extraction, use mr_crawl4ai plugin's fetch_webpage 
    or crawl_site commands instead of this plugin's fetch functionality.

    Args:
        query (str): The search query.
        num_results (int, optional): The number of results to return. Defaults to 15.
        fetch_first (bool, optional): Whether to fetch the content of the first result. Defaults to False.
        search_depth: (str, optional): 'basic' (faster) or 'advanced' (deeper)
        include_images: (bool, optional): defaults to False, may be faster to omit unless needed
        context (object, optional): The context object for the current session.

    Returns:
        str: Formatted string containing search results.

    Example:
        [
            { "search_web": { "query": "Python programming", "num_results": 3 } }
        ]
    """
    try:
        search_results = await web_search(query, num_results, search_depth=search_depth, include_images=include_images)
        if not search_results:
            return "No results found. Please check your search query."

        return search_results        
    except Exception as e:
        return f"Error performing web search: {str(e)}"

if __name__ == "__main__":
    # This block is for testing purposes
    import asyncio
    
    async def test_search():
        results = await search_web("Python programming", num_results=5)
        print(results)
    
    asyncio.run(test_search())

print("Loaded mod.py for Tavily Search")
