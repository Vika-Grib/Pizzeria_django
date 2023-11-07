# coding=utf-8

import time
import zmq
import json
import sqlite3

from apscheduler.schedulers.background import BackgroundScheduler
# импорт фонового расписания задач - чтобы вместе с django запускался этот код

# added schedule, ensure its only done once - см. в APPS.PY
def schedule():
    scheduler = BackgroundScheduler({'apscheduler.job_defaults.max_instances': 2}) # ув максимального количества заданий - такого условия не достигнем, скорее гибкость (на случай такого же сообщения, но ткт запускается 1 раз - то..)
    if not scheduler.get_job('get_message'):  #добавляет гибкости,  проверка чтобы уже не выполняло такое же задание
        scheduler.add_job(tr, id='get_message')
        scheduler.start()

def tr():
    context = zmq.Context()  # испол-е библиотеки, по сути тип созданный нами брокер - Contex, библиотека zmq соединяет socket и брокер - contex - это реализация брокера
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:5555")  # закрепляем конкретный порт за socket-ом

    while True:
        #  Wait for next request from client
        message = socket.recv_json()  # запрос на то что мы получим сообщение, запускается постоянно - через ctrl+C нельзя было остановить сервер и следовательно след команда, кот.останавливает цикл

        if message["order_id"] == -1:  #чтобы не менять директорию - на случай если нужно остановить сервер - сами отправляем -1
            print("break")
            break
        elem = message   # на случай если получим не только json, но и сообщение какое-нибудь
        print(f"Received request: {elem}")

        #  Do some 'work' - занимает время на обработку и ему нужна 1 сек, чтобы делать что-то дальше
        time.sleep(1)

        order_confirmed = check_order(elem['order_id'])
        if order_confirmed:
            print("sending to DB")
            send_to_db(elem)
            #  Send reply back to client
            socket.send(b"Your order confirmed and accepted!")
            send_to_next_queue(elem)  # после того как отправили в БД, мы также отправляем в след очередь
        else:
            #  Send reply back to client
            socket.send(b"Your order is unconfirmed")


def send_to_next_queue(message): # эта ф-ция переход на новый этап очереди (тут след processing)
    context = zmq.Context()
    socket = context.socket(zmq.PUSH)  # пушем отправляем, а пулэм забираем сообщение уже в процессинге
    socket.connect("tcp://localhost:5554")
    socket.send_json(message)
    print(f"Send [ {message} ]")


def check_order(id=None):
    return True

def send_to_db(message):
    # Connect к Базe данных
    conn = sqlite3.connect('C:\\Users\\Lenovo\\PycharmProjects\\Pizza\\PizzaParadise\\db.sqlite3')
    #conn = sqlite3.connect('F:\\Pizza\\PizzaParadise\\db.sqlite3')
    # Создаем объект cursor, который позволяет нам взаимодействовать с базой данных и добавлять записи
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO customer_order(name, description, price) VALUES (?,?,?)''',
                   (message['name'], message['description'], message['price']))
    conn.commit()
# python manage.py runserver

