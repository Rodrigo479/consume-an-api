import requests
import json
import requests_cache

requests_cache.install_cache()
API_KEY = '49d043f6c0b404e0a8cef1011cd099fa'
USER_AGENT = 'Keytarist'

def lastfm_get(payload):
    # define headers and URL
    headers = {'user-agent': USER_AGENT}
    url = 'https://ws.audioscrobbler.com/2.0/'

    # Add API key and format to the payload
    payload['api_key'] = API_KEY
    payload['format'] = 'json'

    response = requests.get(url, headers=headers, params=payload)
    return response

def jprint(obj):
    # create a formatted string of the Python JSON object
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)

payload = {
    'method': 'chart.gettopartists'
}

r = lastfm_get(payload)
jprint(r.json())