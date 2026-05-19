from src.API_request import NominatimAPI, OpenSkyAPI
import os
from dotenv import load_dotenv
from src.Aeroplane import Aeroplane

load_dotenv()


class AeroplanesAPI():
    def __init__(self) -> None:
        self.nominatim = NominatimAPI()
        self.opensky = OpenSkyAPI()

    def get_aeroplanes(self, country_name:str) -> list|None:
        url_geo = f"https://nominatim.openstreetmap.org/search?country={country_name}&format=json"
        raw_geo = self.nominatim.request(url_geo, key=None)
        coordinates = self.nominatim.response(raw_geo)
        print(coordinates)
        lat = coordinates["lat"]
        lon = coordinates["lon"]
        lamin = lat - 5
        lamax = lat + 5
        lomin = lon - 5
        lomax = lon + 5
        url_sky = f"https://opensky-network.org/api/states/all?lamin={lamin}&lomin={lomin}&lamax={lamax}&lomax={lomax}"
        user = os.getenv("OPENSKY_USER")
        password = os.getenv("OPENSKY_PASSWORD")
        my_credentials = f"{user}:{password}"
        raw_sky = self.opensky.request(url_sky, key=my_credentials)
        planes = self.opensky.response(raw_sky)
        return planes

def filter_aeroplanes(aeroplanes:list[Aeroplane], filter_words: list[str]) -> list[Aeroplane]:
    user_request = []
    for plane in aeroplanes:
        if plane.origin_country in filter_words:
            user_request.append(plane)
    return user_request

def get_aeroplanes_by_altitude(aeroplanes:list[Aeroplane], altitude_range: str) -> list[Aeroplane]:
    parts = altitude_range.split('-')
    min_alt = float(parts[0])
    max_alt = float(parts[1])
    user_request_planes = []
    for plane in aeroplanes:
        if plane.baro_altitude is not None and min_alt <= plane.baro_altitude <= max_alt:
            user_request_planes.append(plane)
    return user_request_planes

def sort_aeroplanes(aeroplanes: list[Aeroplane])-> list[Aeroplane] :
    request_ranged_aeroplanes = sorted(aeroplanes, key=lambda plane:plane.baro_altitude)
    return request_ranged_aeroplanes

def get_top_aeroplanes(aeroplanes: list[Aeroplane], top_n:int) -> list[Aeroplane]:
    user_request_list = aeroplanes[:top_n]
    return user_request_list





if __name__ == "__main__":
    api = AeroplanesAPI()
    # 1. Получаем сырые данные из интернета (как и раньше)
    raw_planes = api.get_aeroplanes("Poland")

    # 2. Вызываем ТВОЙ метод для превращения их в объекты!
    # Не забудь импортировать класс Aeroplane в этот файл
    aeroplanes_objects = Aeroplane.cast_to_object_list(raw_planes)

    # 3. Давай выведем для проверки первый самолет из списка объектов
    if aeroplanes_objects:
        first_plane = aeroplanes_objects[0]
        print("Данные первого объекта-самолета:")
        print(f"Рейс: {first_plane.callsign}, Страна: {first_plane.origin_country}, Скорость: {first_plane.velocity}")