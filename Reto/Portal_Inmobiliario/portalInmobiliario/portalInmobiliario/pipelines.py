# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import psycopg2
from psycopg2 import Error


class PortalinmobiliarioPipeline(object):
    
    connection = None
    cur = None
        
    
    
    def open_spider(self, spider):
        # hostname="host.docker.internal"
        hostname = "localhost"
        database="Propiedades"
        username="postgres"
        password="Nesmar$31"
        
        try:
            self.connection = psycopg2.connect(host=hostname, user=username, password=password, dbname=database)
            print("PostgreSQL server information")
            print(self.connection.get_dsn_parameters(), "\n")
            
            self.cur = self.connection.cursor()
            record = self.cur.fetchone()
            print("You are connected to - ", record, "\n")
            
            
        except (Exception, Error) as error:
            print("Error while connecting to PostgreSQL", error)
            
        
        

    def close_spider(self, spider):
        self.cur.close()
        self.connection.close()
        print("PostgreSQL connection is closed")
    
    def process_item(self, item, spider):
        try:
            self.cur.execute("insert into propiedades(nombre, precio, vendedor, codigo, superficie_total, superficie_util, ambientes, dormitorios, baños, estacionamientos, orientacion, antiguedad, gastos, latitud, longitud) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(item['nombre'], item['precio'], item['vendedor'], item['codigo'], item['supTotal'], item['supUtil'], item['ambientes'], item['dormitorios'], item['baños'], item['estacionamientos'], item['orientacion'], item['antiguedad'], item['gastos'], item['latitud'], item['longitud']))
            self.connection.commit()
            print ('\nfinished INSERT INTO execution')
            
            
        except (Exception, Error) as error2:
            print("\nexecute_sql() error:", error2)
            self.connection.rollback()
            
        return item
