from os import environ
import settings

WDIR = environ["WDIR"]

input_file_name = WDIR + 'strava.csv'
output_file_name = WDIR + 'actividades.csv'

tipos = {'Ride','VirtualRide'}

file_in = open(input_file_name)
file_out = open(output_file_name, 'w')


row = next(file_in)
row  = row.strip('\n')
row = row.split(';')

for r in range(0,61):
    
    if row[r] == 'start_date_local':
        start_date_local = r
        
    if row[r] == 'type':
        type = r

    if row[r] == 'total_elevation_gain':
        total_elevation_gain= r
    
    if row[r] == 'average_cadence':
        average_cadence = r

    if row[r] == 'distance':
        distance = r
    
    if row[r] == 'average_watts':
        average_watts = r
        
    if row[r] == 'average_heartrate':
        average_heartrate = r    

    if row[r] == 'elapsed_time':
        elapsed_time = r          

i = 1

file_out.write('id,fecha,año,mes,dia,tipo,altura,cadencia,distancia,potencia,pulsaciones,tiempo,velocidad,atleta_id' + '\n')

for line in file_in:
    
    line  = line.strip('\n')
    line = line.split(';')
    
    id = str(i)
    #start_date_local
    año = line[start_date_local][:4]
    mes = line[start_date_local][5:7]
    dia = line[start_date_local][8:10]
    fecha = año + mes + dia
    #type
    tipo = line[type]
    #total_elevation_gain
    altura = line[total_elevation_gain]
    if altura == '':
        altura = '0'
    #average_cadence
    cadencia = line[average_cadence]
    if cadencia == '':
        cadencia = '0'
    #distance
    distancia = str(round(float(line[distance])/1000,2))
    if distancia == '':
        distancia = '0'
    #average_watts
    potencia = line[average_watts]
    if potencia == '':
        potencia = '0'
    #average_heartrate
    pulsaciones = line[average_heartrate]
    if pulsaciones == '' or pulsaciones == 'False':
        pulsaciones = '0'
    #elapsed_time
    tiempo = line[elapsed_time]
    if tiempo == '':
        tiempo = '0'
    try:
        velocidad = str(round(float(distancia)/(float(tiempo)/3600),2))
    except:
        velocidad = 0
    #atleta_id
    atleta_id = line[60]
    
    if tipo in tipos:

        tipo = tipo.replace("VirtualRide","Virtual")        
        tipo = tipo.replace("Ride","Ruta")
                    
        file_out.write(id + ',' + fecha + ',' + año + ',' + mes + ',' + dia + ',' + tipo + ',' + altura + ',' + cadencia + ',' + distancia + ',' + potencia + ',' + pulsaciones + ',' + tiempo + ',' + velocidad + ',' + atleta_id + '\n')
        
        i+=1
    
file_in.close()
file_out.close()
