import requests

GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
WEATHER_URL = "https://api.open-meteo.com/v1/forecast"

def execute(arguments: dict):
    city = arguments.get("city")
    if not city:
        return {"error": "Weather error"}

    try:
        geo_response = requests.get(
            GEOCODING_URL,
            params={"name": city, "count": 1},
            timeout=10,
        )
        geo_response.raise_for_status()
        geo_data = geo_response.json()

        if "results" not in geo_data or not geo_data["results"]:
            return {"error": "City not found"}

        location = geo_data["results"][0]
        latitude = location["latitude"]
        longitude = location["longitude"]
        city_name = location.get("name", city)
        country = location.get("country", "")

        weather_response = requests.get(
            WEATHER_URL,
            params={
                "latitude": latitude,
                "longitude": longitude,
                "current_weather": True,
            },
            timeout=10,
        )
        weather_response.raise_for_status()
        weather_data = weather_response.json()

        current_weather = weather_data.get("current_weather")
        if not current_weather:
            return {"error": "Current weather unavailable"}

        temperature = current_weather["temperature"]
        windspeed = current_weather["windspeed"]
        weather_code = current_weather["weathercode"]

        return (
            f"City: {city_name}, {country}\n"
            f"Temperature: {temperature}°C\n"
            f"Wind Speed: {windspeed} km/h\n"
            f"Weather Code: {weather_code}"
        )
    except Exception as e:
        return {"error": f"Weather error: {e}"}


if __name__ == "__main__":
    print("weather tool\n")
    print(
        execute(
            {
                "city": "Gurugram",
            }
        )
    )