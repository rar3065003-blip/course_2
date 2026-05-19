

class Aeroplane:

    def __init__(self, callsign:str, origin_country:str, velocity:float|None, baro_altitude:float|None):
        self.callsign = callsign
        self.origin_country = origin_country
        self.velocity = velocity
        self.baro_altitude = baro_altitude

    @classmethod
    def cast_to_object_list(cls, aeroplanes_list:list|None) -> list:
        if aeroplanes_list is None:
            return []

        object_list = []
        for plane in aeroplanes_list:
            callsign = plane[1]
            origin_country = plane[2]
            baro_altitude = plane[7]
            velocity = plane[9]
            new_plane_object = cls(callsign, origin_country, velocity, baro_altitude)
            object_list.append(new_plane_object)
        return object_list