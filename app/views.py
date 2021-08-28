from .filters import actividades_filter
from .models import *
from decouple import config
from django import forms
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from django.contrib.auth.views import PasswordChangeView
from django.db.models import Avg
from django.db.models import CharField
from django.db.models import Count
from django.db.models import F
from django.db.models import FloatField
from django.db.models import Min
from django.db.models import Sum
from django.db.models import Value
from django.forms import formset_factory
from django.forms import inlineformset_factory
from django.forms import modelformset_factory
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse
from django.urls import reverse_lazy
from django_pandas.io import read_frame
from pandas.io.json import json_normalize
import datetime
# Local
# import environ
import json
import numpy as np
import pandas as pd
import requests
import urllib
import urllib.request
import time

# Create your views here.

def api_actividades(request):

    atleta = dict(request.GET)['atleta'][0]
    año = dict(request.GET)['año'][0]
    mes = dict(request.GET)['mes'][0]
    dia = dict(request.GET)['dia'][0]
    tipo = dict(request.GET)['tipo'][0]

    query = {}

    if (atleta !=''):
        query['atleta'] = atleta    

    if (año !=''):
        query['año'] = año

    if (mes !=''):
        query['mes'] = mes

    if (dia !=''):
        query['dia'] = dia    

    if (tipo !=''):
        query['tipo'] = tipo

    data_api_actividades = actividades.objects.filter(**query).values('id','fecha','año','mes','dia','tipo','altura','cadencia','distancia','potencia','pulsaciones','tiempo','velocidad','atleta')

    df_data = read_frame(data_api_actividades)

    data = []

    for index, row in df_data.iterrows():
        id = int(row['id'])
        fecha = row['fecha']
        año = row['año']
        mes = row['mes']
        dia = row['dia']
        tipo = row['tipo']
        altura = row['altura']
        cadencia = row['cadencia']
        distancia = row['distancia']
        potencia = row['potencia']
        pulsaciones = row['pulsaciones']
        tiempo = row['tiempo']
        velocidad = row['velocidad']
        atleta = row['atleta']
        data.append({id:(fecha,año,mes,dia,tipo,altura,cadencia,distancia,potencia,pulsaciones,tiempo,velocidad,atleta,)})

    return JsonResponse(data, safe=False)

def api_atletas(request):

    data_api_atletas = atletas.objects.values('id','firstname','lastname','city','state','country','weight','sex')

    df_data = read_frame(data_api_atletas)

    data = []

    for index, row in df_data.iterrows():
        id = int(row['id'])
        nombre = row['firstname']
        apellido = row['lastname']
        ciudad = row['city']
        provincia = row['state']
        pais = row['country']
        peso = row['weight']
        sexo = row['sex']
        data.append({id:(nombre,apellido,ciudad,provincia,pais,peso,sexo,)})

    return JsonResponse(data, safe=False)

def atleta(request):
    atleta = atletas.objects.all().order_by('firstname','lastname','athlete_id')
    context = {'atletas':atleta}
    return render(request, 'atletas.html', context)

def ayuda(request):
    context = {}
    return render(request, 'ayuda.html', context)

