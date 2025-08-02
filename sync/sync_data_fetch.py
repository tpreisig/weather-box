import os
from dotenv import load_dotenv
import requests


load_dotenv()
API_KEY: str = os.getenv("API_KEY")
BASE_URL: str = "http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}"

def fetch_weather_data():
    if not API_KEY:
        raise ValueError("API_KEY is not set in the environment variables.")
    url = BASE_URL.format(CITY="Dubai", API_KEY=API_KEY)
    try:
        response = requests.get(url)
        data = response.json()
        if data.get("cod") == 200:
            print("success")
        print("")
        print(data)
        print("")
        print(f"Dubai: ➡️  Logitude: {data['coord']['lon']}, Latidude: {data['coord']['lat']}")
        print(f"Weather description: ➡️  {data['weather'][0]['description']}")
        print(f"Country: ➡️  {data['sys']['country']}")
    except Exception as e:
        print(f"An error occurred while fetching weather data: {e}")

fetch_weather_data()