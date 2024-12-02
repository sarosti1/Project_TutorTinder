async function fetchWeather() {
    const city = document.getElementById("city-input").value;
    const response = await fetch(`/api/weather/${city}`);
    if (response.ok) {
        const data = await response.json();
        document.getElementById("weather-data").innerHTML = `
            <h3>Weather in ${data.name}</h3>
            <p>Temperature: ${data.main.temp} °C</p>
            <p>Condition: ${data.weather[0].description}</p>
        `;
    } else {
        document.getElementById("weather-data").innerText = "City not found!";
    }
}

async function loadFavorites() {
    const response = await fetch("/api/favorites");
    const data = await response.json();
    const favoritesList = document.getElementById("favorites-list");
    favoritesList.innerHTML = data.favorites.map(city => `
        <li>${city} <button onclick="deleteFavorite('${city}')">Remove</button></li>
    `).join("");
}

async function addFavorite(city) {
    await fetch("/api/favorites", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ city })
    });
    loadFavorites();
}

async function deleteFavorite(city) {
    await fetch(`/api/favorites/${city}`, {
        method: "DELETE"
    });
    loadFavorites();
}
