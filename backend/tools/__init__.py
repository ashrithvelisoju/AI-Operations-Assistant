"""
Tools module - API integrations for the AI Operations Assistant
"""
from .weather_tool import WeatherTool, weather_tool
from .news_tool import NewsTool, news_tool

# Tool registry for easy access
AVAILABLE_TOOLS = {
    "weather": weather_tool,
    "news": news_tool
}

TOOL_DESCRIPTIONS = {
    "weather": WeatherTool.description,
    "news": NewsTool.description
}

__all__ = [
    "WeatherTool", "weather_tool",
    "NewsTool", "news_tool", 
    "AVAILABLE_TOOLS", "TOOL_DESCRIPTIONS"
]
