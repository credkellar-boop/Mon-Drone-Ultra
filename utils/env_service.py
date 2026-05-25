import datetime
import requests
from mavsdk import System

# Configuration
OPENWEATHER_API_KEY = "your_api_key_here"

async def get_system_context(drone: System):
    """
    Gathers precise time (from GPS) and weather (from API)
    to inject into the Gemini Agent's reasoning.
    """
    # 1. Atomic Time from GPS
    async for time in drone.telemetry.unix_epoch_time():
        dt = datetime.datetime.fromtimestamp(time.time_utc_us / 1_000_000)
        break
    
    # 2. Get Weather via OpenWeatherMap (using last known GPS position)
    async for pos in drone.telemetry.position():
        lat, lon = pos.latitude_deg, pos.longitude_deg
        break
    
    weather = "Unknown"
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={OPENWEATHER_API_KEY}"
        res = requests.get(url).json()
        weather = f"{res['weather'][0]['description']}, Wind: {res['wind']['speed']} m/s"
    except Exception as e:
        weather = "Service unavailable"

    return {
        "timestamp": dt.strftime("%Y-%m-%d %H:%M:%S"),
        "weather": weather
    }
