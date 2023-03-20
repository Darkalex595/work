import psycopg2
from psycopg2 import Error
from const import HOSTNAME, USERNAME, PASSWORD, DATABASE



def insert_into_db(property_id, list_id, list_date, stories, beds, studio, area, area_tot, garage, description, agent, office, address, bathroom, full_baths, latitude, longitude, price, unit, year_built):
    
    connection = psycopg2.connect(host=HOSTNAME, user=USERNAME, password=PASSWORD, dbname=DATABASE)
    
    cursor = connection.cursor()
    try:
        cursor.execute("INSERT INTO compras_usa (property_id, list_id, stories, beds, studio, useful_area, total_area, garage_spaces, description, agent, office, address, bathrooms, full_baths, latitude, longitude, total_price, unit_name, year_built, list_date) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (property_id, list_id, stories, beds, studio, area, area_tot, garage, description, agent, office, address, bathroom, full_baths, latitude, longitude, price, unit, year_built, list_date))
        connection.commit()
        print ('\nfinished INSERT INTO execution')
        
    except (Exception, Error) as error2:
            print("\nexecute_sql() error:", error2)
            connection.rollback()

    cursor.close()