from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import httpx
import sqlite3
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI()

# Setup Jinja2 templates
templates = Jinja2Templates(directory="templates")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# OpenWeather API Key
API_KEY = os.getenv("OPENWEATHER_API_KEY")

# Optional Database Setup
DB_FILE = "weatherhub.db"

def setup_database():
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS favorite_cities (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                city_name TEXT UNIQUE
            )
        """)
        conn.commit()

setup_database()

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Render the home page."""
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/api/weather/{city}")
async def get_weather(city: str):
    """Fetch weather data from OpenWeather API."""
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="City not found")
    return response.json()

@app.get("/api/favorites")
def get_favorites():
    """Retrieve favorite cities."""
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT city_name FROM favorite_cities")
        cities = [row[0] for row in cursor.fetchall()]
    return {"favorites": cities}

@app.post("/api/favorites")
def add_favorite(city: str):
    """Add a city to favorites."""
    try:
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO favorite_cities (city_name) VALUES (?)", (city,))
            conn.commit()
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="City already in favorites")
    return {"message": f"{city} added to favorites"}

@app.delete("/api/favorites/{city}")
def delete_favorite(city: str):
    """Remove a city from favorites."""
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM favorite_cities WHERE city_name = ?", (city,))
        conn.commit()
    return {"message": f"{city} removed from favorites"}
