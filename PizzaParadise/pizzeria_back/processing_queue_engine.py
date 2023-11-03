# coding=utf-8

import time
import zmq
import json
import sqlite3

from apscheduler.schedulers.background import BackgroundScheduler
# импорт фонового расписания задач - чтобы вместе с django запускался этот код

# added schedule, ensure its only done once - см. в APPS.PY, благодаря ему запускается очередь
def schedule():
    scheduler = BackgroundScheduler({'apscheduler.job_defaults.max_instances': 2}) # ув максимального количества заданий - такого условия не достигнем, скорее гибкость (на случай такого же сообщения, но ткт запускается 1 раз - то..)
    if not scheduler.get_job('get_message'):  #добавляет гибкости,  проверка чтобы уже не выполняло такое же задание
        scheduler.add_job(tr, id='get_message')
        scheduler.start()

def tr():
    context = zmq.Context()  # испол-е библиотеки, по сути тип созданный нами брокер - Contex, библиотека zmq соединяет socket и брокер - contex - это реализация брокера
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:5554")  # закрепляем конкретный порт за socket-ом

    while True:
        #  Wait for next request from client
        message = socket.recv_json()  # запрос на то что мы получим сообщение, запускается постоянно - через ctrl+C нельзя было остановить сервер и следовательно след команда, кот.останавливает цикл

        if message["order_id"] == -1:  #чтобы не менять директорию - на случай если нужно остановить сервер, очередь - сами отправляем -1
            print("break")
            break
        elem = message   # на случай если получим не только json, но и сообщение какое-нибудь
        print(f"Received request: {elem}")

        #  Do some 'work' - занимает время на обработку и ему нужна 1 сек, чтобы делать что-то дальше
        time.sleep(1)


        # if :
        #     #  Send reply back to client
        #     socket.send(b"Your order was started to cook")
        # else:
        #     #  Send reply back to client
        #     socket.send(b"Your order is unconfirmed")

