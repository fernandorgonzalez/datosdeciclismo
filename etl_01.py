from datetime import datetime, timedelta
import pandas as pd
import psycopg2
import requests
import urllib3
import settings
from os import environ

DB_HOST = environ["DB_HOST"]
DB_NAME = environ["DB_NAME"]
DB_USER = environ["DB_USER"]
DB_PASSWORD = environ["DB_PASSWORD"]

WDIR = environ["WDIR"]

STRAVA_CLIENT_ID = environ["STRAVA_CLIENT_ID"]
STRAVA_CLIENT_SECRET = environ["STRAVA_CLIENT_SECRET"]

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

auth_url = "https://www.strava.com/oauth/token"
activites_url = "https://www.strava.com/api/v3/athlete/activities"

output_file_name = WDIR + "strava.csv"

after = int((datetime.today() - timedelta(days=365)).timestamp())

df = pd.DataFrame()

conexion = psycopg2.connect(host=DB_HOST,dbname=DB_NAME,user=DB_USER,  password=DB_PASSWORD)

cursor = conexion.cursor()

query = ''' SELECT id,firstname,lastname,refresh_token FROM APP_ATLETAS order by firstname, lastname '''

cursor.execute(query)

for atleta in cursor:
    
    id=atleta[0]
    firstname=atleta[1]
    lastname=atleta[2]
    refresh_token=atleta[3]

    id_atleta = id
    atleta = firstname + " " + lastname

    print("\n" + atleta + "\n")

    payload = {
        'client_id': STRAVA_CLIENT_ID,
        'client_secret': STRAVA_CLIENT_SECRET,
        'refresh_token': refresh_token,
        'grant_type': "refresh_token",
        'f': 'json'
    }

    res = requests.post(auth_url, data=payload, verify=False)
    access_token = res.json()['access_token']

    header = {'Authorization': 'Bearer ' + access_token}

    page = 1

    while True:
        my_dataset = requests.get(activites_url, headers=header, params={'per_page': 200, 'page': page, 'after': after}).json()
        _df = pd.json_normalize(my_dataset)
        if (_df.shape[0] == 0):
            break
        print("Page " + str(page))
        _df['atleta_id'] = id_atleta
        df=pd.concat([df,_df], ignore_index=True)
        page = page +1

cursor.close()
conexion.close()

print("\n")

df.to_csv(output_file_name,index=False,sep=';')