def inicio(request):

    url_inicio = request.get_full_path()

    if(url_inicio=="/"):        
            return HttpResponseRedirect('/?atleta=&año=&mes=&dia=&tipo=')

    try:
        atleta = dict(request.GET)['atleta'][0]
    except:
        return HttpResponseRedirect('/?atleta=&año=&mes=&dia=&tipo=')
    año = dict(request.GET)['año'][0]
    mes = dict(request.GET)['mes'][0]
    dia = dict(request.GET)['dia'][0]
    tipo = dict(request.GET)['tipo'][0]

    query = {} 

    if (atleta !=''):
        query['atleta'] = atleta

    if (año !=''):
        query['año'] = año

    if (mes !=''):
        query['mes'] = mes

    if (dia !=''):
        query['dia'] = dia    

    if (tipo !=''):
        query['tipo'] = tipo

    inicio_actividades = actividades.objects.all().order_by("-año","-mes","-dia","atleta","tipo","altura","cadencia")

    inicio_altura = actividades.objects.filter(**query).values('altura')
    df_inicio_altura = read_frame(inicio_altura)
    if inicio_altura.count() != 0:
        altura = float(df_inicio_altura[['altura']].sum())
    else:
        altura = 0
    altura = altura/1000    
    altura = round(float(altura),2)

    inicio_cadencia = actividades.objects.filter(**query).values('cadencia')
    df_inicio_cadencia = read_frame(inicio_cadencia)
    if inicio_cadencia.count() != 0:
        cadencia = float(df_inicio_cadencia[['cadencia']].mean())
    else:
        cadencia = 0
    cadencia = round(float(cadencia),2)

    inicio_dias = actividades.objects.filter(**query).values('fecha').distinct()
    df_inicio_dias = read_frame(inicio_dias)
    if inicio_dias.count() != 0:
        dias = float(df_inicio_dias[['fecha']].count())
    else:
        dias = 0
    dias = int(dias)

    inicio_distancia = actividades.objects.filter(**query).values('distancia')
    df_inicio_distancia = read_frame(inicio_distancia)
    if inicio_distancia.count() != 0:
        distancia = float(df_inicio_distancia[['distancia']].sum())
    else:
        distancia = 0
    distancia = distancia
    distancia = round(float(distancia))

    inicio_pulsaciones = actividades.objects.filter(**query).values('pulsaciones')
    df_inicio_pulsaciones = read_frame(inicio_pulsaciones)
    if inicio_pulsaciones.count() != 0:
        pulsaciones = float(df_inicio_pulsaciones[['pulsaciones']].mean())
    else:
        pulsaciones = 0
    pulsaciones = round(float(pulsaciones),2)

    inicio_potencia = actividades.objects.filter(**query).values('potencia')
    df_inicio_potencia = read_frame(inicio_potencia)
    if inicio_potencia.count() != 0:
        potencia = float(df_inicio_potencia[['potencia']].mean())
    else:
        potencia = 0
    potencia = round(float(potencia),2)

    inicio_tiempo = actividades.objects.filter(**query).values('tiempo')
    df_inicio_tiempo = read_frame(inicio_tiempo)
    if inicio_tiempo.count() != 0:
        tiempo = float(df_inicio_tiempo[['tiempo']].sum())
    else:
        tiempo = 0       
    tiempo = str(int(tiempo/3600)) + ":" + time.strftime('%M:%S', time.gmtime(tiempo))

    inicio_velocidad = actividades.objects.filter(**query).values('velocidad')
    df_inicio_velocidad = read_frame(inicio_velocidad)
    if inicio_velocidad.count() != 0:
        velocidad = float(df_inicio_velocidad[['velocidad']].mean())
    else:
        velocidad = 0
    velocidad = round(float(velocidad),2)

    my_filter = actividades_filter(request.GET, queryset=inicio_actividades)

    inicio_actividades = my_filter.qs
    
    context = {'actividades':inicio_actividades,'altura':altura,'atleta':atleta,'cadencia':cadencia,'dias':dias,'distancia':distancia,'my_filter':my_filter,'pulsaciones':pulsaciones, 'potencia':potencia,'tiempo':tiempo,'url_inicio':url_inicio,'velocidad':velocidad}

    return render(request, 'inicio.html', context)

def data_altura(request):

    atleta = dict(request.GET)['atleta'][0]
    año = dict(request.GET)['año'][0]
    mes = dict(request.GET)['mes'][0]
    dia = dict(request.GET)['dia'][0]
    tipo = dict(request.GET)['tipo'][0]

    query = {}

    if (atleta !=''):
        query['atleta'] = atleta    

    if (año !=''):
        query['año'] = año

    if (mes !=''):
        query['mes'] = mes

    if (dia !=''):
        query['dia'] = dia    

    if (tipo !=''):
        query['tipo'] = tipo

    data_altura = actividades.objects.filter(**query).values('altura','año','mes','tipo')

    df_data_altura = read_frame(data_altura)

    df_data = pd.DataFrame()

    if data_altura.count() != 0:
        for label, _df_data in df_data_altura.groupby(['año','mes']):
            _mes = str(label[1])
            _df_data_ruta = _df_data.loc[_df_data.tipo.isin({'Ruta'})]
            _df_data_virtual = _df_data.loc[_df_data.tipo.isin({'Virtual'})]
            _ruta = float((_df_data_ruta[['altura']].sum())/1000)
            _virtual = float((_df_data_virtual[['altura']].sum())/1000)
            __df_data=pd.DataFrame({"mes":_mes,"ruta":_ruta,"virtual":_virtual}, index=[0])
            df_data=pd.concat([df_data,__df_data], ignore_index=True)

    data = []

    for index, row in df_data.iterrows():
        mes = int(row['mes'])
        ruta = round(float(row['ruta']),2)
        virtual = round(float(row['virtual']),2)
        data.append({mes:(ruta,virtual,)})

    return JsonResponse(data, safe=False)

