
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

# Константы
FILTER_URL = "https://auto.ria.com/uk/search/?indexName=auto&categories.main.id=1&country.import.usa.not=-1&region.id[0]=12&city.id[0]=12&price.currency=1&abroad.not=0&custom.not=1&page=0&size=100"
COMPARE_URL = "https://auto.ria.com/uk/auto_"
HEADERS = {
    'Cookie': '_gcl_au=1.1.707876906.1693575975; __utmc=79960839; ui=ab59f9bd0d5f66d0; _fbp=fb.1.1693575975051.673396265; _cc_id=80cf1657627e5f524f4bc5b091409709; gdpr=[2,3]; test_fast_search=3; _ga_KGL740D7XD=GS1.1.1694436370.27.1.1694437661.60.0.0; _ga_KGL740D7XD=deleted; _ga_1XC358ET5K=GS1.2.1695195758.37.1.1695195856.27.0.0; cto_bundle=UcX_xl9yTmRlMFNpaGZKaTl5cUhycE5WZmNBV0JPTDFHdEZCUUkyTFIzajklMkJLM0VvSDBzcFNlbjElMkY4Y05ncTlnRVdXOXNVJTJGYUx6TllTRFdWJTJGMUNsVFI3JTJGeUNBN2wyTGF5dmt5S2gzZGpUbnoxTEM5OVFMOUZhdUJ0OHBKZVJVU3V2Y3klMkYlMkZOMGVtTnV3ajFkSmZteXFXbWclMkZDV1pXQlJDZzI1a21iREJiWlRNYSUyQkppdlNGT0gzUHFwUWpBNlZZZ0M0TnBPTlRUYjdzOVgyWE9zVGFwenYxU1B3JTNEJTNE; AMP-CONSENT=amp-VNphoop22CqKNhDbv20eCg; slonik_utm_medium=share_final_page; slonik_utm_source=ios; extendedSearch=1; showNewFinalPage=1; g_state={"i_p":1701084796415,"i_l":4}; showNewFeatures=7; showNewNextAdvertisement=10; test_new_features=726; advanced_search_test=42; _ga_E241E4XQ26=GS1.1.1700134373.1.1.1700134379.54.0.0; descriptionHidden=1; ipp=20; ab-link-video-stories=2; ab_redesign=0; _ga=GA1.3.190258360.1693575975; _clck=1pzp3cz%7C2%7Cfgx%7C0%7C1421; _ga_QE9NBY8W7X=GS1.1.1700640245.1.1.1700640282.23.0.0; slonik_utm_campaign=ads_bu; promolink2=4; _504c2=http://10.42.12.237:3000; AMP_TOKEN=%24NOT_FOUND; _gid=GA1.2.1556869753.1700897404; PHPSESSID=XFt1i0XiYlHnqDM0O72vH2GKQNJxRxJg; ria_sid=50115496820727; __utma=79960839.190258360.1693575975.1700897402.1700900083.128; __utmz=79960839.1700900083.128.28.utmcsr=ios|utmccn=ads_bu|utmcmd=share_final_page; __utmt=1; __utmt_b=1; PHPSESSID=eyJ3ZWJTZXNzaW9uQXZhaWxhYmxlIjp0cnVlLCJ3ZWJQZXJzb25JZCI6MCwid2ViQ2xpZW50SWQiOjI4NzQ4MDA1NzMsIndlYkNsaWVudENvZGUiOjIyNDM1NjA0OCwid2ViQ2xpZW50Q29va2llIjoiYWI1OWY5YmQwZDVmNjZkMCIsIl9leHBpcmUiOjE3MDA5ODY0ODc0ODIsIl9tYXhBZ2UiOjg2NDAwMDAwfQ==; __gads=ID=6e723e6239d1e3e8-22d8a07262de000d:T=1693575976:RT=1700900087:S=ALNI_MYievLIwYiynpUCT5OzzLqcLIcngw; __gpi=UID=00000c6d635f4afd:T=1693575976:RT=1700900087:S=ALNI_MbJbZ5_NOYUEvQEcmtDWxoHcXU0KQ; _ga_KGL740D7XD=GS1.1.1700900082.153.1.1700900160.59.0.0; _ga=GA1.1.190258360.1693575975; __utmb=79960839.4.10.1700900083',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Host': 'auto.ria.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    'Accept-Language': 'en-GB,en;q=0.9',
    'Connection': 'keep-alive',
}

KNOWN_BRANDS = ['Volkswagen', 'Mercedes-Benz', 'BMW', 'Renault', 'Audi', 'Ford', 'Skoda', 'Opel', 'Nissan', 'Toyota', 'Hyundai', 'Mazda', 'Honda', 'Chevrolet', 'Peugeot', 'Kia', 'Daewoo', 'Mitsubishi', 'ЗАЗ', 'Citroen', 'Volvo', 'Lexus', 'Fiat', 'Jeep', 'Land Rover', 'Chery', 'Dacia', 'Dodge', 'Geely', 'Porsche', 'Infiniti', 'SEAT', 'Ford', 'Chevrolet', 'Tesla', 'Jeep', 'Dodge', 'Chrysler', 'Lincoln', 'Cadillac', 'Buick', 'GMC', 'Hummer', 'Pontiac', 'Land Rover', 'Jaguar', 'MINI', 'Rover', 'Bentley', 'MG', 'Rolls-Royce', 'Fiat', 'Alfa Romeo', 'Maserati', 'Lancia', 'Iveco', 'Lamborghini', 'Chery', 'Geely', 'BYD', 'Great Wall', 'JAC', 'Lifan', 'Dadi', 'Dongfeng', 'FAW', 'Hyundai', 'Kia', 'Daewoo', 'SsangYong', 'Volkswagen', 'BMW', 'Audi', 'Mercedes-Benz', 'Opel', 'Porsche', 'Smart', 'ВАЗ / Lada', 'ГАЗ', 'УАЗ', 'ЗАЗ', 'Богдан', 'Renault', 'Peugeot', 'Citroen', 'Nissan', 'Toyota', 'Mazda', 'Mitsubishi', 'Honda', 'Lexus', 'Subaru', 'Infiniti', 'Suzuki', 'Acura', 'Daihatsu', 'Isuzu']
