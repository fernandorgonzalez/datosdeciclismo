from os import environ
import settings

WDIR = environ["WDIR"]

input_file_name = WDIR + 'strava.csv'
output_file_name = WDIR + 'actividades.csv'

tipos = {'Ride','VirtualRide'}

file_in = open(input_file_name)
file_out = open(output_file_name, 'w')

next(file_in)

i = 1

file_out.write('id,fecha,año,mes,dia,tipo,altura,cadencia,distancia,potencia,pulsaciones,tiempo,velocidad,atleta_id' + '\n')

for line in file_in:
    
    line  = line.strip('\n')
    line = line.split(';')
    
    id = str(i)
    #start_date_local
    año = line[11][:4]
    mes = line[11][5:7]
    dia = line[11][8:10]
    fecha = año + mes + dia
    #type
    tipo = line[6]
    #total_elevation_gain
    altura = line[5]
    if altura == '':
        altura = '0'
    #average_cadence
    cadencia = line[37]
    if cadencia == '':
        cadencia = '0'
    #distance
    distancia = str(round(float(line[2])/1000,2))
    if distancia == '':
        distancia = '0'
    #average_watts
    potencia = line[38]
    if potencia == '':
        potencia = '0'
    #average_heartrate
    pulsaciones = line[43]
    if pulsaciones == '' or pulsaciones == 'False':
        pulsaciones = '0'
    #elapsed_time
    tiempo = line[4]
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
