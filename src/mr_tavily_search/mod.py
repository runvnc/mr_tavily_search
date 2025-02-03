print("Loading mod.py for Tavily Search")

import os
from tavily import TavilyClient
from lib.providers.services import service
from lib.providers.commands import command
import trafilatura

tavily_client = TavilyClient(api_key=os.environ.get('TAVILY_API_KEY'))

@service()
async def web_search(query, num_results=5):
    """Perform a web search using Tavily API.

    Args:
        query (str): The search query.
        num_results (int, optional): The number of results to return. Defaults to 5.

    Returns:
        list: A list of dictionaries containing search results.
    """
    try:
        response = tavily_client.search(query)
        results = response.get('results', [])[:num_results]
        return [{'title': r['title'], 
                'link': r['url'], 
                'snippet': r['content']} for r in results]
    except Exception as e:
        print(f"Error in web search: {str(e)}")
        return []

def fetch_and_extract(url):
    """Fetch and extract the main content from a given URL using trafilatura.

    Args:
        url (str): The URL to fetch and extract content from.

    Returns:
        str: The extracted main content of the webpage, or None if extraction fails.
    """
    downloaded = trafilatura.fetch_url(url)
    if downloaded is None:
        return None
    content = trafilatura.extract(downloaded, include_comments=False, 
                                include_tables=True, no_fallback=False)
    return content

@command()
async def search_web(query, num_results=15, fetch_first=False, context=None):
    """Perform a web search and return the results.

    Args:
        query (str): The search query.
        num_results (int, optional): The number of results to return. Defaults to 15.
        fetch_first (bool, optional): Whether to fetch the content of the first result. Defaults to False.
        context (object, optional): The context object for the current session.

    Returns:
        str: Formatted string containing search results and optionally the content of the first result.

    Example:
        [
            { "search_web": { "query": "Python programming", "num_results": 3, "fetch_first": true } }
        ]
    """
    try:
        search_results = await web_search(query, num_results)
        if not search_results:
            return "No results found. Please check your search query."
        
        formatted_results = []
        for result in search_results:
            formatted_result = f"Title: {result['title']}\nLink: {result['link']}\nDescription: {result['snippet']}"
            if fetch_first and len(formatted_results) == 0:
                content = fetch_and_extract(result['link'])
                if content:
                    formatted_result += f"\n\nExtracted Full Content:\n{content[:500]}..."
            formatted_results.append(formatted_result)
        
        return "\n\n".join(formatted_results)
    except Exception as e:
        return f"Error performing web search: {str(e)}"

@command()
async def fetch_webpage(url, context=None):
    """Fetch and extract the main content from a given URL.

    Args:
        url (str): The URL to fetch and extract content from.
        context (object, optional): The context object for the current session.

    Returns:
        str: The extracted main content of the webpage, or an error message if extraction fails.

    Example:
        [
            { "fetch_webpage": { "url": "https://www.example.com/article" } }
        ]
    """
    content = fetch_and_extract(url)
    if content is None:
        return f"Failed to fetch or extract content from {url}"
    return f"Extracted content from {url}:\n\n{content}"

if __name__ == "__main__":
    # This block is for testing purposes
    import asyncio
    
    async def test_search():
        results = await search_web("Python programming", num_results=5, fetch_first=True)
        print(results)
    
    asyncio.run(test_search())

print("Loaded mod.py for Tavily Search")