def data_distancia(request):

    atleta = dict(request.GET)['atleta'][0]
    año = dict(request.GET)['año'][0]
    mes = dict(request.GET)['mes'][0]
    dia = dict(request.GET)['dia'][0]
    tipo = dict(request.GET)['tipo'][0]

    query = {}

    if (atleta !=''):
        query['atleta'] = atleta

    if (año !=''):
        query['año'] = año

    if (mes !=''):
        query['mes'] = mes

    if (dia !=''):
        query['dia'] = dia    

    if (tipo !=''):
        query['tipo'] = tipo

    data_distancia = actividades.objects.filter(**query).values('año','distancia','mes','tipo')

    df_data_distancia = read_frame(data_distancia)

    df_data = pd.DataFrame()

    if data_distancia.count() != 0:
        for label, _df_data in df_data_distancia.groupby(['año','mes']):
            _mes = str(label[1])
            _df_data_ruta = _df_data.loc[_df_data.tipo.isin({'Ruta'})]
            _df_data_virtual = _df_data.loc[_df_data.tipo.isin({'Virtual'})]
            _ruta = float(_df_data_ruta[['distancia']].sum())
            _virtual = float(_df_data_virtual[['distancia']].sum())
            __df_data=pd.DataFrame({"mes":_mes,"ruta":_ruta,"virtual":_virtual}, index=[0])
            df_data=pd.concat([df_data,__df_data], ignore_index=True)

    data = []

    for index, row in df_data.iterrows():
        mes = int(row['mes'])
        ruta = round(float(row['ruta']),2)
        virtual = round(float(row['virtual']),2)
        data.append({mes:(ruta,virtual,)})

    return JsonResponse(data, safe=False)

def data_distancia_total(request):

    año = dict(request.GET)['año'][0]
    mes = dict(request.GET)['mes'][0]
    dia = dict(request.GET)['dia'][0]
    tipo = dict(request.GET)['tipo'][0]

    query = {}

    if (año !=''):
        query['año'] = año

    if (mes !=''):
        query['mes'] = mes

    if (dia !=''):
        query['dia'] = dia    

    if (tipo !=''):
        query['tipo'] = tipo

    data_distancia_total = actividades.objects.filter(**query).values('atleta','distancia')

    df_data_distancia_total = read_frame(data_distancia_total)

    df_data = pd.DataFrame()

    if data_distancia_total.count() != 0:
        for label, _df_data in df_data_distancia_total.groupby(['atleta']):
            _atleta = label
            _distancia = float(_df_data[['distancia']].sum())
            __df_data=pd.DataFrame({"atleta":_atleta,"distancia":_distancia}, index=[0])
            df_data=pd.concat([df_data,__df_data], ignore_index=True)

    df_data = df_data.sort_values(by='distancia', ascending=True)

    if len(df_data.index) > 5:
        df_data = df_data.tail(5)

    data = []

    for index, row in df_data.iterrows():
        atleta = row['atleta']
        distancia = round(float(row['distancia']),2)
        data.append({atleta:(distancia,)})

    return JsonResponse(data, safe=False)

