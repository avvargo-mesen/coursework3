import os
from dotenv import load_dotenv
from src.db_manager import DBManager
from src.api import AeroplanesAPI
from src.utils import read_countries



def main():
    """ Cобирает данные и запускает методы DBManager"""
    load_dotenv()
    api = AeroplanesAPI("https://nominatim.openstreetmap.org",
        "https://opensky-network.org")
    host=os.getenv("DB_HOST")
    port = int(os.getenv("DB_PORT"))
    database = os.getenv("DB_NAME")
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    db = DBManager(host=host, port=port, database=database, user=user, password=password)

    db.clear_tables()

    countries = read_countries()

    for country in countries:
        coordinates = api.get_info_about_country(country)
        if coordinates is None:
            continue
        latitude = float(coordinates[0])
        longitude = float(coordinates[2])
        db.insert_country(country, latitude, longitude)

    for country in countries:
        country_id = db.get_country_id_by_name(country)
        if country_id is None:
            continue
        coordinates = api.get_info_about_country(country)
        if coordinates is None:
            continue
        planes = api.get_info_about_plane(coordinates)
        if not planes:
            continue

        for plane in planes:
            db.insert_aeroplane(plane["callsign"], plane["origin_country"], plane["velocity"], plane["baro_altitude"], plane["latitude"], plane["longitude"], country_id)

    count = db.get_countries_and_aeroplanes_count()
    aeroplanes = db.get_all_aeroplanes()
    avg_speed = db.get_avg_speed()
    higher_speed = db.get_aeroplanes_with_higher_speed()
    keyword = db.get_aeroplanes_with_keyword('ACA')

    print(count)
    print(aeroplanes)
    print(avg_speed)
    print(higher_speed)
    print(keyword)

if __name__ == "__main__":
    main()