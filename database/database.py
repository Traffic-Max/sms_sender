#database/database.py
from sqlalchemy import create_engine, Column, Integer, String, Float, Date, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

DATABASE_URL = "postgresql://postgres:2517@localhost/vehicles_platinum"

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
Base = declarative_base()

class CarAd(Base):
    __tablename__ = 'car_ads'
    id = Column(Integer, primary_key=True)
    brand = Column(String)
    model = Column(String)
    year = Column(Integer)
    mileage = Column(String)
    engine = Column(String)
    ad_date = Column(Date)
    seller_name = Column(String)
    is_new = Column(Boolean, default=True)
    category = Column(String)

    phone_numbers = relationship("PhoneNumber", backref="car_ad")

    def __repr__(self):
        return f"<CarAd(brand={self.brand}, model={self.model}, year={self.year}, mileage={self.mileage}, ad_date={self.ad_date}, seller_name={self.seller_name}, phone_number={self.phone_number})>"


class PhoneNumber(Base):
    __tablename__ = 'phone_numbers'
    id = Column(Integer, primary_key=True)
    number = Column(String)
    car_ad_id = Column(Integer, ForeignKey('car_ads.id'))

    def __repr__(self):
        return f"<PhoneNumber(number={self.number})>"


def add_car_ad(brand, model, year, mileage, engine, ad_date, seller_name, phone_numbers, is_new=True, category=None):
    session = Session()
    new_ad = CarAd(
        brand=brand,
        model=model,
        year=year,
        mileage=mileage,
        engine=engine,
        ad_date=ad_date,
        seller_name=seller_name,
        is_new=is_new,
        category=category
    )
    session.add(new_ad)
    session.flush()  # Для получения ID только что созданного объявления

    # Добавление телефонных номеров
    for number in phone_numbers:
        new_phone = PhoneNumber(number=number, car_ad_id=new_ad.id)
        session.add(new_phone)

    try:
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

def get_all_ads():
    session = Session()
    ads = session.query(CarAd).all()
    for ad in ads:
        print(f"Объявление: {ad.brand} {ad.model} {ad.ad_date} {ad.seller_name} {ad.mileage}, Телефоны: {[phone.number for phone in ad.phone_numbers]}")
    session.close()
    return ads

def init_db():
    # Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

# Инициализация базы данных
init_db()
