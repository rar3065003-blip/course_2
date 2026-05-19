from src.AeroplanesAPI import AeroplanesAPI, filter_aeroplanes, get_aeroplanes_by_altitude, sort_aeroplanes, top_aeroplanes
from src.Aeroplane import Aeroplane
from src.JSONSaver import JSONSaver

def user_interaction():
    country = input("Введите название страны: ")
    top_n = int(input("Введите количество самолетов для вывода в топ N: "))
    filter_words = [word.lower() for word in input("Введите названия стран для фильтрации по стране регистрации: ").split()]
    altitude_range = input("Введите диапазон высот полета: ")

    api = AeroplanesAPI()
    raw_planes = api.get_aeroplanes(country)
    aeroplanes = Aeroplane.cast_to_object_list(raw_planes)

    filtered_aeroplanes = filter_aeroplanes(aeroplanes, filter_words)

    ranged_aeroplanes = get_aeroplanes_by_altitude(filtered_aeroplanes, altitude_range)

    sorted_aeroplanes = sort_aeroplanes(ranged_aeroplanes)

    final_top = top_aeroplanes(sorted_aeroplanes, top_n)
    print(f"\n--- ТОП {top_n} самолетов в диапазоне высот {altitude_range} ---")
    for plane in final_top:
        print(f"Рейс: {plane.callsign} | Страна регистрации: {plane.origin_country} | Высота: {plane.baro_altitude}м")

if __name__ == "__main__":
    user_interaction()