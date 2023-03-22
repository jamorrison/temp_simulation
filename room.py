import utils

class Room:
    def __init__(self, temp):
        self.temp = temp

    def __str__(self):
        return f'Room temperature: {self.temp}'

    def heat_gain(self, heater):
        """Rate of thermal energy gained by the room."""
        if heater.on:
            return utils.HEATER_AIR_MASS * utils.AIR_SPECIFIC_HEAT * (utils.HEATER_TEMP - self.temp)
        else:
            return 0

    def heat_loss(self, config, outside_temp):
        """Rate of thermal energy lost from room to outside."""
        return (self.temp - outside_temp) / config['R_effective']

    def heat_change(self, config, heater, outside_temp):
        return (heat_gain(heater) - heat_loss(config, outside_temp)) / (config['air_mass'] * utils.AIR_SPECIFIC_HEAT)

