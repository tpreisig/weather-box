"""Reflex Weather App."""

import reflex as rx
from dotenv import load_dotenv
import os
import requests

load_dotenv()
API_KEY: str = os.getenv("API_KEY")
BASE_URL: str = "http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}"

class State(rx.State):
    """The app state."""
    city: str = ""
    weather_data: dict = {}
    
    """Update city input"""
    def get_city(self, name: str):
        self.city = name
    
    def fetch_weather(self):
        """Fetch weather data for the city"""
        url = BASE_URL.format(CITY=self.city, API_KEY=API_KEY)
        response = requests.get(url)
        data = response.json()
        if data.get("cod") == 200:
            self.weather_data = {
                "city": data["name"],
                "temp": round(data["main"]["temp"] - 273.15, 2),  # Convert Kelvin to Celsius and round
                "description": data["weather"][0]["description"].capitalize(),
            }



def index() -> rx.Component:
    """Main page component."""
    return rx.vstack(
        rx.color_mode.button(position="top-left"),
        rx.input(
            placeholder="Enter city name",
            value=State.city,
            on_change=State.get_city,
        ),
        rx.button(
            "Get Weather",
            on_click=State.fetch_weather,
        ),

        rx.cond(
            State.weather_data,
            rx.vstack(
                rx.text(f"City: {State.weather_data['city']}"),
                rx.text(f"Temperature: {State.weather_data['temp']}°C"),
                rx.text(f"Description: {State.weather_data['description']}"),
            ),
            rx.text("Enter a city to see the weather."),
        ),
        padding="1rem",
        align_items="center",
        width="30%",
        justify="center",
        margin="100px auto",
        background="rgba(59, 56, 220, 0.4)",
        border="1px solid white",
        border_radius="12px",
        box_shadow="0px 10px 30px rgba(140, 140, 140, 0.5)",
        min_width="200px"
        
    )


app = rx.App()
app.add_page(index)
