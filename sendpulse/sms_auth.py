#sendpulse/sms_auth.py
import requests

def get_access_token(client_id, client_secret):
    url = 'https://api.sendpulse.com/oauth/access_token'
    payload = {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret
    }
    response = requests.post(url, json=payload)
    return response.json().get('access_token')
