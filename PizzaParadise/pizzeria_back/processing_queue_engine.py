# coding=utf-8
import time
import zmq
import json
import sqlite3
import asyncio

from apscheduler.schedulers.background import BackgroundScheduler
# импорт фонового расписания задач - чтобы вместе с django запускался этот код

# added schedule, ensure its only done once - см. в APPS.PY, благодаря ему запускается очередь
def schedule():
    scheduler = BackgroundScheduler({'apscheduler.job_defaults.max_instances': 2}) # ув максимального количества заданий - такого условия не достигнем, скорее гибкость (на случай такого же сообщения, но ткт запускается 1 раз - то..)
    if not scheduler.get_job('get_message'):  #добавляет гибкости,  проверка чтобы уже не выполняло такое же задание
        scheduler.add_job(tr, id='get_message')
        scheduler.start()


def work_with_active_orders_db(active_orders):
    conn = sqlite3.connect('C:\\Users\\Lenovo\\PycharmProjects\\Pizza\\PizzaParadise\\db.sqlite3')
    cursor = conn.cursor()
    cursor.execute(f'''UPDATE active_orders SET active_orders={active_orders}''')
    conn.commit()

# python manage.py runserver


def cooking():
    conn = sqlite3.connect('C:\\Users\\Lenovo\\PycharmProjects\\Pizza\\PizzaParadise\\db.sqlite3')
    cursor = conn.cursor()
    cursor.execute('SELECT * from active_orders')
    active_orders = list(cursor.fetchall())[0][0]
    #time.sleep(3)
    if active_orders >=1:
        active_orders -= 1
        work_with_active_orders_db(active_orders)
        print('*', 'cooked!', '*')


async def processing(socket, active_orders):
    #  Wait for next request from client
    message = socket.recv_json()  # запрос на то что мы получим сообщение, запускается постоянно - через ctrl+C нельзя было остановить сервер и следовательно след команда, кот.останавливает цикл
    active_orders += 1
    work_with_active_orders_db(active_orders)
    elem = message  # на случай если получим не только json, но и сообщение какое-нибудь
    print(f"Received processing request: {elem}")

    #  Do some 'work' - занимает время на обработку и ему нужна 1 сек, чтобы делать что-то дальше
    time.sleep(1)

def schedule_1(): # отвечает за работу печки!
    print('IN!')

    scheduler = BackgroundScheduler({'apscheduler.job_defaults.max_instances': 2})
    if not scheduler.get_job('process'):
        scheduler.add_job(lambda: cooking(), 'interval', seconds=3, id='process')
        scheduler.start()

def tr():
    schedule_1()
    conn = sqlite3.connect('C:\\Users\\Lenovo\\PycharmProjects\\Pizza\\PizzaParadise\\db.sqlite3')
    cursor = conn.cursor()
    context = zmq.Context()  # испол-е библиотеки, по сути тип созданный нами брокер - Context, библиотека zmq соединяет socket и брокер - contex - это реализация брокера
    socket = context.socket(zmq.PULL) # будет вытягивать сообщения
    socket.bind("tcp://*:5554")  # закрепляем конкретный порт за socket-ом

    while True:
        cursor.execute('SELECT * from active_orders')
        active_orders = list(cursor.fetchall())[0][0]
        #print('A_O ', active_orders)
        if active_orders <= 5:
            asyncio.run(processing(socket, active_orders))  # когда происходит asyncio.run, то обновляет значения в work_proc_bd
            print('active_orders_previous: ', active_orders)
            cursor.execute('SELECT * from active_orders')
            active_orders = list(cursor.fetchall())[0][0]
            #asyncio.run(cooking(active_orders))
            print('active_orders: ', active_orders)

        else:
            pass

