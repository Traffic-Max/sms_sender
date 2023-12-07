import requests
import pprint

headers = {
    'authority': 'www.olx.ua',
    'accept': '*/*',
    'accept-language': 'uk',
    'authorization': 'Bearer ded8830ac46eb8a437db7c95963690207c02e82b',
    'origin': 'https://platinum-auto.olx.ua',
    'referer': 'https://platinum-auto.olx.ua/',
    'sec-ch-ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    'x-client': 'DESKTOP',
    'x-device-id': '21b53d4e-ed0f-40ef-b75f-7fbff4e31dc5',
    'x-fingerprint': 'fbdc4f53959cdb4a0ca0f7f0d089ca8a00ab77cc9433c497f1625c5c241a92a96255da10575393646255da105753936456b16d11aecc818682e4cda99633e224801d6b5073f992cf00ab77cc9433c49756b16d11aecc818629b755643a58ca1b4618cb94a4cccf89e631c3c89377a0bb2601616aab71baecc9ca8e1b7394feb1f1625c5c241a92a9ef069f2845625c946255da1057539364838493b575e238f7941884f54688d0eb4c900da77a01aaf0061ced26da634318745ddd797fe8df60a8e06d4216f6691883bb1eb95319dd525a1778be62509b003fef60c9cf99daee308e012c59cf7bddb497a357830277b84b9d07ac14aa528742dbc50f4bc9cf48be25d661fcb5c283bea1a54213c0c5effba3f93a541321b34b27b167ffd437e7f2a904bd6181b2297aeefdcd3fa45b868405a46c218194e73fe2f7b0b294ce7c973d3b56ded5b600973d3b56ded5b600973d3b56ded5b600973d3b56ded5b600973d3b56ded5b600973d3b56ded5b600973d3b56ded5b600973d3b56ded5b600973d3b56ded5b600674588ce8ed5ec6f',
    'x-platform-type': 'mobile-html5',
}

params = {
    'offset': '30',
    'limit': '30',
    'category_id': '0',
    'sort_by': 'created_at:desc',
    'query': '',
    'user_id': '1124424367',
    'owner_type': 'business',
    'facets': '[{"field":"category","limit":150}]',
    'last_seen_id': '',
}

response = requests.get('https://www.olx.ua/api/v1/offers/', params=params, headers=headers)

# Проверка на успешный ответ
if response.status_code == 200:
    # Сохранение содержимого ответа в файл
    with open("source.html", "w", encoding="utf-8") as file:
        file.write(response.text)
else:
    print("Ошибка запроса, статус код:", response.status_code)
    