# coding=utf-8
import time
import zmq
import sqlite3

from apscheduler.schedulers.background import BackgroundScheduler
# импорт фонового расписания задач - чтобы вместе с django запускался этот код

# # добавляем schedule, убедиться что запускается один раз - см. в APPS.PY, благодаря ему запускается очередь
def schedule():
    scheduler = BackgroundScheduler({'apscheduler.job_defaults.max_instances': 2}) #  проверяет, существует ли уже задача, ув максимального количества заданий - такого условия не достигнем, скорее гибкость (на случай такого же сообщения, но ткт запускается 1 раз - то..)
    if not scheduler.get_job('get_message'):  #добавляет гибкости,  проверка чтобы уже не выполняло такое же задание
        scheduler.add_job(tr, id='get_message')
        scheduler.start()

def tr():
    context = zmq.Context()  # испол-е библиотеки, по сути тип созданный нами брокер - Contex, библиотека zmq соединяет socket и брокер - contex - это реализация брокера
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:5555")  # закрепляем конкретный порт за socket-ом

    while True:
        message = socket.recv_json()  # запрос на то что мы получим сообщение, запускается постоянно - через ctrl+C нельзя было остановить сервер и следовательно след команда, кот.останавливает цикл
        time.sleep(1)
        order_confirmed = check_order(message['order_id'])
        message['unique_id'] = str(message['order_id']) + '_' + str(message['id'])
        if order_confirmed:
            schedule_1(message, 'Принят')
            print("sending to DB")
            message['status'] = 'Принят!'
            send_to_db(message)
            #  Send reply back to client
            socket.send(b"Your order confirmed and accepted!")
            send_to_next_queue(message)  # после того как отправили в БД, мы также отправляем в след очередь
        else:
            schedule_1(message, 'unconfirmed')
            #  Send reply back to client
            socket.send(b"Your order is unconfirmed")


def send_to_next_queue(message): # эта ф-ция переход на новый этап очереди (тут след processing)
    context = zmq.Context()
    socket = context.socket(zmq.PUSH)  # пушем отправляем, а пулэм забираем сообщение уже в процессинге
    socket.connect("tcp://localhost:5554")
    socket.send_json(message)
    print(f"Send to processing queue [ {message} ]")


def check_order(id=None):
    return True


def send_to_db(message):
    # Connect к Базe данных
    conn = sqlite3.connect('C:\\Users\\Lenovo\\PycharmProjects\\Pizza\\PizzaParadise\\db.sqlite3')
    #conn = sqlite3.connect('F:\\Pizza\\PizzaParadise\\db.sqlite3')
    # Создаем объект cursor, который позволяет нам взаимодействовать с базой данных и добавлять записи
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO customer_order(unique_id, price, title, size, image, order_id, status, pizza_id) VALUES (?,?,?,?,?,?,?,?)''',
                   (message['unique_id'], message['price'], message['title'], message['size'], message['img'], message['order_id'], message['status'], message['id']))
    conn.commit()


def send_to_notify(message, status): # эта ф-ция переход на новый этап очереди (тут след processing)
    context = zmq.Context()
    socket = context.socket(zmq.PUSH)  # пушем отправляем, а пулэм забираем сообщение уже в процессинге
    socket.connect("tcp://localhost:5552")
    print(message)
    order_id = message['unique_id']
    notification = {'order_id': order_id, 'status': status}
    socket.send_json(notification)
    print(f"Send to notify [ {notification} ]")

# добавляем функцию def send_to_notify в schedule_1 - чтобы всем отправлялись асинхронно уведомления
def schedule_1(message, status): # отвечает за работу печки!
    scheduler = BackgroundScheduler({'apscheduler.job_defaults.max_instances': 2}) # запускаем асинхронно кукинг готовку и дальше мы могли принимать новые пиццы
    scheduler.add_job(lambda: send_to_notify(message, status), id=f'process')
    scheduler.start()