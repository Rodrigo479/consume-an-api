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

def get_top_artists():    
    responses = []
    page = 1
    while page <= total_pages:
        payload = {
            'method': 'chart.gettopartists',
            'limit': 5,
            'page': page
        }

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
        
        array = response.json()
        for index, artist in enumerate(array['artists']['artist']):
            array['artists']['artist'][index]['tags'] = get_top_tags(artist['name'])
        json_response = json.dumps(array)
        # append response
        responses.append(json_response)

        # if it's not a cached result, sleep
        if not getattr(response, 'from_cache', False):
            time.sleep(0.25)

        # increment the page number
        page += 1
    return responses

def get_top_tags(artist):
    payload = {
            'method': 'artist.getTopTags',
            'artist': artist
        }
    response = lastfm_get(payload)
    tags = [t['name'] for t in response.json()['toptags']['tag'][:3]]
    tags_str = ', '.join(tags)
    return tags_str

response = get_top_artists()
frames = [pd.DataFrame(json.loads(r)['artists']['artist']) for r in response]
artists = pd.concat(frames)
artists = artists.drop('image', axis=1)
artists = artists.drop_duplicates().reset_index(drop=True)
artists[["playcount", "listeners"]] = artists[["playcount", "listeners"]].astype(int)
artists = artists.sort_values("listeners", ascending=False)
artists.head()
artists.to_csv('artists.csv', index=False)
print(artists.to_string())