def data_potencia(request):

    atleta = dict(request.GET)['atleta'][0]
    año = dict(request.GET)['año'][0]
    mes = dict(request.GET)['mes'][0]
    dia = dict(request.GET)['dia'][0]
    tipo = dict(request.GET)['tipo'][0]

    query = {}

    if (atleta !=''):
        query['atleta'] = atleta

    if (año !=''):
        query['año'] = año

    if (mes !=''):
        query['mes'] = mes

    if (dia !=''):
        query['dia'] = dia    

    if (tipo !=''):
        query['tipo'] = tipo

    data_potencia = actividades.objects.filter(**query).values('año','mes','potencia','tipo')

    df_data_potencia = read_frame(data_potencia)

    df_data = pd.DataFrame()

    if data_potencia.count() != 0:
        for label, _df_data in df_data_potencia.groupby(['año','mes']):
            _mes = str(label[1])
            _df_data_ruta = _df_data.loc[_df_data.tipo.isin({'Ruta'})]
            _df_data_virtual = _df_data.loc[_df_data.tipo.isin({'Virtual'})]    
            _ruta = float(_df_data_ruta[['potencia']].mean())
            _virtual = float(_df_data_virtual[['potencia']].mean())
            __df_data=pd.DataFrame({"mes":_mes,"ruta":_ruta,"virtual":_virtual}, index=[0])
            __df_data = __df_data.fillna(0)
            df_data=pd.concat([df_data,__df_data], ignore_index=True)

    data = []

    for index, row in df_data.iterrows():
        mes = int(row['mes'])
        ruta = round(float(row['ruta']),2)
        virtual = round(float(row['virtual']),2)
        data.append({mes:(ruta,virtual,)})

    return JsonResponse(data, safe=False)

def data_potencia_total(request):

    año = dict(request.GET)['año'][0]
    mes = dict(request.GET)['mes'][0]
    dia = dict(request.GET)['dia'][0]
    tipo = dict(request.GET)['tipo'][0]

    query = {}

    if (año !=''):
        query['año'] = año

    if (mes !=''):
        query['mes'] = mes

    if (dia !=''):
        query['dia'] = dia    

    if (tipo !=''):
        query['tipo'] = tipo

    data_potencia_total = actividades.objects.filter(**query).values('atleta','potencia')

    df_data_potencia_total = read_frame(data_potencia_total)

    df_data = pd.DataFrame()

    if data_potencia_total.count() != 0:
        for label, _df_data in df_data_potencia_total.groupby(['atleta']):
            _atleta = label
            _potencia = float(_df_data[['potencia']].mean())
            __df_data=pd.DataFrame({"atleta":_atleta,"potencia":_potencia}, index=[0])
            df_data=pd.concat([df_data,__df_data], ignore_index=True)

    df_data = df_data.sort_values(by='potencia', ascending=True)

    if len(df_data.index) > 5:
        df_data = df_data.tail(5)

    data = []

    for index, row in df_data.iterrows():
        atleta = row['atleta']
        potencia = round(float(row['potencia']),2)
        data.append({atleta:(potencia,)})

    return JsonResponse(data, safe=False)

def data_tiempo(request):

    atleta = dict(request.GET)['atleta'][0]
    año = dict(request.GET)['año'][0]
    mes = dict(request.GET)['mes'][0]
    dia = dict(request.GET)['dia'][0]
    tipo = dict(request.GET)['tipo'][0]

    query = {}

    if (atleta !=''):
        query['atleta'] = atleta

    if (año !=''):
        query['año'] = año

    if (mes !=''):
        query['mes'] = mes

    if (dia !=''):
        query['dia'] = dia    

    if (tipo !=''):
        query['tipo'] = tipo

    data_tiempo = actividades.objects.filter(**query).values('año','mes','tiempo','tipo')

    df_data_tiempo = read_frame(data_tiempo)

    df_data = pd.DataFrame()

    if data_tiempo.count() != 0:
        for label, _df_data in df_data_tiempo.groupby(['año','mes']):
            _mes = str(label[1])
            _df_data_ruta = _df_data.loc[_df_data.tipo.isin({'Ruta'})]
            _df_data_virtual = _df_data.loc[_df_data.tipo.isin({'Virtual'})]
            _ruta = float(_df_data_ruta[['tiempo']].sum())
            _virtual = float(_df_data_virtual[['tiempo']].sum())
            __df_data=pd.DataFrame({"mes":_mes,"ruta":_ruta,"virtual":_virtual}, index=[0])
            df_data=pd.concat([df_data,__df_data], ignore_index=True)

    data = []

    for index, row in df_data.iterrows():
        mes = int(row['mes'])
        ruta = round(float((row['ruta'])/3600),2)
        virtual = round(float((row['virtual'])/3600),2)
        data.append({mes:(ruta,virtual,)})

    return JsonResponse(data, safe=False)

