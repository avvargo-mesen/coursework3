CREATE TABLE countries
(
country_id SERIAL PRIMARY KEY,
country_name varchar(100) UNIQUE,
country_latitude real,
country_longitude real
);



CREATE TABLE aeroplanes
(
aeroplane_id SERIAL PRIMARY KEY,
callsign varchar(50),
origin_country varchar(100),
velocity real,
baro_altitude real,
latitude real,
longitude real,
country_id integer REFERENCES countries(country_id)
);