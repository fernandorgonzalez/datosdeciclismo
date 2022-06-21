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

file = open(WDIR + 'actividades.csv', encoding='utf-8')

next(file)

for line in file:
    
    line  = line.strip('\n')
    line = line.split(',')
    
    id_ = line[0]
    fecha = line[1]
    año = line[2]
    mes = line[3]
    dia = line[4]
    tipo = line[5]
    altura = line[6]
    cadencia = line[7]
    distancia = line[8]
    potencia = line[9]
    pulsaciones = line[10]
    tiempo = line[11]
    velocidad = line[12]
    atleta_id = line[13]

    print(id_)
    
    query = "INSERT INTO APP_ACTIVIDADES(id, fecha, año, mes, dia, tipo, altura, cadencia, distancia, potencia, pulsaciones, tiempo, velocidad, atleta_id) VALUES  (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

    cursor.execute(query, (id_,fecha,año,mes,dia,tipo,altura,cadencia,distancia,potencia,pulsaciones,tiempo,velocidad,atleta_id))

conexion.commit()

cursor.close()
conexion.close()

