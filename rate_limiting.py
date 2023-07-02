import requests
import time
import os
import json
import pandas as pd
import requests_cache

requests_cache.install_cache()

API_KEY = '49d043f6c0b404e0a8cef1011cd099fa'
USER_AGENT = 'Keytarist'
total_pages = 3 # this is just a dummy number so the loop starts

def lastfm_get(payload):
    # define headers and URL
    headers = {'user-agent': USER_AGENT}
    url = 'https://ws.audioscrobbler.com/2.0/'

    # Add API key and format to the payload
    payload['api_key'] = API_KEY
    payload['format'] = 'json'

    response = requests.get(url, headers=headers, params=payload)
    return response

def jprint(array):
    for obj in array:
        # create a formatted string of the Python JSON object
        text = json.dumps(obj.json(), sort_keys=True, indent=4)
        print(text)

def run_request(method, artist = ""):    
    responses = []
    page = 1
    while page <= total_pages:
        payload = {
            'method': method,
            'limit': 5,
            'page': page
        }

        if method == 'artist.getTopTags':
            payload['artist'] = artist

        # print some output so we can see the status
        print("Requesting page {}/{}".format(page, total_pages))
        # clear the output to make things neater
        # os.system('cls')

        # make the API call
        response = lastfm_get(payload)

        # if we get an error, print the response and halt the loop
        if response.status_code != 200:
            print(response.text)
            break

        # extract pagination info
        # page = int(response.json()['artists']['@attr']['page'])
        # total_pages = int(response.json()['artists']['@attr']['totalPages'])

        # append response
        responses.append(response)

        # if it's not a cached result, sleep
        if not getattr(response, 'from_cache', False):
            time.sleep(0.25)

        # increment the page number
        page += 1
        
    if method == 'chart.gettopartists':
        frames = [pd.DataFrame(r.json()['artists']['artist']) for r in responses]
        artists = pd.concat(frames)
        artists = artists.drop('image', axis=1)
    elif method == 'artist.getTopTags':
        frames = [pd.DataFrame(r.json()['toptags']['tag']) for r in responses]
        artists = pd.concat(frames)
    artists = artists.drop_duplicates().reset_index(drop=True)
    artists.head()
    print(artists.to_string())
    
    # jprint(responses) # desborda el terminal y no aparecen todos los resultados

run_request('chart.gettopartists')
run_request('artist.getTopTags', 'Lana Del Rey')