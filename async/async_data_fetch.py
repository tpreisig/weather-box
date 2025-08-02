import aiohttp
import asyncio
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY: str = os.getenv("API_KEY")


async def fetch_url():
    url = f'http://api.openweathermap.org/data/2.5/weather?q=Dubai&appid={API_KEY}'
    try:
        async with aiohttp.ClientSession() as session:
            response = await session.get(url, timeout=10)
            if response.status != 200:
                error_message = await response.text()
                raise Exception(f"Request failed with status {response.status}: {error_message}")
            data = await response.json()
            return data
    except aiohttp.ClientError as e:
        raise Exception(f"Network error: {str(e)}")

if __name__ == "__main__":
    try:
        result = asyncio.run(fetch_url())
        print(result)
    except Exception as e:
        print(f"Error: {e}")
    