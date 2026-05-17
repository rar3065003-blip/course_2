from abc import ABC, abstractmethod
import requests
from requests import Response
from typing import Any


class API(ABC):
    @abstractmethod
    def request(self, url:str , key: str| None) -> Response:
        pass
    @abstractmethod
    def response(self, raw_response: Response) -> Any:
        pass

class NominatimAPI(API):

    def request(self, url:str , key: str|None) -> Response:
        response: Response = requests.get(url, headers={'User-Agent': 'MyEducationalApp'})
        return response

    def response(self, raw_response: Response) -> dict:
        data = raw_response.json()
        country_info = data[0]
        lat = float(country_info["lat"])
        lon = float(country_info["lon"])
        return {"lat": lat, "lon": lon}

class OpenSkyAPI(API):

    def request(self, url:str, key: str|None) -> Response:
        response: Response = requests.get(url, headers={'User-Agent': 'MyEducationalApp'})
        return response

    def response(self, raw_response:Response) -> list|None:
        data = raw_response.json()
        planes = data.get("states")
        return planes
