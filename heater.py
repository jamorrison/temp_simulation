class Heater:
    def __init__(self, temp, on):
        self.temp = temp
        self.on   = on

    def __str__(self):
        return f'Thermostat temperature: {self.temp}, On?: {self.on}'

    def set_status(self, room_temp):
        """Set whether the heater is turned on or off."""
        if room_temp < self.temp-1:
            self.on = True
        elif room_temp > self.temp+1:
            self.on = False
