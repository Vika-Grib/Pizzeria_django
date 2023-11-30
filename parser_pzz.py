import requests
from bs4 import BeautifulSoup as bs
import json
import sqlite3

url = 'https://pzz.by/api/v1/pizzas?load=ingredients,filters&filter=meal_only:0&order=position:asc'
url_1 = 'https://pzz.by/api/v1/snacks?load=modifications&filter=meal_only:0,parent_id:is:null&order=position:asc'

# # парсим с сайта меню пицц
# def get_content(url):
#     headers = {
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36'
#     }
#     resp = requests.get(url, headers=headers)
#     current_page_pizzas = resp.json()['response']['data']
#     print(current_page_pizzas)
#     pizza_data = []
#     conn = sqlite3.connect('C:\\Users\\Lenovo\\PycharmProjects\\Pizza\\PizzaParadise\\db.sqlite3')
#     cursor = conn.cursor()
#     for pizza in current_page_pizzas:
#         print(pizza)
#         pizza_id = pizza['id']
#         title = pizza['title']
#         photo_small = pizza['photo_small']
#         big_price = pizza['big_price']/10000
#         thin_price = pizza['thin_price']/10000
#         medium_price = pizza['medium_price']/10000
#         ingredients = pizza['anonce']
#         cursor.execute('INSERT INTO Pizzas(id, title, big_price, medium_price, thin_price, ingredients, photo) VALUES (?, ?, ?, ?, ?, ?, ?)', (pizza_id, title, big_price, medium_price, thin_price, ingredients, photo_small))
#         conn.commit()
#         pizza_data.append({'pizza_id': pizza_id,
#                            'title': title,
#                            'photo_small': photo_small,
#                            'big_price': big_price,
#                            'thin_price': thin_price,
#                            'medium_price': medium_price,
#                            'ingredients': ingredients,
#                            })
#     # for title in pizza_data:
#     #     print(title)
#     return pizza_data
# pizza_info_list = get_content(url)
#
# # conn = sqlite3.connect('C:\\Users\\Lenovo\\PycharmProjects\\Pizza\\PizzaParadise\\db.sqlite3')
# # cursor = conn.cursor()
# # cursor.execute('''CREATE TABLE Pizzas (id INTEGER PRIMARY KEY, title TEXT, big_price FLOAT, medium_price FLOAT, thin_price FLOAT, ingredients JSON, photo IMG)''')
#

#
# # парсим с сайта меню закуски
# def get_content(url):
#     headers = {
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36'
#     }
#     resp = requests.get(url, headers=headers)
#     current_page_snacks = resp.json()['response']['data']
#     print(current_page_snacks)
#     snack_data = []
#     conn = sqlite3.connect('C:\\Users\\Lenovo\\PycharmProjects\\Pizza\\PizzaParadise\\db.sqlite3')
#     cursor = conn.cursor()
#     for snack in current_page_snacks:
#         print(snack)
#         title = snack['title']
#         photo = snack['photo1']
#         big_price = snack['big_price']/10000
#         short_description = snack['anonce']
#         cursor.execute('INSERT INTO Snacks(title, big_price, short_description, photo) VALUES (?, ?, ?, ?)', (title, big_price, short_description, photo))
#         conn.commit()
#         snack_data.append({'title': title,
#                            'photo': photo,
#                            'big_price': big_price,
#                            'short_description': short_description,
#                            })
#     for title in snack_data:
#         print(title)
#     return snack_data
#
#
# # conn = sqlite3.connect('C:\\Users\\Lenovo\\PycharmProjects\\Pizza\\PizzaParadise\\db.sqlite3')
# # cursor = conn.cursor()
# # cursor.execute('''CREATE TABLE Snacks (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, big_price FLOAT, short_description JSON, photo IMG)''')
#
# snack_info_list = get_content(url_1)

