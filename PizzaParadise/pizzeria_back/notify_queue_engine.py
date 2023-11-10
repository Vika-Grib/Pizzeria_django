# coding=utf-8
import time
import zmq
import json
import sqlite3
import asyncio
import random
import smtplib
import mailtrap as mt

from apscheduler.schedulers.background import BackgroundScheduler
# импорт фонового расписания задач - чтобы вместе с django запускался этот код

# added schedule, ensure its only done once - см. в APPS.PY, благодаря ему запускается очередь
def schedule():
    scheduler = BackgroundScheduler({'apscheduler.job_defaults.max_instances': 2}) # ув максимального количества заданий - такого условия не достигнем, скорее гибкость (на случай такого же сообщения, но ткт запускается 1 раз - то..)
    if not scheduler.get_job('get_message'):  #добавляет гибкости,  проверка чтобы уже не выполняло такое же задание
        scheduler.add_job(tr, id='get_message')
        scheduler.start()

# python manage.py runserver

def tr():
    conn = sqlite3.connect('C:\\Users\\Lenovo\\PycharmProjects\\Pizza\\PizzaParadise\\db.sqlite3')
    cursor = conn.cursor()
    context = zmq.Context()  # испол-е библиотеки, по сути тип созданный нами брокер - Context, библиотека zmq соединяет socket и брокер - contex - это реализация брокера
    socket = context.socket(zmq.PULL) # будет вытягивать сообщения
    socket.bind("tcp://*:5552")  # закрепляем конкретный порт за socket-ом

    while True:
        asyncio.run(process_of_notifications(socket))  #заказы прих в очередь, запускаем очередь трансферинга и из очереди достаем заказ и отдаем



async def process_of_notifications(socket):
    #  Wait for next request from client
    message = socket.recv_json()  # запрос на то что мы получим сообщение, запускается постоянно - через ctrl+C нельзя было остановить сервер и следовательно след команда, кот.останавливает цикл
    schedule_1(message) # запускаем процесс отправки уведомлений перманентно
    elem = message  # на случай если получим не только json, но и сообщение какое-нибудь
    print(f"Received notifying: {elem}")

    #  Do some 'work' - занимает время на обработку и ему нужна 1 сек, чтобы делать что-то дальше
    time.sleep(1)


def schedule_1(message): # отвечает за работу доставки!
    scheduler = BackgroundScheduler({'apscheduler.job_defaults.max_instances': 2})  # сам процесс на отправку доставки не запускался дважды - проверяет есть ли уже такое активное задание
    scheduler.add_job(lambda: notify(message), id='process')
    scheduler.start()


def notify(message):
    order_id = message['order_id']
    status = message['status']
    update_status(order_id, status)


def update_status(order_id, status):
    conn = sqlite3.connect('C:\\Users\\Lenovo\\PycharmProjects\\Pizza\\PizzaParadise\\db.sqlite3')
    cursor = conn.cursor()
    cursor.execute(f'UPDATE customer_order SET status="{status}" WHERE id={order_id}')
    conn.commit()
