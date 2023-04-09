import matplotlib.pyplot as plt
import json
import math
import sys

import validate
from heater import Heater
import errors
import utils
from room import Room

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

    ## Temperatures
    # Starting room temperature
    d['room']['starting_temp'] = 22

    # Average sinusoidal temperature
    d['outside']['avg'] = (d['outside']['max_temp'] + d['outside']['min_temp']) / 2
    d['outside']['amp'] = d['outside']['max_temp'] - d['outside']['avg']

    ## Simulation run time
    d['run_time'] = 2 * 24 * 60 # Number of minutes in 2 days

    return d

def set_outdoor_temps(config):
    """Set outdoor temperatures for each minute of simulation.

    Inputs -
        config - input values for simulation
    Returns -
        list
    """
    temps = []

    if config['outside']['type'] == 'fixed':
        temps = config['run_time'] * [config['outside']['fixed_temp']]
    else:
        for i in range(config['run_time']):
            temps.append(
                config['outside']['amp'] * math.cos(2*math.pi*i/1440 - 300) + config['outside']['avg']
            )

    return temps

def main():
    # Load user defined values
    config = load_config()

    # Process user values, convert non-metric values if needed
    inputs = preprocess_values(config)

    # Set up room and it's initial conditions
    room = Room(inputs['room']['starting_temp'])

    # Set up heater and determine if it should be on or off
    heater = Heater(inputs['room']['thermostat_temp'], False)
    heater.set_status(room.temp)

    # Outdoor temperatures
    o_temps = set_outdoor_temps(inputs)

    # Run simulation
    times   = list(range(inputs['run_time']))
    r_temps = []
    h_stats = []
    for i in times:
        # Set/check status of heater
        heater.set_status(room.temp)

        # Calculate heat gain/loss and adjust room temp
        delta = room.heat_change(inputs, heater, o_temps[i])
        room.add_delta_temp(delta)

        r_temps.append(room.temp)
        h_stats.append(1 if heater.on else 0)

    if inputs['units']['temperature'] == 'f':
        r_temps = [utils.celsius_to_fahrenheit(v) for v in r_temps]
        o_temps = [utils.celsius_to_fahrenheit(v) for v in o_temps]
        inputs['room']['thermostat_temp'] = utils.celsius_to_fahrenheit(inputs['room']['thermostat_temp'])

    plt.plot(times, o_temps, 'k-', label='Outdoor Temp')
    plt.plot(times, r_temps, 'r-', label='Room Temp')
    plt.plot(times, h_stats, 'g-', label='Heater status')

    plt.show()

    return None

if __name__ == '__main__':
    main()
