from django.test import TestCase
from django_tasker_geobase import geocoder


class Geobase(TestCase):

    def test_vegetation(self):
        vegetation = geocoder.geo(query="37.601278, 55.730564")


    def test_zipcode(self):
        postal_office = geocoder.zipcode(zipcode=630024)
        self.assertEqual(postal_office.ru, "17")
        self.assertEqual(postal_office.en, "17")
        self.assertEqual(postal_office.type, 7)
        self.assertEqual(postal_office.timezone, 'Asia/Novosibirsk')
        self.assertEqual(postal_office.latitude, 54.964401)
        self.assertEqual(postal_office.longitude, 82.908177)
        self.assertEqual(postal_office.zipcode, '630024')

    def test_address(self):
        apartment = geocoder.geo(query="Новосибирск улица Мира, 61к1 кв.11")
        self.assertEqual(apartment.zipcode, '630024')
        self.assertEqual(apartment.longitude, 82.940462)
        self.assertEqual(apartment.latitude, 54.959423)
        self.assertEqual(apartment.timezone, 'Asia/Novosibirsk')
        self.assertEqual(apartment.type, 15)
        self.assertEqual(apartment.ru, '11')
        self.assertEqual(apartment.en, '11')

        house = apartment.parent
        self.assertEqual(house.ru, "61к1")
        self.assertEqual(house.en, "61к1")
        self.assertEqual(house.type, 7)
        self.assertEqual(house.timezone, 'Asia/Novosibirsk')
        self.assertEqual(house.latitude, 54.959423)
        self.assertEqual(house.longitude, 82.940462)
        self.assertEqual(house.zipcode, '630024')

        street = house.parent
        self.assertEqual(street.ru, "улица Мира")
        self.assertEqual(street.en, "ulitsa Mira")
        self.assertEqual(street.type, 6)
        self.assertEqual(street.timezone, 'Asia/Novosibirsk')
        self.assertIsNone(street.latitude)
        self.assertIsNone(street.longitude)
        self.assertIsNone(street.zipcode)

        locality = street.parent
        self.assertEqual(locality.ru, "Новосибирск")
        self.assertEqual(locality.en, "Novosibirsk")
        self.assertEqual(locality.timezone, "Asia/Novosibirsk")
        self.assertIsNone(street.zipcode)
        self.assertEqual(locality.latitude, 55.030199)
        self.assertEqual(locality.longitude, 82.92043)

        province = locality.parent
        self.assertEqual(province.ru, "Новосибирская область")
        self.assertEqual(province.en, "Novosibirsk Region")
        self.assertIsNone(street.zipcode)
        self.assertIsNone(street.latitude)
        self.assertIsNone(street.longitude)
        self.assertEqual(street.timezone, "Asia/Novosibirsk")

        province = province.parent
        self.assertEqual(province.ru, "Сибирский федеральный округ")
        self.assertEqual(province.en, "Sibirskiy federalny okrug")
        self.assertIsNone(province.timezone)
        self.assertIsNone(province.latitude)
        self.assertIsNone(province.longitude)
        self.assertIsNone(province.zipcode)

        country = province.parent
        self.assertEqual(country.ru, "Россия")
        self.assertEqual(country.en, "Russia")
        self.assertIsNone(province.timezone)
        self.assertIsNone(province.latitude)
        self.assertIsNone(province.longitude)
        self.assertIsNone(province.zipcode)

    def test_geopoint(self):
        house = geocoder.geo(query="82.940462, 54.959423")

        self.assertEqual(house.ru, "61к1")
        self.assertEqual(house.en, "61к1")
        self.assertEqual(house.type, 7)
        self.assertEqual(house.timezone, 'Asia/Novosibirsk')
        self.assertEqual(house.latitude, 54.959423)
        self.assertEqual(house.longitude, 82.940462)
        self.assertEqual(house.zipcode, '630024')

        street = house.parent
        self.assertEqual(street.ru, "улица Мира")
        self.assertEqual(street.en, "ulitsa Mira")
        self.assertEqual(street.type, 6)
        self.assertEqual(street.timezone, 'Asia/Novosibirsk')
        self.assertIsNone(street.latitude)
        self.assertIsNone(street.longitude)
        self.assertIsNone(street.zipcode)

        locality = street.parent
        self.assertEqual(locality.ru, "Новосибирск")
        self.assertEqual(locality.en, "Novosibirsk")
        self.assertEqual(locality.timezone, "Asia/Novosibirsk")
        self.assertIsNone(street.zipcode)
        self.assertEqual(locality.latitude, 55.030199)
        self.assertEqual(locality.longitude, 82.92043)

        province = locality.parent
        self.assertEqual(province.ru, "Новосибирская область")
        self.assertEqual(province.en, "Novosibirsk Region")
        self.assertIsNone(street.zipcode)
        self.assertIsNone(street.latitude)
        self.assertIsNone(street.longitude)
        self.assertEqual(street.timezone, "Asia/Novosibirsk")

        province = province.parent
        self.assertEqual(province.ru, "Сибирский федеральный округ")
        self.assertEqual(province.en, "Sibirskiy federalny okrug")
        self.assertIsNone(province.timezone)
        self.assertIsNone(province.latitude)
        self.assertIsNone(province.longitude)
        self.assertIsNone(province.zipcode)

        country = province.parent
        self.assertEqual(country.ru, "Россия")
        self.assertEqual(country.en, "Russia")
        self.assertIsNone(province.timezone)
        self.assertIsNone(province.latitude)
        self.assertIsNone(province.longitude)
        self.assertIsNone(province.zipcode)

    def test_ip4(self):
        result = geocoder.ip(ip="8.8.8.8")
        self.assertEqual(result.timezone, 'America/New_York')

        country = result.get_family().get(type=1)
        self.assertEqual(country.en, 'United States of America')
        self.assertEqual(country.ru, 'Соединённые Штаты Америки')

