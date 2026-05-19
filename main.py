from src.Aeroplane import Aeroplane
from src.AeroplanesAPI import (
    AeroplanesAPI,
    filter_aeroplanes,
    get_aeroplanes_by_altitude,
    sort_aeroplanes,
    top_aeroplanes,
)
from src.JSONSaver import JSONSaver


def user_interaction():
    country = input("Введите название страны: ")
    top_n = int(input("Введите количество самолетов для вывода в топ N: "))
    filter_words = [
        word.lower()
        for word in input(
            "Введите названия стран для фильтрации по стране регистрации: "
        ).split()
    ]
    altitude_range = input("Введите диапазон высот полета: ")
    sort_choice = input(
        "По какому критерию сортировать? (1 - по высоте, 2 - по скорости): "
    )
    by_criterion = "velocity" if sort_choice == "2" else "altitude"

    api = AeroplanesAPI()
    raw_planes = api.get_aeroplanes(country)
    aeroplanes = Aeroplane.cast_to_object_list(raw_planes)

    filtered_aeroplanes = filter_aeroplanes(aeroplanes, filter_words)

    ranged_aeroplanes = get_aeroplanes_by_altitude(filtered_aeroplanes, altitude_range)
    sorted_aeroplanes = sort_aeroplanes(ranged_aeroplanes, by_criterion=by_criterion)

    final_top = top_aeroplanes(sorted_aeroplanes, top_n)
    print(f"\n--- ТОП {top_n} самолетов в диапазоне высот {altitude_range} ---")
    for plane in final_top:
        print(
            f"Рейс: {plane.callsign} | Страна регистрации: {plane.origin_country} | Высота: {plane.baro_altitude}м"
        )

    json_saver = JSONSaver()

    print("\n--- Доступные действия с файлом ---")
    print("1 - Сохранить найденный ТОП в файл")
    print("2 - Удалить первый самолет из ТОПа из файла (тест удаления)")
    print("0 - Выйти без изменений")

    choice = input("Выберите действие: ")

    if choice == "1":
        if final_top:
            for plane in final_top:
                json_saver.add_aeroplane(plane)
            print(f"Данные успешно сохранены в {json_saver.file_name}")
        else:
            print("Нечего сохранять, список пуст.")

    elif choice == "2":
        if final_top:
            target_plane = final_top[0]
            json_saver.delete_aeroplane(target_plane)
            print(
                f"Самый низкий самолет {target_plane.callsign} успешно удален из файла (если он там был)."
            )
        else:
            print("Список пуст, нечего удалять.")

    elif choice == "0" or choice == "":
        print("Выход из программы.")


if __name__ == "__main__":
    user_interaction()
