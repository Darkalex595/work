# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import psycopg2
from psycopg2 import Error



class RealtorPipeline(object):
    
    connection = None
    cur = None
    
    
    def open_spider(self, spider):
        hostname = "localhost"
        database="Realtor"
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
    
    def process_item(self, item, spider):
        try:
            self.cur.execute("insert into publicaciones_usa(prov_id, id_publicacion_scrapper, id_publicacion_proveedor, codigo_publicacion, codigo_proyecto, codigo_unidad, nombre_unidad, pais_id, id_zona_administrativa, nombre, direccion, descripcion, publicacion_link, tipo_propiedad, estado_uso, tipo_transaccion, dormitorios, banios, piso, estacionamientos, bodegas, amoblado, superficie_util, superficie_terraza, superficie_total, precio_bodegas, precio_estacionamientos, precio_total, tipo_moneda, fecha_publicacion, email, telefono, id_vendedor, vendedor, inmobiliaria, constructora, rango_entrega, anio_entrega, mes_entrega, latitud, longitud, agregada_el, actualizada_el, dormitorios_studio, banios_ducha, fuente_precio_total, estado_lista, anio_construccion, detalle_anio_construccion) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(item["prov_id"], item["id_publication_scraper"], item["id_publication_provider"], item["publication_code"], item["project_code"], item["unit_code"], item["unit_name"], item["country_id"], item["id_admin_zone"], item["name"], item["address"], item["description"], item["publication_link"], item["property_type"], item["use_state"], item["transaction_type"], item["bedrooms"], item["bathrooms"], item["floors"], item["garage"], item["warehouse"], item["furnished"], item["util_area"], item["terrace_area"], item["total_area"], item["warehouse_price"], item["garage_price"], item["total_price"], item["currency_type"], item["publication_date"], item["email"], item["phone"], item["seller_id"], item["seller"], item["real_state_name"], item["construction_company"], item["delivery_range"], item["delivery_year"], item["delivery_month"], item["latitude"], item["longitude"], item["add_date"], item["updated_date"], item["studio"], item["full_baths"], item["source_total_price"], item["state_list"], item["build_year"], item["build_year_detail"]))
            self.connection.commit()
            print ('\nfinished INSERT INTO execution')
            
            
        except (Exception, Error) as error2:
            print("\nexecute_sql() error:", error2)
            self.connection.rollback()
            
        return item
    
    def close_spider(self, spider):
        self.cur.close()
        self.connection.close()
        print("PostgreSQL connection is closed")
