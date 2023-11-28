#sendpulse/sms_sender.py
import requests
from config import CLIENT_ID, CLIENT_SECRET
from database.database import add_phone_number, get_all_phone_numbers
from sendpulse.sms_auth import get_access_token

def send_sms(access_token, sender, phones, message):
    url = 'https://api.sendpulse.com/sms/send'
    headers = {'Authorization': f'Bearer {access_token}'}
    payload = {
        'sender': sender,
        'phones': phones,
        'body': message
    }
    response = requests.post(url, headers=headers, json=payload)
    return response.json()

# Пример использования
access_token = get_access_token(CLIENT_ID, CLIENT_SECRET)
response = send_sms(access_token, "SenderName", ["+1234567890"], "Test message")
print(response)
