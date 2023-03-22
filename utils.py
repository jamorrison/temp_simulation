# Constants
ALMOST_ZERO = 0.000001

AIR_DENSITY = 1.293 # kg / m^3

K_FIBERGLASS = 136.8 # thermal conductivity of fiberglass [joule / (meter*hour*degree)]
K_GLASS = 2808 # thermal conductivity of glass [joule / (meter*hour*degree)]

HEATER_AIR_MASS = 3600 # mass of air passing through heater [kilogram / hour]
HEATER_TEMP = 50 # [degree Celsius]

AIR_SPECIFIC_HEAT = 1005.4 # specific heat of air [joule / (kilogram*degree C)]

KEYS = """
Format of config file with valid inputs:

{
    "units": {
        "length": "meters" or "feet" (also accepts m or ft),
        "temperature": "celsius" or "fahrenheit" (also accepts C or F)
    },
    "room": {
        "width": float (> 0),
        "depth": float (> 0),
        "height": float (> 0),
        "wall_thickness": float (> 0),
        "thermostat_temp": float (-10 <= degrees C <= 40, 14 <= degrees F <= 104)
    },
    "window": {
        "width": float (> 0),
        "height": float (> 0),
        "thickness": float (> 0),
    },
    "outside": {
        "type": "fixed" or "sinusoidal",
        "fixed_temp": float (-20 <= degrees C <= 50, -4 <= degrees F <= 122)
        "min_temp": float (-20 <= degrees C <= 50, -4 <= degrees F <= 122),
        "max_temp": float (-20 <= degrees C <= 50, -4 <= degrees F <= 122)
    }
}
"""

# Functions
def feet_to_meters(ft):
    """Convert feet into meters."""
    return 0.3048 * ft

def meters_to_feet(m):
    """Convert meters into feet."""
    return 3.28084 * m

def fahrenheit_to_celsius(f):
    """Convert degrees Fahrenheit to degrees Celsius."""
    return 5 * (f - 32) / 9

def celsius_to_fahrenheit(c):
    """Convert degrees Celsius to degrees Fahrenheit."""
    return 9 * c / 5 + 32
