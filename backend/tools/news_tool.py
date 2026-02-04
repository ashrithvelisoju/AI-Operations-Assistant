"""
News Tool - NewsAPI.org Integration
"""
import os
import requests
from dotenv import load_dotenv

load_dotenv()


class NewsTool:
    """Tool for fetching news articles from NewsAPI"""
    
    name = "news"
    description = "Get latest news articles on a topic or from top headlines. Input: search query or 'headlines' for top news"
    
    def __init__(self):
        self.api_key = os.environ.get("NEWS_API_KEY")
        self.base_url = "https://newsapi.org/v2"
    
    def execute(self, query: str, count: int = 5) -> dict:
        """
        Fetch news articles based on query
        
        Args:
            query: Search term or 'headlines' for top headlines
            count: Number of articles to return (default 5)
            
        Returns:
            dict with news articles or error
        """
        try:
            if query.lower() == "headlines":
                url = f"{self.base_url}/top-headlines"
                params = {
                    "apiKey": self.api_key,
                    "country": "us",
                    "pageSize": count
                }
            else:
                url = f"{self.base_url}/everything"
                params = {
                    "apiKey": self.api_key,
                    "q": query,
                    "pageSize": count,
                    "sortBy": "publishedAt",
                    "language": "en"
                }
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                articles = []
                
                for article in data.get("articles", [])[:count]:
                    articles.append({
                        "title": article.get("title"),
                        "source": article.get("source", {}).get("name"),
                        "description": article.get("description"),
                        "url": article.get("url"),
                        "published_at": article.get("publishedAt")
                    })
                
                return {
                    "success": True,
                    "query": query,
                    "total_results": data.get("totalResults", 0),
                    "articles": articles
                }
            elif response.status_code == 401:
                return {"success": False, "error": "Invalid API key"}
            elif response.status_code == 429:
                return {"success": False, "error": "Rate limit exceeded"}
            else:
                return {"success": False, "error": f"API error: {response.status_code}"}
                
        except requests.exceptions.Timeout:
            return {"success": False, "error": "Request timed out"}
        except requests.exceptions.RequestException as e:
            return {"success": False, "error": str(e)}


# Singleton instance
news_tool = NewsTool()
