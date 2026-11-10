

def read_countries():
    """Функция читает countries.txt и возвращает список стран"""
    with open("countries.txt", "r", encoding="utf-8") as file:
        countries = []
        for country in file:
            if country.strip() != "":
                countries.append(country.strip())
    return countries


