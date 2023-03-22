import utils

class Room:
    def __init__(self, temp):
        self.temp = temp

    def __str__(self):
        return f'Room temperature: {self.temp}'

    def heat_gain(self, heater):
        """Rate of thermal energy gained by the room."""
        if heater.on:
            return round(
                utils.HEATER_AIR_MASS * utils.AIR_SPECIFIC_HEAT * (utils.HEATER_TEMP - self.temp),
                2
            )
        else:
            return 0

    def heat_loss(self, conf, outside_temp):
        """Rate of thermal energy lost from room to outside."""
        return round(
            (self.temp - outside_temp) / conf['R_effective'],
            2
        )

    def heat_change(self, conf, heater, outside_temp):
        gain = self.heat_gain(heater)
        loss = self.heat_loss(conf, outside_temp)
        return round(
            (gain - loss) / (conf['air_mass'] * utils.AIR_SPECIFIC_HEAT),
            2
        )

    def add_delta_temp(self, delta):
        self.temp = round(self.temp + delta, 2)

