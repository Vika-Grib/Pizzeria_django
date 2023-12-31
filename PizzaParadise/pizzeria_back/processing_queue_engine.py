# coding=utf-8
import time
import zmq
import sqlite3
import asyncio

from apscheduler.schedulers.background import BackgroundScheduler

# добавляем schedule, убедиться что запускается один раз - см. в APPS.PY, благодаря ему запускается очередь
def schedule():
    scheduler = BackgroundScheduler({'apscheduler.job_defaults.max_instances': 2})
    if not scheduler.get_job('get_message1'):
        scheduler.add_job(tr, id='get_message1')
        scheduler.start()


def work_with_active_orders_db(active_orders):
    conn = sqlite3.connect('C:\\Users\\Lenovo\\PycharmProjects\\Pizza\\PizzaParadise\\db.sqlite3')
    cursor = conn.cursor()
    cursor.execute(f'''UPDATE active_orders SET active_orders={active_orders}''')
    conn.commit()


def cooking(message):  # не отправляет сам заказ, а просто готовит заказы (ум их количество)
    send_to_notify(message,'В печи')
    order_id = message['order_id']
    pizza_id = message['id']  # чтобы выбирать из количества пицц в заказе по id
    num_of_pizzas = message['num_of_pizzas']  # по ключу к количеству пицц, чтобы взять последнюю
    if int(pizza_id) == int(num_of_pizzas) - 1:
        update_order_for_user(order_id, 'В печи')
    time.sleep(10)
    conn = sqlite3.connect('C:\\Users\\Lenovo\\PycharmProjects\\Pizza\\PizzaParadise\\db.sqlite3')
    cursor = conn.cursor()
    cursor.execute('SELECT * from active_orders')
    active_orders = list(cursor.fetchall())[0][0]  # наши печки, которые готовят
    if active_orders >= 1:
        active_orders -= 1
        work_with_active_orders_db(active_orders)
        send_to_next_queue(message)
        send_to_notify(message, 'Пицца готова')
        if int(pizza_id) == int(num_of_pizzas) - 1:
            update_order_for_user(order_id, 'Заказ готов')



def update_order_for_user(order_id, status):
    conn = sqlite3.connect('C:\\Users\\Lenovo\\PycharmProjects\\Pizza\\PizzaParadise\\db.sqlite3')
    cursor = conn.cursor()
    cursor.execute(f'''UPDATE pizzeria_back_user_order SET status="{status}" WHERE order_id="{order_id}"''')
    conn.commit()




async def processing(socket): # добавляет заказы в бд
    #  ожидаем след запрос, след заказ, пиццу
    message = socket.recv_json()  # запрос на то что мы получим сообщение, запускается постоянно - через ctrl+C нельзя было остановить сервер и следовательно след команда, кот.останавливает цикл
    conn = sqlite3.connect('C:\\Users\\Lenovo\\PycharmProjects\\Pizza\\PizzaParadise\\db.sqlite3')
    cursor = conn.cursor()
    cursor.execute('SELECT * from active_orders')
    active_orders = list(cursor.fetchall())[0][0]
    active_orders += 1
    work_with_active_orders_db(active_orders) # обновляем в базе данные +1
    schedule_1(message, active_orders) # чтобы дальше передал в готовку кукинг конкретный заказ
    elem = message  # на случай если получим не только json, но и сообщение какое-нибудь
    print(f"Received processing request: {elem}")

    #  Do some 'work' - занимает время на обработку и ему нужна 1 сек, чтобы делать что-то дальше
    time.sleep(1)

def schedule_1(message, active_orders): # отвечает за работу печки!
    print('IN!')

    scheduler = BackgroundScheduler({'apscheduler.job_defaults.max_instances': 2}) # запускаем асинхронно кукинг готовку и дальше мы могли принимать новые пиццы
    # if not scheduler.get_job('process'):
    scheduler.add_job(lambda: cooking(message), id=f'process-{active_orders}') # add_job  - доб задание
    scheduler.start() # запускает выполнение ассинхронно

def tr():
    conn = sqlite3.connect('C:\\Users\\Lenovo\\PycharmProjects\\Pizza\\PizzaParadise\\db.sqlite3')
    cursor = conn.cursor()
    context = zmq.Context()  # испол-е библиотеки, по сути тип созданный нами брокер - Context, библиотека zmq соединяет socket и брокер - contex - это реализация брокера
    socket = context.socket(zmq.PULL) # будет вытягивать сообщения
    socket.bind("tcp://*:5554")  # закрепляем конкретный порт за socket-ом

    while True:
        cursor.execute('SELECT * from active_orders')
        active_orders = list(cursor.fetchall())[0][0]
        #print('A_O ', active_orders)
        if active_orders < 5:  # запускаем процессинг когда меньше 5
            asyncio.run(processing(socket))  # когда происходит asyncio.run асинхр процесс, то обновляет значения в work_proc_bd
            print('active_orders: ', active_orders)
        else:
            pass


def send_to_next_queue(message): # эта ф-ция переход на новый этап очереди (тут след processing)
    context = zmq.Context()
    socket = context.socket(zmq.PUSH)  # пушем отправляем, а пулэм забираем сообщение уже в процессинге
    socket.connect("tcp://localhost:5553")
    socket.send_json(message)
    print(f"Send to transfer [ {message} ]")

def send_to_notify(message, status): # эта ф-ция переход на новый этап очереди (тут след processing)
    context = zmq.Context()
    socket = context.socket(zmq.PUSH)  # пушем отправляем, а пулэм забираем сообщение уже в процессинге
    socket.connect("tcp://localhost:5552")
    order_id = message['unique_id']
    notification = {'order_id': order_id, 'status': status}
    socket.send_json(notification)
    print(f"Send to notify [ {notification} ]")