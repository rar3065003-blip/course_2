from src.API_request import NominatimAPI, OpenSkyAPI
import os
from dotenv import load_dotenv

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


if __name__ == "__main__":
    # 1. Создаем наш главный инструмент-диспетчер
    api = AeroplanesAPI()

    # 2. Вызываем метод для поиска самолетов над Испанией
    # (Код сам внутри найдет координаты, создаст квадрат и сделает запрос к OpenSky)
    result = api.get_aeroplanes("Spain")

    # 3. Смотрим, что получилось
    print("Итоговый список самолетов:")
    print(result)
