import settings
from os import environ
import psycopg2

DB_HOST = environ["DB_HOST"]
DB_NAME = environ["DB_NAME"]
DB_USER = environ["DB_USER"]
DB_PASSWORD = environ["DB_PASSWORD"]

WDIR = environ["WDIR"]

conexion = psycopg2.connect(host=DB_HOST,dbname=DB_NAME,user=DB_USER,  password=DB_PASSWORD)

cursor = conexion.cursor()

query = 'DELETE FROM APP_ACTIVIDADES'

cursor.execute(query)

archivo = open(WDIR + 'actividades.csv', encoding='utf-8')

for linea in archivo:
    
    linea  = linea.strip('\n')
    lista = linea.split(',')
    
    id_ = lista[0]
    fecha = lista[1]
    año = lista[2]
    mes = lista[3]
    dia = lista[4]
    tipo = lista[5]
    altura = lista[6]
    cadencia = lista[7]
    distancia = lista[8]
    potencia = lista[9]
    pulsaciones = lista[10]
    tiempo = lista[11]
    velocidad = lista[12]
    atleta_id = lista[13]
    
    print(id_)
    
    query = "INSERT INTO APP_ACTIVIDADES(id, fecha, año, mes, dia, tipo, altura, cadencia, distancia, potencia, pulsaciones, tiempo, velocidad, atleta_id) VALUES  (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

    cursor.execute(query, (id_,fecha,año,mes,dia,tipo,altura,cadencia,distancia,potencia,pulsaciones,tiempo,velocidad,atleta_id))

conexion.commit()

cursor.close()
conexion.close()

