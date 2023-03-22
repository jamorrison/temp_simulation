import errors
import utils

# TODO: change boundary values for thermostat
# TODO: should I change boundary values for outside temperatures also?
def validate(d):
    """Validate input values from config file.

    Inputs -
        d - dict from json.load
    Returns -
        d (may be corrected if values understood but need modification)
    Errors -
        errors.MissingKeyError
        errors.InvalidValueError
    """
    ## Check all keys exist
    # Outer keys
    for k in ['room', 'window', 'units', 'outside']:
        if k not in d.keys():
            raise errors.MissingKeyError(f'Could not find key: {k}')

    # Inner keys
    for k in ['width', 'depth', 'height', 'wall_thickness', 'thermostat_temp']:
        if k not in d['room'].keys():
            raise errors.MissingKeyError(f'Could not find room key: {k}')
    for k in ['width', 'height', 'thickness']:
        if k not in d['window'].keys():
            raise errors.MissingKeyError(f'Could not find window key: {k}')
    for k in ['length', 'temperature']:
        if k not in d['units'].keys():
            raise errors.MissingKeyError(f'Could not find units key: {k}')
    for k in ['type', 'fixed_temp', 'min_temp', 'max_temp']:
        if k not in d['outside'].keys():
            raise errors.MissingKeyError(f'Could not find outside key: {k}')

    ## Check provided values are valid
    # Check units
    if d['units']['length'].lower() not in ['meters', 'feet', 'm', 'ft']:
        raise errors.InvalidValueError('Length units must be "meters", "feet", "m", or "ft"')
    if d['units']['temperature'].lower() not in ['celsius', 'fahrenheit', 'c', 'f']:
        raise errors.InvalidValueError('Temperature units must be "celsius", "fahrenheit", "C", or "F"')

    # Make the units consistent for reference in code
    d['units']['length'] = d['units']['length'].lower()
    d['units']['temperature'] = d['units']['temperature'].lower()

    if d['units']['length'] == 'meters':
        d['units']['length'] = 'm'
    elif d['units']['length'] == 'feet':
        d['units']['length'] = 'ft'
    if d['units']['temperature'] == 'celsius':
        d['units']['temperature'] = 'c'
    elif d['units']['temperature'] == 'fahrenheit':
        d['units']['temperature'] = 'f'

    # Room and window dimensions
    if d['room']['width'] < utils.ALMOST_ZERO:
        raise errors.InvalidValueError('Room width must be > 0')
    if d['room']['depth'] < utils.ALMOST_ZERO:
        raise errors.InvalidValueError('Room depth must be > 0')
    if d['room']['height'] < utils.ALMOST_ZERO:
        raise errors.InvalidValueError('Room height must be > 0')
    if d['room']['wall_thickness'] < utils.ALMOST_ZERO:
        raise errors.InvalidValueError('Room wall thickness must be > 0')
    if d['window']['width'] < utils.ALMOST_ZERO:
        raise errors.InvalidValueError('Window width must be > 0')
    if d['window']['height'] < utils.ALMOST_ZERO:
        raise errors.InvalidValueError('Window height must be > 0')
    if d['window']['thickness'] < utils.ALMOST_ZERO:
        raise errors.InvalidValueError('Window thickness must be > 0')

    # Temperatures
    if d['units']['temperature'] == 'f':
        if d['room']['thermostat_temp'] < 14 or d['room']['thermostat_temp'] > 104:
            raise errors.InvalidValueError('Room thermostat temperature (F) must be in range [14, 104], inclusive')
        if d['outside']['fixed_temp'] < -4 or d['room']['thermostat_temp'] > 122:
            raise errors.InvalidValueError('Outside fixed temperature (F) must be in range [-4, 122], inclusive')
        if d['outside']['min_temp'] < -4 or d['outside']['min_temp'] > 122:
            raise errors.InvalidValueError('Outside minimum temperature (F) must be in range [-4, 122], inclusive')
        if d['outside']['max_temp'] < -4 or d['outside']['max_temp'] > 122:
            raise errors.InvalidValueError('Outside maximum temperature (F) must be in range [-4, 122], inclusive')
    else:
        if d['room']['thermostat_temp'] < -10 or d['room']['thermostat_temp'] > 40:
            raise errors.InvalidValueError('Room thermostat temperature (C) must be in range [-10, 40], inclusive')
        if d['outside']['fixed_temp'] < -20 or d['room']['thermostat_temp'] > 122:
            raise errors.InvalidValueError('Outside fixed temperature (C) must be in range [-20, 50], inclusive')
        if d['outside']['min_temp'] < -20 or d['outside']['min_temp'] > 50:
            raise errors.InvalidValueError('Outside minimum temperature (C) must be in range [-20, 50], inclusive')
        if d['outside']['max_temp'] < -20 or d['outside']['max_temp'] > 50:
            raise errors.InvalidValueError('Outside maximum temperature (C) must be in range [-20, 50], inclusive')

    return d

