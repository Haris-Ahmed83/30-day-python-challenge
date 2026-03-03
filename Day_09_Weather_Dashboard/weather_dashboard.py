import openmeteo_requests
import requests_cache
import pandas as pd
from retry_requests import retry
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError

def get_coordinates(city_name):
    geolocator = Nominatim(user_agent="weather-dashboard-app")
    try:
        location = geolocator.geocode(city_name, timeout=10)
        if location:
            return location.latitude, location.longitude
        else:
            print(f"Could not find coordinates for {city_name}. Please try again.")
            return None, None
    except (GeocoderTimedOut, GeocoderServiceError) as e:
        print(f"Geocoding error for {city_name}: {e}")
        return None, None

def get_weather_data(latitude, longitude):
    cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
    openmeteo = openmeteo_requests.Client(session=retry_session)

    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": ["temperature_2m", "relative_humidity_2m", "apparent_temperature", "is_day", "precipitation", "rain", "showers", "snowfall", "weather_code", "cloud_cover", "pressure_msl", "surface_pressure", "wind_speed_10m", "wind_direction_10m", "wind_gusts_10m"],
        "hourly": ["temperature_2m", "relative_humidity_2m", "dew_point_2m", "apparent_temperature", "precipitation_probability", "precipitation", "rain", "showers", "snowfall", "snow_depth", "weather_code", "pressure_msl", "surface_pressure", "cloud_cover", "cloud_cover_low", "cloud_cover_mid", "cloud_cover_high", "visibility", "evapotranspiration", "et0_fao_evapotranspiration", "vapour_pressure_deficit", "wind_speed_10m", "wind_speed_80m", "wind_speed_120m", "wind_speed_180m", "wind_direction_10m", "wind_direction_80m", "wind_direction_120m", "wind_direction_180m", "wind_gusts_10m", "temperature_80m", "temperature_120m", "temperature_180m", "soil_temperature_0cm", "soil_temperature_6cm", "soil_temperature_18cm", "soil_temperature_54cm", "soil_moisture_0_to_1cm", "soil_moisture_1_to_3cm", "soil_moisture_3_to_9cm", "soil_moisture_9_to_27cm", "soil_moisture_27_to_81cm"],
        "timezone": "auto",
        "forecast_days": 1
    }
    responses = openmeteo.weather_api(url, params=params)
    return responses[0] if responses else None

def display_weather(response):
    if not response:
        print("No weather data to display.")
        return

    current = response.Current()
    current_data = {
        "Time": pd.to_datetime(current.Time(), unit="s", utc=True).tz_convert(response.Timezone()).strftime('%Y-%m-%d %H:%M %Z'),
        "Temperature (2m)": f"{current.Variables(0).Value()}°C",
        "Apparent Temperature": f"{current.Variables(2).Value()}°C",
        "Relative Humidity (2m)": f"{current.Variables(1).Value()} %",
        "Precipitation": f"{current.Variables(4).Value()} mm",
        "Rain": f"{current.Variables(5).Value()} mm",
        "Showers": f"{current.Variables(6).Value()} mm",
        "Snowfall": f"{current.Variables(7).Value()} cm",
        "Weather Code": current.Variables(8).Value(),
        "Cloud Cover": f"{current.Variables(9).Value()} %",
        "Pressure (MSL)": f"{current.Variables(10).Value()} hPa",
        "Wind Speed (10m)": f"{current.Variables(12).Value()} km/h",
        "Wind Direction (10m)": f"{current.Variables(13).Value()}°",
        "Wind Gusts (10m)": f"{current.Variables(14).Value()} km/h",
        "Is Day": "Yes" if current.Variables(3).Value() == 1 else "No"
    }

    print("\n--- Current Weather ---")
    for key, value in current_data.items():
        print(f"{key}: {value}")

    hourly = response.Hourly()
    hourly_data = {
        "Date": pd.date_range(
            start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
            end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
            freq=pd.Timedelta(seconds=hourly.Interval()),
            inclusive="left"
        ).tz_convert(response.Timezone()),
        "Temperature (2m)": hourly.Variables(0).ValuesAsNumpy(),
        "Relative Humidity (2m)": hourly.Variables(1).ValuesAsNumpy(),
        "Apparent Temperature": hourly.Variables(3).ValuesAsNumpy(),
        "Weather Code": hourly.Variables(10).ValuesAsNumpy(),
        "Wind Speed (10m)": hourly.Variables(21).ValuesAsNumpy()
    }
    hourly_dataframe = pd.DataFrame(data=hourly_data)
    print("\n--- Hourly Forecast ---")
    print(hourly_dataframe.head())

if __name__ == "__main__":
    city = input("Enter city name: ")
    if city:
        latitude, longitude = get_coordinates(city)
        if latitude is not None and longitude is not None:
            print(f"Fetching weather for {city} ({latitude}, {longitude})...")
            weather_response = get_weather_data(latitude, longitude)
            display_weather(weather_response)
    else:
        print("City name cannot be empty.")
