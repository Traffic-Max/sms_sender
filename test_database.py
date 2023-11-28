# test_database.py
from database.database import get_all_ads, init_db, Session

def test_get_all_ads():
    # Инициализация базы данных (если нужно)
    init_db()

    # Создание сессии для работы с базой данных
    db_session = Session()

    try:
        nums = get_all_ads()
        print(len(nums))
        # for ad in ads:
            # print(f"Объявление: {ad.brand} {ad.model}, Телефоны: {[phone.number for phone in ad.phone_numbers]}")
    except Exception as e:
        print(f"Ошибка при получении данных: {e}")
    finally:
        db_session.close()

if __name__ == "__main__":
    test_get_all_ads()
