#!/usr/bin/env python3
"""
Updates siddik_hero_banner.svg with the current Dhaka time, date, and weather.
Run manually with: python3 scripts/update_banner.py
Meant to be run on a schedule via GitHub Actions (see .github/workflows/update-banner.yml).
"""
import re
import sys
from datetime import datetime
from zoneinfo import ZoneInfo

import requests

SVG_PATH = "siddik_hero_banner.svg"
LAT, LON = 23.8103, 90.4125  # Dhaka

WEATHER_ICONS = {
    "Sunny": "☀️", "Clear": "☀️", "Partly cloudy": "⛅",
    "Cloudy": "☁️", "Overcast": "☁️", "Mist": "🌫️", "Fog": "🌫️",
    "Patchy rain possible": "🌦️", "Light rain": "🌧️", "Moderate rain": "🌧️",
    "Heavy rain": "🌧️", "Thundery outbreaks possible": "⛈️",
}


def get_time_strings():
    now = datetime.now(ZoneInfo("Asia/Dhaka"))
    time_str = now.strftime("%I:%M:%S")
    ampm = now.strftime("%p")
    date_str = now.strftime("%A, %d %b %Y")
    return time_str, ampm, date_str


def get_weather_string():
    try:
        resp = requests.get(f"https://wttr.in/Dhaka?format=j1", timeout=10)
        resp.raise_for_status()
        data = resp.json()
        current = data["current_condition"][0]
        temp_c = current["temp_C"]
        desc = current["weatherDesc"][0]["value"]
        icon = WEATHER_ICONS.get(desc, "🌤️")
        return f"{icon} {temp_c}°C, {desc}"
    except Exception as e:
        print(f"Weather fetch failed: {e}", file=sys.stderr)
        return "🌤️ Weather unavailable"


def main():
    with open(SVG_PATH, "r", encoding="utf-8") as f:
        svg = f.read()

    time_str, ampm, date_str = get_time_strings()
    weather_str = get_weather_string()

    # If placeholders exist (first run), replace them directly.
    # On subsequent runs, replace whatever values are currently baked in.
    svg = re.sub(r"\{\{TIME\}\}|\d{2}:\d{2}:\d{2}", time_str, svg, count=1)
    svg = re.sub(r"\{\{AMPM\}\}|\bAM\b|\bPM\b", ampm, svg, count=1)
    svg = re.sub(
        r"\{\{DATE\}\}|[A-Za-z]+day, \d{1,2} [A-Za-z]{3} \d{4}",
        date_str,
        svg,
        count=1,
    )
    svg = svg.replace("{{WEATHER}}", weather_str)

    with open(SVG_PATH, "w", encoding="utf-8") as f:
        f.write(svg)

    print(f"Updated banner: {time_str} {ampm}, {date_str}, {weather_str}")


if __name__ == "__main__":
    main()
