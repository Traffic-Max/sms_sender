#parser/phone_collector.py
import re
import json
import time
import requests
import dateparser
from dateparser import parse
from bs4 import BeautifulSoup
from requests_html import HTMLSession
from datetime import datetime, timedelta
from database.database import add_car_ad, init_db, CarAd, Session
from .parse_config import WEEKDAYS, MONTHS_UK_TO_EN, FILTER_URL, COMPARE_URL, HEADERS, KNOWN_BRANDS


from requests.adapters import HTTPAdapter
from urllib3.util import Retry


def requests_retry_session(retries=3, backoff_factor=0.3, status_forcelist=(500, 502, 504)):
    session = requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session


def translate_date_uk_to_en(date_str):
    for uk, en in MONTHS_UK_TO_EN.items():
        date_str = date_str.replace(uk, en)
    return date_str


def convert_relative_date_ukrainian(date_str):
    # Сначала попробуем распознать дату с помощью dateparser
    parsed_date = dateparser.parse(date_str, languages=['uk'], settings={'DATE_ORDER': 'DMY'})
    
    # Если dateparser успешно распознал дату
    if parsed_date:
        return parsed_date.date()  # Возвращаем только дату, без времени

    # Если dateparser не смог распознать, пробуем альтернативные методы
    current_time = datetime.now()

    if date_str.startswith("вчора о"):
        return (current_time - timedelta(days=1)).date()
    
    elif date_str.startswith("сьогодні о"):
        return current_time.date()

    # Обработка случая "години тому"
    elif "години тому" in date_str:
        hours_ago = int(re.search(r'(\d+) години тому', date_str).group(1))
        return current_time - timedelta(hours=hours_ago)

    # Обработка случая "минулої ..."
    elif "минулої" in date_str:
        match = re.search(r'минулої (\w+’?\w+)', date_str)
        if match:
            weekday_str = match.group(1)
            target_weekday = list(WEEKDAYS.keys()).index(weekday_str)
            current_weekday = current_time.weekday()
            days_ago = (7 + current_weekday - target_weekday) % 7
            target_date = current_time - timedelta(days=days_ago)
            return target_date.date()  # Возвращаем только дату

    else:
        date_str = translate_date_uk_to_en(date_str)
        parsed_date = parse(date_str, languages=['uk'])
        if parsed_date:
            return parsed_date.date()

    return None


def get_number(num_url, params, headers):
    session_with_retry = requests_retry_session()
    response = session_with_retry.get(url=num_url, params=params, headers=headers)
    phone_data = json.loads(response.text)['phones']
    clean_number = clean_phone_numbers(phone_data)
    return clean_number


def clean_phone_numbers(phone_data):
    cleaned_numbers = []

    for phone_entry in phone_data:
        phone_number = phone_entry['phoneFormatted']
        # Удаляем все кроме цифр
        phone_number = re.sub("[^\d]", "", phone_number)

        # Добавляем префикс '380', если номер слишком короткий
        if len(phone_number) == 10:
            phone_number = '38' + phone_number
        
        cleaned_numbers.append(phone_number)
    
    return cleaned_numbers


def get_hash_data(link, HEADERS):
    session_with_retry = requests_retry_session()
    response = session_with_retry.get(url=link, headers=HEADERS)
    soup = BeautifulSoup(response.text, "html.parser")
    script = soup.find("script", attrs={'src': True, 'data-user-secure-hash': True})
    return {
        'hash': script.get('data-user-secure-hash', None),
        'expires': script.get('data-user-secure-expires', None),
        'ad_id': script.get('data-advertisement-id', None)
    }


def get_links(filter_url, compare_url, page):
    session = HTMLSession()

    # Нахождение и замена параметра 'page'
    page_param = "page=" + str(page)
    if "page=0" in filter_url:
        updated_url = filter_url.replace("page=0", page_param)
    else:
        updated_url = filter_url + "&" + page_param

    response = session.get(updated_url)
    return [link for link in response.html.absolute_links if compare_url in link]


def extract_brand_model_year(full_string):
    parts = full_string.split()
    year = parts[-1]  # Год - последнее слово

    # Проверка, является ли год числом
    if not year.isdigit():
        year = None  # Или другая логика обработки

    brand_model = ' '.join(parts[:-1])  # Остальная часть - марка и модель
    
    # Поиск марки в строке
    for brand in KNOWN_BRANDS:
        if brand in brand_model:
            start = brand_model.find(brand)
            end = start + len(brand)
            model = brand_model[end:].strip()  # Модель - это остальная часть строки после марки
            return brand, model, year

    return None, None, year  # Если марка не найдена


