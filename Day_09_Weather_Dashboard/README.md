# Day 09 - Weather Dashboard

This project is a command-line weather dashboard that fetches live weather data for a specified city using the Open-Meteo API and displays it in a clean, readable format.

## Features

- **Current Weather:** Displays current temperature, humidity, apparent temperature, precipitation, cloud cover, wind speed, and more.
- **Hourly Forecast:** Provides a brief hourly forecast for key weather parameters.
- **City Geocoding:** Converts city names into geographical coordinates using the `geopy` library.

## Installation

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/Haris-Ahmed83/30-day-python-challenge.git
    cd 30-day-python-challenge/Day_09_Weather_Dashboard
    ```

2.  **Create a virtual environment (recommended):**

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install dependencies:**

    ```bash
    pip install requests-cache pandas openmeteo-requests geopy
    ```

## Usage

Run the script from your terminal and enter the city name when prompted:

```bash
python weather_dashboard.py
```

Example:

```
Enter city name: London
Fetching weather for London (51.5073219, -0.1276474)...

--- Current Weather ---
Time: 2026-03-03 10:00 GMT
Temperature (2m): 8.5°C
Apparent Temperature: 6.1°C
Relative Humidity (2m): 87.0 %
Precipitation: 0.0 mm
Rain: 0.0 mm
Showers: 0.0 mm
Snowfall: 0.0 cm
Weather Code: 3
Cloud Cover: 100.0 %
Pressure (MSL): 1018.5 hPa
Wind Speed (10m): 10.1 km/h
Wind Direction (10m): 288.0°
Wind Gusts (10m): 18.0 km/h
Is Day: Yes

--- Hourly Forecast ---
                 Date  Temperature (2m)  Relative Humidity (2m)  Apparent Temperature  Weather Code  Wind Speed (10m)
0 2026-03-03 00:00:00               7.9                    93.0                   5.5           3.0              10.1
1 2026-03-03 01:00:00               7.7                    94.0                   5.3           3.0               9.7
2 2026-03-03 02:00:00               7.5                    95.0                   5.1           3.0               9.4
3 2026-03-03 03:00:00               7.3                    95.0                   4.9           3.0               9.0
4 2026-03-03 04:00:00               7.1                    96.0                   4.7           3.0               8.6
...
```

## API Reference

- **Open-Meteo API:** [https://open-meteo.com/](https://open-meteo.com/)
- **geopy:** [https://geopy.readthedocs.io/](https://geopy.readthedocs.io/)

---
*Created by Manus AI*
