from abc import ABC, abstractmethod
import requests
import time
from urllib.parse import quote


class BaseAPI(ABC):
    '''Абстрактный класс, хранит URL'''

    def __init__(self, url):
        self.url = url

    @abstractmethod
    def get_info_about_country(self, country):
        pass

    @abstractmethod
    def get_info_about_plane(self, coordinates):
        pass


class AeroplanesAPI(BaseAPI):
    '''Класс, для выхова данных страны и координат самолета через URL'''

    def __init__(self, url_nominatim, url_opensky):
        super().__init__(url_nominatim)
        self.url_opensky = url_opensky

    def get_info_about_country(self, country):
        '''Метод запрашивает расположение страны'''
        url_country = (
            f"https://nominatim.openstreetmap.org/search?"
            f"q={quote(country)}&format=json"
        )
        try:
            response_about_country = requests.get(
                url_country,
                headers={"User-Agent": "my-app"}
            )
            time.sleep(1)
            if response_about_country.status_code != 200:
                return None
            else:
                data = response_about_country.json()
                if not data:
                    return None
                return data[0]["boundingbox"]
        except requests.RequestException:
            return None

    def get_info_about_plane(self, coordinates):
        '''Метод запрашивает координаты самолета'''
        if coordinates is None:
            return None
        else:
            url_coordinates = (
                f"https://opensky-network.org/api/states/all?"
                f"lamin={coordinates[0]}&lomin={coordinates[2]}"
                f"&lamax={coordinates[1]}&lomax={coordinates[3]}"
            )
            try:
                response_about_coordinates = requests.get(url_coordinates)
                if response_about_coordinates.status_code != 200:
                    return None
                else:
                    data = response_about_coordinates.json()
                    list_of_planes = []
                    states = data.get("states")
                    if states is None:
                        return []
                    for plane in states:
                        card = {
                            "callsign": plane[1],
                            "origin_country": plane[2],
                            "longitude": plane[5],
                            "latitude": plane[6],
                            "baro_altitude": plane[7],
                            "velocity": plane[9]
                        }
                        list_of_planes.append(card)
                    return list_of_planes
            except requests.RequestException:
                return None
