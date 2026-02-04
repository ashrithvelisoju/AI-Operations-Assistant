"""
Weather Tool - OpenWeatherMap API Integration
"""
import os
import requests
from dotenv import load_dotenv

load_dotenv()


class WeatherTool:
    """Tool for fetching weather data from OpenWeatherMap API"""
    
    name = "weather"
    description = "Get current weather information for a city. Input: city name (e.g., 'London', 'New York')"
    
    def __init__(self):
        self.api_key = os.environ.get("WEATHER_API_KEY")
        self.base_url = "https://api.openweathermap.org/data/2.5/weather"
    
    def execute(self, city: str) -> dict:
        """
        Fetch current weather for a given city
        
        Args:
            city: Name of the city to get weather for
            
        Returns:
            dict with weather information or error
        """
        try:
            params = {
                "q": city,
                "appid": self.api_key,
                "units": "metric"
            }
            
            response = requests.get(self.base_url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "success": True,
                    "city": data.get("name"),
                    "country": data.get("sys", {}).get("country"),
                    "temperature": data.get("main", {}).get("temp"),
                    "feels_like": data.get("main", {}).get("feels_like"),
                    "humidity": data.get("main", {}).get("humidity"),
                    "description": data.get("weather", [{}])[0].get("description"),
                    "wind_speed": data.get("wind", {}).get("speed"),
                    "pressure": data.get("main", {}).get("pressure")
                }
            elif response.status_code == 404:
                return {"success": False, "error": f"City '{city}' not found"}
            else:
                return {"success": False, "error": f"API error: {response.status_code}"}
                
        except requests.exceptions.Timeout:
            return {"success": False, "error": "Request timed out"}
        except requests.exceptions.RequestException as e:
            return {"success": False, "error": str(e)}


# Singleton instance
weather_tool = WeatherTool()
