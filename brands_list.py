import requests
from bs4 import BeautifulSoup

# URL страницы со списком марок автомобилей
url = 'https://auto.ria.com/legkovie-catalog/'

# Отправка запроса на страницу
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Поиск всех элементов с марками автомобилей
brand_elements = soup.find_all('span', class_='name')

# Извлечение названий марок автомобилей
brands = [brand_element.get_text().strip() for brand_element in brand_elements]

print(brands)
