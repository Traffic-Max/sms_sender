import time
import aiohttp
import asyncio
import logging
from bs4 import BeautifulSoup
import json
import re
from datetime import datetime, timedelta
from dateparser import parse
from database.database import add_car_ad, init_db, CarAd, Session

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Конфигурация логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AsyncCarAdParser:
    FILTER_URL = "https://auto.ria.com/uk/search/?indexName=auto&categories.main.id=1&country.import.usa.not=-1&region.id[0]=12&city.id[0]=12&price.currency=1&abroad.not=0&custom.not=1&page=0&size=100"
    COMPARE_URL = "https://auto.ria.com/uk/auto_"

    KNOWN_BRANDS = [
        'Volkswagen', 'Mercedes-Benz', 'BMW', 'Renault', 'Audi', 'Ford', 'Skoda', 'Opel', 'Nissan', 
        'Toyota', 'Hyundai', 'Mazda', 'Honda', 'Chevrolet', 'Peugeot', 'Kia', 'Daewoo', 'Mitsubishi', 
        'ЗАЗ', 'Citroen', 'Volvo', 'Lexus', 'Fiat', 'Jeep', 'Land Rover', 'Chery', 'Dacia', 'Dodge', 
        'Geely', 'Porsche', 'Infiniti', 'SEAT', 'Ford', 'Chevrolet', 'Tesla', 'Jeep', 'Dodge', 'Chrysler', 
        'Lincoln', 'Cadillac', 'Buick', 'GMC', 'Hummer', 'Pontiac', 'Land Rover', 'Jaguar', 'MINI', 
        'Rover', 'Bentley', 'MG', 'Rolls-Royce', 'Fiat', 'Alfa Romeo', 'Maserati', 'Lancia', 'Iveco', 
        'Lamborghini', 'Chery', 'Geely', 'BYD', 'Great Wall', 'JAC', 'Lifan', 'Dadi', 'Dongfeng', 'FAW', 
        'Hyundai', 'Kia', 'Daewoo', 'SsangYong', 'Volkswagen', 'BMW', 'Audi', 'Mercedes-Benz', 'Opel', 
        'Porsche', 'Smart', 'ВАЗ / Lada', 'ГАЗ', 'УАЗ', 'ЗАЗ', 'Богдан', 'Renault', 'Peugeot', 'Citroen', 
        'Nissan', 'Toyota', 'Mazda', 'Mitsubishi', 'Honda', 'Lexus', 'Subaru', 'Infiniti', 'Suzuki', 
        'Acura', 'Daihatsu', 'Isuzu'
        ]
    
    WEEKDAYS = {
        "понеділок": "Monday",
        "понеділка": "Monday",
        "вівторок": "Tuesday",
        "вівторка": "Tuesday",
        "середа": "Wednesday",
        "середи": "Wednesday",
        "четвер": "Thursday",
        "четверга": "Thursday",
        "п’ятниця": "Friday",
        "п’ятниці": "Friday",
        "субота": "Saturday",
        "суботи": "Saturday",
        "неділя": "Sunday",
        "неділі": "Sunday"
    }

    MONTHS_UK_TO_EN = {
        "січня": "January",
        "лютого": "February",
        "березня": "March",
        "квітня": "April",
        "травня": "May",
        "червня": "June",
        "липня": "July",
        "серпня": "August",
        "вересня": "September",
        "жовтня": "October",
        "листопада": "November",
        "грудня": "December"
    }

    HEADERS = {
        'Cookie': '_gcl_au=1.1.707876906.1693575975; __utmc=79960839; ui=ab59f9bd0d5f66d0; _fbp=fb.1.1693575975051.673396265; _cc_id=80cf1657627e5f524f4bc5b091409709; gdpr=[2,3]; test_fast_search=3; _ga_KGL740D7XD=GS1.1.1694436370.27.1.1694437661.60.0.0; _ga_KGL740D7XD=deleted; _ga_1XC358ET5K=GS1.2.1695195758.37.1.1695195856.27.0.0; cto_bundle=UcX_xl9yTmRlMFNpaGZKaTl5cUhycE5WZmNBV0JPTDFHdEZCUUkyTFIzajklMkJLM0VvSDBzcFNlbjElMkY4Y05ncTlnRVdXOXNVJTJGYUx6TllTRFdWJTJGMUNsVFI3JTJGeUNBN2wyTGF5dmt5S2gzZGpUbnoxTEM5OVFMOUZhdUJ0OHBKZVJVU3V2Y3klMkYlMkZOMGVtTnV3ajFkSmZteXFXbWclMkZDV1pXQlJDZzI1a21iREJiWlRNYSUyQkppdlNGT0gzUHFwUWpBNlZZZ0M0TnBPTlRUYjdzOVgyWE9zVGFwenYxU1B3JTNEJTNE; AMP-CONSENT=amp-VNphoop22CqKNhDbv20eCg; slonik_utm_medium=share_final_page; slonik_utm_source=ios; extendedSearch=1; showNewFinalPage=1; g_state={"i_p":1701084796415,"i_l":4}; showNewFeatures=7; showNewNextAdvertisement=10; test_new_features=726; advanced_search_test=42; _ga_E241E4XQ26=GS1.1.1700134373.1.1.1700134379.54.0.0; descriptionHidden=1; ipp=20; ab-link-video-stories=2; ab_redesign=0; _ga=GA1.3.190258360.1693575975; _clck=1pzp3cz%7C2%7Cfgx%7C0%7C1421; _ga_QE9NBY8W7X=GS1.1.1700640245.1.1.1700640282.23.0.0; slonik_utm_campaign=ads_bu; promolink2=4; _504c2=http://10.42.12.237:3000; AMP_TOKEN=%24NOT_FOUND; _gid=GA1.2.1556869753.1700897404; PHPSESSID=XFt1i0XiYlHnqDM0O72vH2GKQNJxRxJg; ria_sid=50115496820727; __utma=79960839.190258360.1693575975.1700897402.1700900083.128; __utmz=79960839.1700900083.128.28.utmcsr=ios|utmccn=ads_bu|utmcmd=share_final_page; __utmt=1; __utmt_b=1; PHPSESSID=eyJ3ZWJTZXNzaW9uQXZhaWxhYmxlIjp0cnVlLCJ3ZWJQZXJzb25JZCI6MCwid2ViQ2xpZW50SWQiOjI4NzQ4MDA1NzMsIndlYkNsaWVudENvZGUiOjIyNDM1NjA0OCwid2ViQ2xpZW50Q29va2llIjoiYWI1OWY5YmQwZDVmNjZkMCIsIl9leHBpcmUiOjE3MDA5ODY0ODc0ODIsIl9tYXhBZ2UiOjg2NDAwMDAwfQ==; __gads=ID=6e723e6239d1e3e8-22d8a07262de000d:T=1693575976:RT=1700900087:S=ALNI_MYievLIwYiynpUCT5OzzLqcLIcngw; __gpi=UID=00000c6d635f4afd:T=1693575976:RT=1700900087:S=ALNI_MbJbZ5_NOYUEvQEcmtDWxoHcXU0KQ; _ga_KGL740D7XD=GS1.1.1700900082.153.1.1700900160.59.0.0; _ga=GA1.1.190258360.1693575975; __utmb=79960839.4.10.1700900083',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Host': 'auto.ria.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        'Accept-Language': 'en-GB,en;q=0.9',
        'Connection': 'keep-alive',
    }


    async def init_session(self):
        self.session = aiohttp.ClientSession()


    async def close_session(self):
        if self.session:
            await self.session.close()
            self.session = None


    async def fetch_links(self):
        logger.info("Fetching links...")
        async with self.session.get(self.FILTER_URL) as response:
            html = await response.text()
            soup = BeautifulSoup(html, "html.parser")
            return [a['href'] for a in soup.find_all('a', href=True) if self.COMPARE_URL in a['href']]


    async def get(self, url):
        try:
            async with self.session.get(url) as response:
                return await response.text()
        except Exception as e:
            logger.error(f"Error fetching URL {url}: {e}")
            return None


    async def fetch_ad_details(self, url):
        try:
            logger.info(f"Fetching ad details from {url}")
            async with self.session.get(url, headers=self.HEADERS) as response:
                html = await response.text()
                if html:
                    soup = BeautifulSoup(html, "html.parser")
                    # Извлечение всех данных, включая дату, с помощью BeautifulSoup
                    attributes = self.extract_all_data(soup)
                    if not attributes['ad_date']:
                        # Если дата не найдена, используйте Selenium
                        ad_date = await self.fetch_ad_date_with_selenium(url)
                        attributes['ad_date'] = ad_date
                    logger.info("Ad details extracted successfully")
                    return attributes
                else:
                    logger.error(f"No HTML content retrieved for URL: {url}")
                    return None
        except Exception as e:
            logger.error(f"Error fetching ad details from {url}: {e}")
            return None
        

    async def fetch_ad_date_with_selenium(self, url):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

        try:
            driver.get(url)
            await asyncio.sleep(3)  # Дайте странице время для загрузки

            soup = BeautifulSoup(driver.page_source, "html.parser")
            ad_date_info = soup.find("li", {"id": "addDate"})
            if ad_date_info and ad_date_info.find("span"):
                ad_date = ad_date_info.find("span").text.strip()
                return ad_date
            else:
                logger.error(f"Ad date info not found in URL: {url}")
                ad_date = "Не указано"
                return None

        except Exception as e:
            logger.error(f"Error fetching ad date from {url} using Selenium: {e}")
            return None
        finally:
            driver.quit()


    def extract_all_data(self, soup):
        data = {}

        # Марка, модель, и год автомобиля
        car_info = soup.find('span', {'class': 'argument d-link__name'})
        if car_info and car_info.text:
            brand, model, year = self.extract_brand_model_year(car_info.text)
            data['brand'] = brand
            data['model'] = model
            data['year'] = year

        try:
            auto_wrap = soup.find('div', {'class': 'auto-wrap'})
            if auto_wrap:
                text_blocks = auto_wrap.text.split('\n')
                for block in text_blocks:
                    block = block.strip()
                    if block.startswith("Ціна:"):
                        data['price'] = block.split("•")[0].replace("Ціна:", "").strip()
                    elif block.startswith("Пробіг"):
                        data['mileage'] = block.split("•")[0].replace("Пробіг", "").strip()
                    elif block.startswith("Двигун"):
                        data['engine'] = block.replace("Двигун", "").strip()
        except Exception as e:
            logger.error(f"Error processing auto_wrap for, error: {e}")


        # Информация о продавце и дате объявления
        seller_info = soup.find("div", class_="seller_info_name")
        data['seller_name'] = seller_info.text.strip() if seller_info else "Не указано"

        ad_date_info = soup.find("li", {"id": "addDate"})
        ad_date = ad_date_info.find("span").text.strip() if ad_date_info and ad_date_info.find("span") else "Не указано"
        data['ad_date'] = self.convert_relative_date_ukrainian(ad_date)

        return data
    

    def extract_brand_model_year(self, full_string):
        # Логика извлечения марки, модели и года
        parts = full_string.split()
        if parts:
            year = parts[-1] if parts[-1].isdigit() else None
            brand_model = ' '.join(parts[:-1]) if year else full_string
            for brand in self.KNOWN_BRANDS:
                if brand in brand_model:
                    start = brand_model.find(brand)
                    end = start + len(brand)
                    model = brand_model[end:].strip()
                    return brand, model, year
            return None, None, year
        else:
            return None, None, None
 

    # async def extract_seller_info(self, url, soup):
    #     seller_info = soup.find("div", class_="seller_info_name")
    #     seller_name = seller_info.text.strip() if seller_info else "Не указано"

    #     ad_date_info = soup.find("li", {"id": "addDate"})
    #     if ad_date_info:
    #         ad_date = ad_date_info.find("span").text.strip() if ad_date_info.find("span") else "Не указано"
    #         logger.info(f"Raw ad date extracted: {ad_date}")  # Добавлено логирование сырой даты
    #     else:
    #         logger.warning(f"Ad date element not found in URL: {url}")
    #         ad_date = "Не указано"

    #     ad_date_converted = self.convert_relative_date_ukrainian(ad_date)

    #     return seller_name, ad_date_converted


    async def fetch_phone_numbers(self, ad_id, hash_data):
        """Асинхронное получение номеров телефонов."""
        num_url = f'https://auto.ria.com/users/phones/{ad_id}/'
        logger.info(f"Fetching phone numbers with ad_id: {ad_id}, hash_data: {hash_data}")
        async with self.session.get(num_url, params=hash_data) as response:
            data = await response.json()
            phone_data = data['phones']
            clean_numbers = await self.clean_phone_numbers(phone_data)
            return clean_numbers


    async def clean_phone_numbers(self, phone_data):
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
    
    def translate_date_uk_to_en(self, date_str):
        for uk, en in self.MONTHS_UK_TO_EN.items():
            date_str = date_str.replace(uk, en)
        return date_str
    
    def convert_relative_date_ukrainian(self, date_str):
        # Сначала попробуем распознать дату с помощью dateparser
        parsed_date = parse(date_str, languages=['uk'], settings={'DATE_ORDER': 'DMY'})
        
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
                target_weekday = list(self.WEEKDAYS.keys()).index(weekday_str)
                current_weekday = current_time.weekday()
                days_ago = (7 + current_weekday - target_weekday) % 7
                target_date = current_time - timedelta(days=days_ago)
                return target_date.date()  # Возвращаем только дату

        else:
            date_str = self.translate_date_uk_to_en(date_str)
            parsed_date = parse(date_str, languages=['uk'])
            if parsed_date:
                return parsed_date.date()

        return None


    async def save_to_database(self, ad_details):
        logger.info(f"Saving ad to database: {ad_details}")
        try:
            add_car_ad(
                brand=ad_details.get('brand', ''),
                model=ad_details.get('model', ''),
                year=ad_details.get('year'),
                mileage=ad_details.get('mileage', ''),
                engine=ad_details.get('engine', ''),
                ad_date=ad_details.get('ad_date'),
                seller_name=ad_details.get('seller_name', ''),
                phone_numbers=ad_details.get('phone_numbers', []),
                is_new=True,  # или другой логический флаг, если нужен
                category=None  # или другое значение, если нужно
            )
            logger.info("Ad saved successfully")
        except Exception as e:
            logger.error(f"Error saving ad to database: {e}")


    async def main(self):
        start_time = time.time()
        try:
            logger.info("Starting parser...")
            await self.init_session()
            links = await self.fetch_links()
            unique_links = set(links)  # Удаление дубликатов

            # Ограничение количества одновременно выполняемых задач
            sem = asyncio.Semaphore(10)  # Пример: 10 задач одновременно

            async def parse_link(link):
                async with sem:
                    try:
                        logger.debug(f"Processing link: {link}")
                        data = await self.extract_all_data(link)
                        logger.debug(f"Data extracted for link: {link}")
                        return data
                    except Exception as e:
                        logger.error(f"Error processing link {link}: {e}")
                        return None
                
            tasks = [parse_link(link) for link in unique_links]
            ad_details_list = await asyncio.gather(*tasks)
            for ad_details in ad_details_list:
                for key, value in ad_details.items():
                    print(f"{key}: {value}")
                print("-" * 50)

            # ... Обработка результатов ...
            elapsed_time = time.time() - start_time
            logger.info(f"Parsing completed successfully with {len(ad_details_list)} ads in {elapsed_time:.2f} seconds")
        except Exception as e:
            logger.error(f"Ошибка во время парсинга: {e}")
        finally:
            await self.close_session()
            logger.info("Session closed")


# Инициализация и запуск парсера
if __name__ == '__main__':
    parser = AsyncCarAdParser()
    asyncio.run(parser.main())
