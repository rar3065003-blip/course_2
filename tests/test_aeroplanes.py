import os
from unittest.mock import MagicMock


from src.Aeroplane import Aeroplane
from src.AeroplanesAPI import (
    filter_aeroplanes,
    get_aeroplanes_by_altitude,
    sort_aeroplanes,
    top_aeroplanes,
)
from src.API_request import NominatimAPI, OpenSkyAPI
from src.JSONSaver import JSONSaver


def test_aeroplane_all_methods():
    """Тестируем ВСЕ методы класса Aeroplane, включая перевод списков"""
    # 1. Конструктор и сравнение
    p1 = Aeroplane("POL1", "Poland", 100.0, 2000.0)
    p2 = Aeroplane("ESP2", "Spain", 200.0, 8000.0)
    p3 = Aeroplane("NONE", "NoneCountry", None, None)  # Тест защиты от None

    assert p1 < p2
    assert (p1 == p1) is True
    assert p3 < p1

    # 2. Метод cast_to_object_list (запускаем реальный код!)
    raw_data = [
        [
            "4b1",
            "SWR1",
            "Switzerland",
            0,
            0,
            0,
            0,
            4000.0,
            False,
            150.0,
            0,
            0,
            None,
            4000.0,
            "20",
            False,
            0,
        ]
    ]
    objects = Aeroplane.cast_to_object_list(raw_data)
    assert len(objects) == 1
    assert Aeroplane.cast_to_object_list(None) == []


def test_all_filtering_and_sorting_functions():
    """Запускаем реальный код всех функций фильтрации и сортировки"""
    p1 = Aeroplane("LOW", "Poland", 100.0, 2000.0)
    p2 = Aeroplane("HIGH", "Spain", 300.0, 10000.0)
    planes = [p1, p2]

    # Фильтр стран
    assert len(filter_aeroplanes(planes, ["poland"])) == 1
    assert len(filter_aeroplanes(planes, [])) == 2  # Пустой ввод

    # Фильтр высоты
    assert len(get_aeroplanes_by_altitude(planes, "1000-5000")) == 1
    assert len(get_aeroplanes_by_altitude(planes, "1000 5000")) == 1  # Через пробел
    assert len(get_aeroplanes_by_altitude(planes, "кривой_ввод")) == 2  # Ошибка ввода

    # Сортировка и Топ
    assert sort_aeroplanes(planes, "velocity")[0].callsign == "HIGH"
    assert sort_aeroplanes(planes, "altitude")[0].callsign == "HIGH"  # DESC сортировка
    assert len(top_aeroplanes(planes, 1)) == 1


def test_json_saver_real_file():
    """Тестируем РЕАЛЬНЫЙ код добавления и удаления в JSONSaver"""
    test_file = "data/test_real_planes.json"
    saver = JSONSaver(file_name=test_file)
    plane = Aeroplane("REAL999", "Test", 300.0, 9000.0)

    # Прогоняем через реальный код добавления
    saver.add_aeroplane(plane)
    assert os.path.exists(test_file) is True

    # Прогоняем через реальный код удаления
    saver.delete_aeroplane(plane)

    # Чистим за собой
    if os.path.exists(test_file):
        os.remove(test_file)


def test_api_responses_real_code():
    """Тестируем РЕАЛЬНЫЙ код методов response в API классах"""
    # 1. Тест NominatimAPI.response
    geo_api = NominatimAPI()
    fake_geo_response = MagicMock()
    fake_geo_response.json.return_value = [{"lat": "52.2", "lon": "19.1"}]

    res_geo = geo_api.response(fake_geo_response)
    assert res_geo["lat"] == 52.2

    # Тест защиты Nominatim от пустой страны
    fake_geo_response.json.return_value = []
    assert geo_api.response(fake_geo_response) == {}

    # 2. Тест OpenSkyAPI.response
    sky_api = OpenSkyAPI()
    fake_sky_response = MagicMock()
    fake_sky_response.json.return_value = {
        "states": [
            [
                "1",
                "C1",
                "Poland",
                0,
                0,
                0,
                0,
                3000.0,
                False,
                150.0,
                0,
                0,
                None,
                3000.0,
                "2",
                False,
                0,
            ]
        ]
    }

    res_sky = sky_api.response(fake_sky_response)
    assert len(res_sky) == 1
