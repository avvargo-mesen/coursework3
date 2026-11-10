import psycopg2

class DBManager:
    def __init__(self, host, port, database, user, password):
        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = password
        self.connection = psycopg2.connect(
            host=self.host,
            port=self.port,
            database=self.database,
            user=self.user,
            password=self.password
        )
        self.cursor = self.connection.cursor()

    def insert_country(self, name, latitude, longitude):
        '''Метод отправляет в таблицу названия, долготу и широту страны'''
        self.cursor.execute(
            "INSERT INTO countries (country_name, country_latitude, country_longitude) VALUES (%s, %s, %s)",
            (name, latitude, longitude)
        )
        self.connection.commit()

    def get_country_id_by_name(self, name):
        '''Метод отправляет в таблицу имя страны и выводит id страны'''
        self.cursor.execute(
            "SELECT country_id FROM countries WHERE country_name = %s",
            (name,)
        )
        country_id_by_name = self.cursor.fetchone()
        if country_id_by_name is None:
            return None
        else:
            return country_id_by_name[0]


    def insert_aeroplane(self, callsign, origin_country, velocity, baro_altitude, latitude, longitude, country_id):
        '''Метод добавляет самолёт в таблицу aeroplanes'''

        self.cursor.execute(
            "INSERT INTO aeroplanes (callsign, origin_country, velocity, baro_altitude, latitude, longitude, country_id)" 
            "VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (callsign, origin_country, velocity, baro_altitude, latitude, longitude, country_id)
        )
        self.connection.commit()

    def get_countries_and_aeroplanes_count(self):
        '''Метод возвращает список всех стран и количество самолётов'''
        self.cursor.execute(
            "SELECT country_name, COUNT(aeroplane_id) FROM countries LEFT JOIN aeroplanes USING(country_id)" 
            "GROUP BY country_name")

        return self.cursor.fetchall()

    def get_all_aeroplanes(self):
        '''Метод возвращает список всех самолётов'''
        self.cursor.execute("SELECT * FROM aeroplanes")
        return self.cursor.fetchall()

    def get_avg_speed(self):
        '''Метод возвращает среднюю скорость по всем самолётам'''
        self.cursor.execute(
            "SELECT AVG(velocity) FROM aeroplanes")
        result = self.cursor.fetchone()
        return result[0]

    def get_aeroplanes_with_higher_speed(self):
        '''Метод возвращает самолёты со скоростью выше средней'''
        self.cursor.execute("SELECT * FROM aeroplanes WHERE velocity > (SELECT AVG(velocity) FROM aeroplanes)")
        return self.cursor.fetchall()

    def get_aeroplanes_with_keyword(self, keyword):
        '''Метод возвращает список самолетов по позывному'''
        self.cursor.execute("SELECT * FROM aeroplanes WHERE callsign ILIKE %s", ('%' + keyword + '%',))
        return self.cursor.fetchall()

    def clear_tables(self):
        '''Метод очищает базы данных'''
        self.cursor.execute("TRUNCATE aeroplanes, countries")
        self.connection.commit()
