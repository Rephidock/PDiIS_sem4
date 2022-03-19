from zeroplayer.entities.resource import Resource


class Wheat(Resource):
    _decay_speed_start = 1
    _decay_acceleration = 0.25


class Grass(Resource):
    _decay_speed_start = -2  # negative decay == growth
    _decay_acceleration = 1