def get_body_attributes(link, session):
    """Извлечение атрибутов автомобиля из страницы."""
    r = session.get(link)
    soup = BeautifulSoup(r.text, "html.parser")

    # Проверка, является ли продавец компанией
    seller_info_area = soup.find("div", class_="seller_info_area")
    if seller_info_area:
        seller_type = seller_info_area.find("div", class_="seller_info_title grey")
        if seller_type and seller_type.get_text(strip=True) == "Компанія":
            return None  # Пропускаем объявление от компании

    body_data = r.html.find('div.auto-wrap', first=True).text.split('\n')
    attributes = {}
    description_flag = False
    description = []

    # Извлечение марки, модели и года
    car_info = r.html.find('span.argument.d-link__name', first=True)
    if car_info:
        brand, model, year = extract_brand_model_year(car_info.text)
        attributes['brand'] = brand
        attributes['model'] = model
        attributes['year'] = year

    for block in body_data:
        block = block.strip()
        if block.startswith("Ціна:"):
            price = block.split("•")[0].replace("Ціна:", "").strip()
            attributes['price'] = price
        elif block.startswith("Пробіг"):
            mileage = block.split("•")[0].replace("Пробіг", "").strip()
            attributes['mileage'] = mileage
        elif block.startswith("Двигун"):
            engine = block.replace("Двигун", "").strip()
            attributes['engine'] = engine
        elif block.startswith("Коробка передач"):
            transmission = block.replace("Коробка передач", "").strip()
            attributes['transmission'] = transmission
        elif block.startswith("Привід"):
            drive = block.replace("Привід", "").strip()
            attributes['drive'] = drive
        elif "Кузов" in block:
            body = block.split("•")[0].replace("Кузов", "").strip()
            attributes['body'] = body

        if description_flag:
            if block:
                description.append(block)
            else:
                description_flag = False
                attributes['description'] = ' '.join(description)

        if block.startswith("Опис"):
            description_flag = True
            
        if "Продавець:" in block or "Ім'я:" in block:
            seller_name = block.split(':')[1].strip()
            attributes['seller_name'] = seller_name

    return attributes


def extract_ad_date(link, session):
    """Извлечение даты создания объявления."""
    r = session.get(link)
    r.html.render(timeout=30)  # Для динамически загружаемого контента
    ad_date_info = r.html.find("#addDate", first=True)
    ad_date = ad_date_info.find("span", first=True).text if ad_date_info else "Не указано"
    ad_date_converted = convert_relative_date_ukrainian(ad_date)
    return ad_date_converted


def extract_seller_name(url, session):
    """Извлечение имени продавца."""
    r = session.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    seller_info = soup.find("div", class_="seller_info_name")
    seller_name = seller_info.get_text(strip=True) if seller_info else "Не указано"
    return seller_name


def main():
    """Основная функция скрипта."""
    init_db()  # Инициализация базы данных

    start_time = time.time()
    # links = get_links(FILTER_URL, COMPARE_URL)
    session = HTMLSession()
    # Создание сессии для работы с базой данных
    db_session = Session()

    page = 0
    while True:
        links = get_links(FILTER_URL, COMPARE_URL, page)
        if not links:
            break  # Если нет ссылок, значит достигли последней страницы
    
        for link in links:
            hash_data = get_hash_data(link, HEADERS)
            ad_id = hash_data['ad_id']
            if ad_id and hash_data['hash']:
                num_url = f'https://auto.ria.com/users/phones/{ad_id}/'
                attributes = get_body_attributes(link, session)
                if attributes is None:
                    continue  # Пропускаем объявление от компании

                seller_name = extract_seller_name(link, session)
                ad_date = extract_ad_date(link, session)
                phone_data = get_number(num_url, hash_data, HEADERS)

                # Проверка на существующие объявления в базе данных
                existing_ad = db_session.query(CarAd).filter_by(seller_name=seller_name, ad_date=ad_date).first()
                if not existing_ad:
                    add_car_ad(
                        brand=attributes.get('brand'),
                        model=attributes.get('model'),
                        year=attributes.get('year'),
                        mileage=attributes.get('mileage'),
                        engine=attributes.get('engine'),
                        ad_date=ad_date,
                        seller_name=seller_name,
                        phone_numbers=phone_data,
                        price = attributes.get('price'),
                        is_new=True,  # или другое подходящее значение
                        category=attributes.get('category')  # или другое подходящее значение
                    )

                # Форматированный вывод информации
                print(f"Автомобиль: {link}")
                print(f"Продавец: {seller_name}")
                print(f"Дата создания объявления: {ad_date}")
                for attr, value in attributes.items():
                    print(f"{attr.capitalize()}: {value}")
                print(f"Телефон: {', '.join(phone_data)}")
                print("-" * 50)  # Разделитель между объявлениями
        page += 1  # Переход к следующей странице

    db_session.close()
    print(f"Elapsed general time: {time.time() - start_time}")

if __name__ == '__main__':
    main()
