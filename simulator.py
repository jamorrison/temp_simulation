import json
import sys

import validate
import heater
import errors
import utils
import room

def load_config():
    """Load config JSON file."""
    with open('config.json') as fh:
        out = json.load(fh)

    try:
        out = validate.validate(out)
    except errors.MissingKeyError as e:
        print(utils.KEYS)
        print(e)
        sys.exit(1)

    return out

def preprocess_values(d):
    """Calculate necessary variables and convert non-metric units.

    Inputs -
        d - validated config dict
    Returns -
        dict
    """
    ## Convert non-metric values to metric
    # Feet to meters
    if d['units']['length'] == 'ft':
        d['room']['width']          = utils.feet_to_meters(d['room']['width'])
        d['room']['depth']          = utils.feet_to_meters(d['room']['depth'])
        d['room']['height']         = utils.feet_to_meters(d['room']['height'])
        d['room']['wall_thickness'] = utils.feet_to_meters(d['room']['wall_thickness'])

        d['window']['width']     = utils.feet_to_meters(d['window']['width'])
        d['window']['height']    = utils.feet_to_meters(d['window']['height'])
        d['window']['thickness'] = utils.feet_to_meters(d['window']['thickness'])

    # Fahrenheit to Celsius
    if d['units']['temperature'] == 'f':
        d['room']['thermostat_temp'] = utils.fahrenheit_to_celsius(d['room']['thermostat_temp'])
        d['outside']['fixed_temp']   = utils.fahrenheit_to_celsius(d['outside']['fixed_temp'])
        d['outside']['min_temp']     = utils.fahrenheit_to_celsius(d['outside']['min_temp'])
        d['outside']['max_temp']     = utils.fahrenheit_to_celsius(d['outside']['max_temp'])

    ## Calculate air mass
    # Room volume
    V = d['room']['width'] * d['room']['depth'] * d['room']['height']

    # Air mass
    d['air_mass'] = V * utils.AIR_DENSITY

    ## Calculate R values [D / kA, thickness / (conductivity*area)]
    # Wall surface area (assumes no loss through floor or ceiling)
    A_wall = 2 * d['room']['width'] * d['room']['height'] + 2 * d['room']['depth'] * d['room']['height']

    # Window surface area
    A_window = d['window']['width'] * d['window']['height']

    # Wall R value
    R_wall = d['room']['wall_thickness'] / (utils.K_FIBERGLASS * A_wall)

    # Window R value
    R_window = d['window']['thickness'] / (utils.K_GLASS * A_window)

    # Effective R value
    d['R_effective'] = (R_wall * R_window) / (R_wall + R_window)

    ## Starting temperature of room
    d['room']['starting_temp'] = 22

    ## Simulation run time
    d['run_time'] = 2 * 24 * 60 # Number of minutes in 2 days

    return d

def main():
    # Load user defined values
    config = load_config()

    # Process user values, convert non-metric values if needed
    input_values = preprocess_values(config)

    # TODO: start implementing the actual heat transfer
    # Set up room and it's initial conditions
    room = room.Room(input_values['room']['starting_temp'])

    # Set up heater and determine if it should be on or off
    heater = heater.Heater(input_values['room']['thermostat_temp'], False)
    heater.set_status(room.temp)

    # Setup outside temperatures for each minute of the simulation
    temps = []
    if input_values['outside']['type'] == 'fixed':
        temps = input_values['run_time'] * [input_values['outside']['fixed_temp']]

    return None

if __name__ == '__main__':
    main()
