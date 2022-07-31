class City:
    def __init__ (self,city_name, city_state,coordinates):
        self.city = city_name
        self.state = city_state
        self.x = coordinates[0]
        self.y = coordinates[1]

    def __repr__(self):
        return f"Name:{self.city} State:{self.state} x:{self.x} y:{self.y}"

    def get_name(self):
        return self.city

    def get_state(self):
        return self.state

    def get_x(self):
        return self.x
    def get_y(self):
        return self.y