def data_tiempo_total(request):

    año = dict(request.GET)['año'][0]
    mes = dict(request.GET)['mes'][0]
    dia = dict(request.GET)['dia'][0]
    tipo = dict(request.GET)['tipo'][0]

    query = {}

    if (año !=''):
        query['año'] = año

    if (mes !=''):
        query['mes'] = mes

    if (dia !=''):
        query['dia'] = dia    

    if (tipo !=''):
        query['tipo'] = tipo

    data_tiempo_total = actividades.objects.filter(**query).values('atleta','tiempo')

    df_data_tiempo_total = read_frame(data_tiempo_total)

    df_data = pd.DataFrame()

    if data_tiempo_total.count() != 0:
        for label, _df_data in df_data_tiempo_total.groupby(['atleta']):
            _atleta = label
            _tiempo = float(_df_data[['tiempo']].sum())
            __df_data=pd.DataFrame({"atleta":_atleta,"tiempo":_tiempo}, index=[0])
            df_data=pd.concat([df_data,__df_data], ignore_index=True)

    df_data = df_data.sort_values(by='tiempo', ascending=True)

    if len(df_data.index) > 5:
        df_data = df_data.tail(5)

    data = []

    for index, row in df_data.iterrows():
        atleta = row['atleta']
        tiempo = round(float((row['tiempo'])/3600),2)
        data.append({atleta:(tiempo,)})

    return JsonResponse(data, safe=False)

def registro(request):

    try:
        code = dict(request.GET)['code'][0]
    except:
        return redirect("/")

    # Heroku
    STRAVA_CLIENT_ID = config('STRAVA_CLIENT_ID')
    STRAVA_CLIENT_SECRET = config('STRAVA_CLIENT_SECRET')

    # Local
    # STRAVA_CLIENT_ID = environ['STRAVA_CLIENT_ID']
    # STRAVA_CLIENT_SECRET = environ['STRAVA_CLIENT_SECRET']
    
    response = requests.post(
                    url = 'https://www.strava.com/oauth/token',
                    data = {
                            'client_id': STRAVA_CLIENT_ID,
                            'client_secret': STRAVA_CLIENT_SECRET,
                            'code': code,
                            'grant_type': 'authorization_code'
                            }
                )
    tokens = response.json()
    df = pd.json_normalize(tokens)
    df = df.fillna(0)
    from .models import atletas
    a = atletas(
        code = code,
        token_type = df['token_type'][0],
        expires_at = df['expires_at'][0],
        expires_in = df['expires_in'][0],
        refresh_token = df['refresh_token'][0],
        access_token = df['access_token'][0],
        athlete_id = df['athlete.id'][0],
        username = df['athlete.username'][0],
        resource_state = df['athlete.resource_state'][0],
        firstname = df['athlete.firstname'][0],
        lastname = df['athlete.lastname'][0],
        bio = df['athlete.bio'][0],
        city = df['athlete.city'][0],
        state = df['athlete.state'][0],
        country = df['athlete.country'][0],
        sex = df['athlete.sex'][0],
        premium = df['athlete.premium'][0],
        summit = df['athlete.summit'][0],
        created_at = df['athlete.created_at'][0],
        updated_at = df['athlete.updated_at'][0],
        badge_type_id = df['athlete.badge_type_id'][0],
        weight = df['athlete.weight'][0],
        profile_medium = df['athlete.profile_medium'][0],
        profile = df['athlete.profile'][0],
        friend = df['athlete.friend'][0],
        follower = df['athlete.follower'][0]            
        )
    try:
        a.save()
        return redirect("/atletas/")
    except:
        return redirect("/atletas/")