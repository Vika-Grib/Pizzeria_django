# coding=utf-8
import zmq, json, sys, ast

context = zmq.Context()

#  Socket to talk to server
print("Connecting to server…")
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")


def send_message(data):
    # print(data, '!!')
    pizzas = data['pizza']
    # print(pizzas, '!!')
    for pizza in pizzas:
        pizza['num_of_pizzas'] = len(pizzas) # количество пицц для одного заказа
        print(f"Sending pizza info {pizza}")
        socket.send_json(pizza)

        # Получаем ответ. Любой (либо подтвержден либо нет)
        message = socket.recv()
        print(f"Received reply {pizza} [ {message} ]")


def send_quit_message():
    socket.send_json({"order_id": -1})

#send_quit_message()