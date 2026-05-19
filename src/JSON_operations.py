from src.Aeroplane import Aeroplane
import json

class JSONSaver:
    def __init__(self, file_name: str = "aeroplanes.json"):
        self.file_name = file_name

    def add_aeroplane(self, aeroplane: Aeroplane):
        plane_dict = {"callsign": aeroplane.callsign,
                      "origin_country": aeroplane.origin_country,
                      "velocity": aeroplane.velocity,
                      "baro_altitude": aeroplane.baro_altitude
                      }
        try:
            with open(self.file_name, "r", encoding="utf=8") as f:
                list_aeroplanes = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            list_aeroplanes = []

        list_aeroplanes.append(plane_dict)

        with open(self.file_name, "w", encoding="utf-8") as f:
            json.dump(list_aeroplanes, f, indent=4, ensure_ascii=False)

    def delete_aeroplane(self, aeroplane: Aeroplane):
        try:
            with open(self.file_name, "r", encoding="utf-8") as f:
                list_aeroplanes = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            list_aeroplanes = []

        new_list = [plane for plane in list_aeroplanes if plane["callsign"] != aeroplane.callsign]

        with open (self.file_name, "w", encoding="utf-8") as f:
            json.dump(new_list, f, indent=4, ensure_ascii=False)



