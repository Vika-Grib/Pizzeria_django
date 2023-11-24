# coding=utf-8
import time
import zmq
import json
import sqlite3
import asyncio
import random

from apscheduler.schedulers.background import BackgroundScheduler
# импорт фонового расписания задач - чтобы вместе с django запускался этот код

# added schedule, ensure its only done once - см. в APPS.PY, благодаря ему запускается очередь
def schedule():
    scheduler = BackgroundScheduler({'apscheduler.job_defaults.max_instances': 2}) # ув максимального количества заданий - такого условия не достигнем, скорее гибкость (на случай такого же сообщения, но ткт запускается 1 раз - то..)
    if not scheduler.get_job('get_message'):  #добавляет гибкости,  проверка чтобы уже не выполняло такое же задание
        scheduler.add_job(tr, id='get_message')
        scheduler.start()


def work_with_transfer_orders_db(transfer_orders):
    conn = sqlite3.connect('C:\\Users\\Lenovo\\PycharmProjects\\Pizza\\PizzaParadise\\db.sqlite3')
    cursor = conn.cursor()
    cursor.execute(f'''UPDATE active_orders SET transfer_orders={transfer_orders}''')
    conn.commit()

# python manage.py runserver


def transfering(message):
    conn = sqlite3.connect('C:\\Users\\Lenovo\\PycharmProjects\\Pizza\\PizzaParadise\\db.sqlite3')
    cursor = conn.cursor()
    cursor.execute(f'''UPDATE customer_order SET status="Курьер в пути!" WHERE order_id="{message['order_id']}"''')
    conn.commit()
    send_to_notify(message, 'Курьер в пути!')  # отправили курьером
    trancfering_time = random.randint(7,12)
    time.sleep(trancfering_time)
    conn = sqlite3.connect('C:\\Users\\Lenovo\\PycharmProjects\\Pizza\\PizzaParadise\\db.sqlite3')
    cursor = conn.cursor()
    cursor.execute('SELECT * from active_orders')
    transfer_orders = list(cursor.fetchall())[0][1]
    if transfer_orders >= 1:
        transfer_orders -= 1
        work_with_transfer_orders_db(transfer_orders)
        print('*', 'Transfering!', '*', 'Доставлено за время: ', trancfering_time)
        conn = sqlite3.connect('C:\\Users\\Lenovo\\PycharmProjects\\Pizza\\PizzaParadise\\db.sqlite3')
        cursor = conn.cursor()
        cursor.execute(f'''UPDATE customer_order SET status="Заказ доставлен" WHERE order_id="{message['order_id']}"''')
        conn.commit()
        send_to_notify(message, 'Заказ доставлен')


async def processing_transferinga(socket, transfer_orders):
    #  Wait for next request from client
    message = socket.recv_json()  # запрос на то что мы получим сообщение, запускается постоянно - через ctrl+C нельзя было остановить сервер и следовательно след команда, кот.останавливает цикл
    print(message, '#####')
    num_of_pizzas = message['num_of_pizzas']
    conn = sqlite3.connect('C:\\Users\\Lenovo\\PycharmProjects\\Pizza\\PizzaParadise\\db.sqlite3')
    cursor = conn.cursor()
    cursor.execute(f'''INSERT INTO transfer_order(order_id, title, status) VALUES (?,?,?)''', (message['order_id'], message['title'], "Пицца готова")) # выбираем где статус готова и пиццы в заказе
    conn.commit()
    cursor.execute(f'''SELECT * from transfer_order WHERE order_id="{message['order_id']}" AND status="Пицца готова"''') # выбираем где статус готова и пиццы в заказе
    order_pizzas = list(cursor.fetchall())
    #  Do some 'work' - занимает время на обработку и ему нужна 1 сек, чтобы делать что-то дальше
    time.sleep(2)
    print('order_pizzas!!!!!!!!!!!!!!!!!!!!!!!!!!!!', order_pizzas)
    if int(num_of_pizzas) == len(order_pizzas):
        transfer_orders += 1
        work_with_transfer_orders_db(transfer_orders) # доб в базу данных +1 и курьер получает заказ в очередь чтобы ехать - в этом процесс
        schedule_1(message, transfer_orders) # запускаем процесс трансферинга перманентно
        elem = message  # на случай если получим не только json, но и сообщение какое-нибудь
        print(f"Received transfering request: {elem}")



def schedule_1(message, active_orders): # отвечает за работу доставки!
    scheduler = BackgroundScheduler({'apscheduler.job_defaults.max_instances': 2})  # сам процесс на отправку доставки не запускался дважды - проверяет есть ли уже такое активное задание
    scheduler.add_job(lambda: transfering(message), id=f'process-{active_orders}')
    scheduler.start()

def tr():
    print('HELLLLOOOOW')
    conn = sqlite3.connect('C:\\Users\\Lenovo\\PycharmProjects\\Pizza\\PizzaParadise\\db.sqlite3')
    cursor = conn.cursor()
    context = zmq.Context()  # испол-е библиотеки, по сути тип созданный нами брокер - Context, библиотека zmq соединяет socket и брокер - contex - это реализация брокера
    socket = context.socket(zmq.PULL) # будет вытягивать сообщения
    socket.bind("tcp://*:5553")  # закрепляем конкретный порт за socket-ом

    while True:
        cursor.execute('SELECT * from active_orders')
        transfer_orders = list(cursor.fetchall())[0][1]  # выбирает все элементы подходящие запросу
        if transfer_orders < 5:
            asyncio.run(processing_transferinga(socket, transfer_orders))  #заказы прих в очередь, запускаем очередь трансферинга и из очереди достаем заказ и отдаем
            print('active_transfer_orders: ', transfer_orders)
        else:
            pass


def send_to_notify(message, status): # эта ф-ция переход на новый этап очереди (тут след processing)
    context = zmq.Context()
    socket = context.socket(zmq.PUSH)  # пушем отправляем, а пулэм забираем сообщение уже в процессинге
    socket.connect("tcp://localhost:5552")
    order_id = message['unique_id']
    notification = {'order_id': order_id, 'status': status}
    socket.send_json(notification)
    print(f"Send to notify [ {notification} ]")