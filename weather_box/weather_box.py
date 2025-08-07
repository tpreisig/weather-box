"""Reflex Weather App."""

import reflex as rx
import aiohttp
import asyncio
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY: str = os.getenv("API_KEY")
if not API_KEY:
    print("Error: API_KEY not found in environment variables")
    exit(1)
BASE_URL: str = "http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}"

class State(rx.State):
    """The app state."""
    city: str = ""
    weather_data: dict = {}

    def update_city(self, value: str):
        """Update city input."""
        self.city = value

    async def fetch_weather(self):
        """Asynchronously fetch weather data for the city."""
        url = BASE_URL.format(CITY=self.city, API_KEY=API_KEY)
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()
                        if data.get("cod") == 200:
                            self.weather_data = {
                                "city": data["name"],
                                "temp": round(data["main"]["temp"] - 273.15, 2),  # Convert Kelvin to Celsius and round
                                "description": data["weather"][0]["description"].capitalize(),
                            }
                        else:
                            self.weather_data = {"error": f"API error: {data.get('message')}"}
                    else:
                        self.weather_data = {"error": f"HTTP error: Status code {response.status}"}
            except aiohttp.ClientError as e:
                self.weather_data = {"error": f"Request error: {str(e)}"}

def index() -> rx.Component:
    """Main page component."""
    return rx.center(
        rx.vstack(
            rx.color_mode.button(position="top-left"),
            rx.heading("Weather App ⛈️ ☀️"),
            rx.input(
                placeholder="Enter city name",
                value=State.city,
                on_change=State.update_city,
            ),
            rx.button(
                "Check Weather",
                on_click=State.fetch_weather,
                background=rx.color_mode_cond(light="rgb(180, 229, 13)", dark="slateblue"),
                color=rx.color_mode_cond(light="darkslateblue", dark="white"),
                box_shadow="0 6px 30px rgba(255, 255, 255, 0.3)"
            ),
            rx.cond(
                State.weather_data,
                rx.cond(
                    State.weather_data.get("error"),
                    rx.text(State.weather_data["error"]),
                    rx.vstack(
                        rx.text(f"City: {State.weather_data['city']}"),
                        rx.text(f"Temperature: {State.weather_data['temp']}°C"),
                        rx.text(f"Description: {State.weather_data['description']}"),
                    ),
                ),
                rx.text("Enter a city to see the weather."),
            ),
            padding="1rem",
            align_items="center",
            margin="100px auto",
            background="rgba(59, 56, 220, 0.4)",
            border="1px solid white",
            border_radius="12px",
            box_shadow="0px 10px 30px rgba(140, 140, 140, 0.5)",
            min_width="200px"
        )
    )

app = rx.App()
app.add_page(index)