
import json
from geocoder import ip
from pathlib import Path
from httpx import Client
from datetime import datetime, timedelta

BASE_DIR = Path(__file__).resolve().parent

# HTTP client setup
client = Client(
    timeout=5,  # Increased timeout for reliability
    http2=True,
    follow_redirects=True,
    headers={"Accept-Language": "en-US,en;q=0.9"},
)

def get_timings_from_api(lat, lng, date_str):
    """Fetches prayer timings for a specific date from the Al-Adhan API."""
    url = f"https://api.aladhan.com/v1/timings/{date_str}?latitude={lat}&longitude={lng}&method=4"
    try:
        response = client.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
        return response.json()["data"]["timings"]
    except Exception as e:
        print(f"API request failed for date {date_str}: {e}")
        return None

def conv_time_12h(time_str):
    """Converts 24-hour time string to 12-hour format."""
    if not isinstance(time_str, str):
        # If it's already a time object, format it
        return time_str.strftime("%I:%M %p")
    
    # Handle time strings like "HH:MM" or "HH:MM:SS"
    for fmt in ('%H:%M', '%H:%M:%S'):
        try:
            time_obj = datetime.strptime(time_str, fmt)
            return time_obj.strftime("%I:%M %p")
        except ValueError:
            continue
    return f"Time Format Error -> {time_str}"

def qyam_calc(start_night, end_night, city='--------'):
    """Calculates the night periods based on start and end times."""
    # Ensure times are in 24-hour format for calculation
    start_night_dt = datetime.strptime(start_night, "%H:%M")
    end_night_dt = datetime.strptime(end_night, "%H:%M")

    # If end night is earlier than start night, it means it's on the next day
    if end_night_dt <= start_night_dt:
        end_night_dt += timedelta(days=1)

    duration = end_night_dt - start_night_dt
    sixth = duration / 6
    midnight = (start_night_dt + duration / 2).time()
    last_third = (start_night_dt + (sixth * 4)).time()
    last_sixth = (start_night_dt + (sixth * 5)).time()
    
    calculation = {
        'city': city,
        "allnight": str(duration),
        "start_night": conv_time_12h(start_night),
        "midnight": conv_time_12h(midnight),
        "start_off_last_third": conv_time_12h(last_third),
        "start_off_last_sixth": conv_time_12h(last_sixth),
        "end_night": conv_time_12h(end_night)
    }
    return calculation

def qyam_times(start, end):
    """
    Main function to get Qiyam times. It handles both automatic (based on prayer names)
    and manual (based on user-provided times) calculations.
    """
    # Mapping for automatic time calculation
    auto_times_map = {
        'المغرب': 'Sunset',
        'العشاء': 'Isha',
        'الشروق': 'Sunrise',
        'الفجر': 'Fajr'
    }

    # Handle manual time input
    if start not in auto_times_map or end not in auto_times_map:
        return qyam_calc(start, end)

    # --- Handle automatic time calculation ---
    try:
        # Get location
        ip_location = ip('me')
        if not ip_location.latlng:
             raise ValueError("Could not determine location from IP.")
        lat, lng = ip_location.latlng
        city = ip_location.city or "Unknown Location"

        # Get dates
        today = datetime.now()
        tomorrow = today + timedelta(days=1)
        
        # Get timings from API
        today_timings = get_timings_from_api(lat, lng, today.strftime('%d-%m-%Y'))
        tomorrow_timings = get_timings_from_api(lat, lng, tomorrow.strftime('%d-%m-%Y'))

        if not today_timings or not tomorrow_timings:
            raise ConnectionError("Failed to fetch prayer times from the API.")

        # Extract start and end times (in HH:MM format)
        start_time_24h = today_timings[auto_times_map[start]].split(' ')[0]
        end_time_24h = tomorrow_timings[auto_times_map[end]].split(' ')[0]
        
        # Perform calculation
        return qyam_calc(start_time_24h, end_time_24h, city=city)

    except Exception as err:
        print(f"An error occurred in qyam_times: {err}")
        return {
            'city': "Problem occurred\nNo internet or location update needed",
            "allnight": "00:00:00",
            "start_night": "00:00:00",
            "midnight": "00:00:00",
            "start_off_last_third": "00:00:00",
            "start_off_last_sixth": "00:00:00",
            "end_night": "00:00:00",
        }
