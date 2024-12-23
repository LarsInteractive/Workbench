import math
import datetime
import pytz

# Helper function to calculate Julian Day from a calendar date
def julian_day(year, month, day):
    """ Calculate the Julian Day number for the given date. """
    if month <= 2:
        year -= 1
        month += 12
    A = math.floor(year / 100)
    B = 2 - A + math.floor(A / 4)
    # Julian day calculation formula
    return math.floor(365.25 * (year + 4716)) + math.floor(30.6001 * (month + 1)) + day + B - 1524.5

# Function to calculate the solar declination angle
def solar_declination(julian_day):
    """ Calculate the declination of the Sun given the Julian Day. """
    n = julian_day - 2451545.0  # Number of days since the reference epoch (January 1, 2000)
    
    # Mean longitude of the Sun (L), in degrees
    L = (280.46 + 0.9856474 * n) % 360
    
    # Mean anomaly of the Sun (g), in radians
    g = math.radians((357.528 + 0.9856003 * n) % 360)
    
    # Ecliptic longitude of the Sun (λ), in radians
    ecliptic_longitude = math.radians(L + 1.915 * math.sin(g) + 0.02 * math.sin(2 * g))
    
    # Solar declination, the angle between the rays of the Sun and Earth's equator
    return math.degrees(math.asin(0.39778 * math.sin(ecliptic_longitude)))

# Function to calculate the hour angle for sunrise/sunset
def hour_angle(latitude, declination):
    """ Calculate the hour angle for sunrise/sunset given latitude and solar declination. """
    lat_rad = math.radians(latitude)  # Convert latitude to radians
    decl_rad = math.radians(declination)  # Convert declination to radians
    
    # The hour angle is the angular distance the Earth needs to rotate before the Sun appears on the horizon
    return math.degrees(math.acos(-math.tan(lat_rad) * math.tan(decl_rad)))

# Function to calculate sunrise, sunset, and sunshine duration
def calculate_sun_times(latitude, longitude, date, timezone):
    """ Calculate sunrise, sunset, and sunshine duration for the given location and date. """
    
    # Step 1: Calculate Julian Day for the given date
    jd = julian_day(date.year, date.month, date.day)
    
    # Step 2: Calculate solar declination for the Julian Day
    declination = solar_declination(jd)
    
    # Step 3: Calculate solar noon in UTC (assumes no Daylight Saving Time)
    solar_noon_utc = 12 - (longitude / 15.0)  # Local solar noon depends on longitude
    
    # Step 4: Calculate the hour angle for sunrise/sunset
    h_angle = hour_angle(latitude, declination)
    
    # Step 5: Calculate sunrise and sunset times in UTC
    sunrise_utc = solar_noon_utc - (h_angle / 15.0)  # Convert hour angle to time
    sunset_utc = solar_noon_utc + (h_angle / 15.0)   # Convert hour angle to time
    
    # Step 6: Convert UTC times to local time using the provided timezone (handles CEST/CET)
    sunrise_local = datetime.datetime.combine(date, datetime.time(int(sunrise_utc), int((sunrise_utc % 1) * 60))).replace(tzinfo=pytz.utc).astimezone(timezone)
    sunset_local = datetime.datetime.combine(date, datetime.time(int(sunset_utc), int((sunset_utc % 1) * 60))).replace(tzinfo=pytz.utc).astimezone(timezone)
    
    # Step 7: Calculate the sunshine duration (sunset time - sunrise time)
    sunshine_duration = sunset_local - sunrise_local
    
    return sunrise_local, sunset_local, sunshine_duration

# Set the coordinates for Hamburg, Germany
latitude = 53.551086   # Latitude of Hamburg
longitude = 9.993682   # Longitude of Hamburg

# Set the timezone for Hamburg (handles both CET and CEST automatically)
hamburg_tz = pytz.timezone('Europe/Berlin')

# Get today's date
today = datetime.date.today()

# Calculate the sunrise, sunset, and sunshine duration for today's date
sunrise, sunset, sunshine_duration = calculate_sun_times(latitude, longitude, today, hamburg_tz)

# Print the results with explanations
print("Sunrise (local time):", sunrise.strftime("%H:%M:%S"))
print("Sunset (local time):", sunset.strftime("%H:%M:%S"))
print("Sunshine duration:", sunshine_duration)

# Explanation of printed values:
# - Sunrise (local time): The time of day when the sun rises in Hamburg, adjusted for the local time (CET/CEST).
# - Sunset (local time): The time of day when the sun sets in Hamburg, adjusted for the local time (CET/CEST).
# - Sunshine duration: The total duration between sunrise and sunset, indicating how long the sun is above the horizon.
