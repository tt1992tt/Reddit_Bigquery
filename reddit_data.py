import time
import random
import requests
import pandas as pd
from datetime import datetime, timedelta
from google.cloud import storage
from dependencies.reddit_config import USRNAM, PSSWRD, SCRIPT, SECRET

def upload_to_bucket():
    # armo un request para un token basico OAuth
    auth = requests.auth.HTTPBasicAuth(SCRIPT, SECRET)

    # el metodo de login a utilizar, grant type password porque asi lo indica para scripts
    data = {'grant_type': 'password',
            'username': USRNAM,
            'password': PSSWRD}

    headers = {'User-Agent': 'testing_tt/0.0.1'}

    # le paso la request de OAuth
    req = requests.post('https://www.reddit.com/api/v1/access_token', auth=auth, data=data, headers=headers)

    # si fue exitoso, agarro "access_token"
    TOKEN = req.json()['access_token']

    # apendeo a mi dict header el access token
    #headers = {**headers, **{'Authorization': f'bearer {TOKEN}'}}
    headers["Authorization"] = f'bearer {TOKEN}'

    # ahora cada request que hago va a ser con el header hacia https://oauth.reddit.com
    response = requests.get('https://oauth.reddit.com', headers=headers)

    # si expira el token (cada 1 hora) puedo usar el refresh token en vez del access token
    if not response.ok:
        TOKEN = req.json()['refresh_token']
        headers["TOKEN"] = f'bearer {TOKEN}'

    response = requests.get('https://oauth.reddit.com/r/Argentina/hot', headers=headers, params={'limit' : '100'})

    json_data = response.json()['data']['children']

    results_dict = {"Title" : [],
                    "Date" : [],
                    "Link" : [],
                    "Num_Comments" : [],
                    "Num_Reports" : [],
                    "Score" : []}


    for t in json_data:
        results_dict["Title"].append(t['data']['title'])
        results_dict["Date"].append(datetime.today().date())
        results_dict["Link"].append(t['data']['url'])
        results_dict["Num_Comments"].append(t['data']['num_comments'])
        results_dict["Num_Reports"].append(t['data']['num_reports'])
        results_dict["Score"].append(t['data']['score'])

        df_reddit = pd.DataFrame(results_dict)
        df_reddit.sort_values(by="Score", axis=0, inplace=True, ignore_index=True, ascending=False)
        
    bucket = storage.Client().bucket('bucket_tt')
    bucket.blob('upload_test/test.csv').upload_from_string(df_reddit.to_csv(index=False), 'text/csv')


