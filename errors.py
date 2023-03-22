class MissingKeyError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return f'MissingKeyError: {self.message}'

class InvalidValueError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return f'InvalidValueError: {self.message}'
