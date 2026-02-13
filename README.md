# mr_tavily_search

MindRoot plugin for web search using the Tavily API.

## Overview

This plugin provides web search capabilities for MindRoot agents using the Tavily API. For webpage content extraction, use the companion **mr_crawl4ai** plugin which provides better extraction with JavaScript support.

## Features

- **search_web** - Perform web searches and return results from Tavily

## Installation

```bash
cd /xfiles/upd3/mr_tavily_search
pip install -e .
```

Set your Tavily API key as an environment variable:
```bash
export TAVILY_API_KEY=your_api_key_here
```

## Commands

### search_web

Perform a web search and return results.

```json
{ "search_web": { "query": "Python programming", "num_results": 5 } }
```

**Parameters:**
- `query` (required) - The search query
- `num_results` (optional) - Number of results to return (default: 15)
- `search_depth` (optional) - 'basic' (faster) or 'advanced' (deeper) (default: 'basic')
- `include_images` (optional) - Include image results (default: false)

**Returns:** Search results from Tavily API.

## Related Plugins

For webpage content extraction, use **mr_crawl4ai** instead:
- `fetch_webpage` - Extract clean markdown from a single URL
- `crawl_site` - Deep crawl entire websites

mr_crawl4ai provides superior extraction using a real browser (JavaScript support, better handling of dynamic content).

## Dependencies

- langchain-tavily
- tavily-python
- nanoid

## License

Apache 2.0
