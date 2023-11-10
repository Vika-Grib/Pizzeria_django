# coding=utf-8
import zmq

context = zmq.Context()

#  Socket to talk to server
print("Connecting to server…")
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

def send_message(data):
    #  Do 10 requests, waiting each time for a response
    for request in data:
        print(f"Sending request {request}")
        socket.send_json(request)

        #  Get the reply. Любой (либо подтвержден либо нет)
        message = socket.recv()
        print(f"Received reply {request} [ {message} ]")


def send_quit_message():
    socket.send_json({"order_id": -1})

dt = {'title': 'назв', 'ingredients': 'ingredients', 'big_price': 12, 'medium_price': 9, 'thin_price':9, 'image': 'image', 'id': 2, 'status': '-'}
dt1 = {'title': 'назв2', 'ingredients': 'ingredients2', 'big_price': 14, 'medium_price': 12, 'thin_price':22, 'image': 'image', 'id': 4, 'status': '-'}
dt2 = {'title': 'назв3', 'ingredients': 'ingredients', 'big_price': 15, 'medium_price': 5, 'thin_price':5, 'image': 'image', 'id': 5, 'status': '-'}
dt3 = {'title': 'назв', 'ingredients': 'ingredients', 'big_price': 82, 'medium_price': 29, 'thin_price':29, 'image': 'image', 'id': 3, 'status': '-'}
dt4 = {'title': 'назвssw', 'ingredients': 'ingredients', 'big_price': 56, 'medium_price': 9, 'thin_price':9, 'image': 'image', 'id': 7, 'status': '-'}
dt5 = {'title': 'назвss', 'ingredients': 'ingredients', 'big_price': 42, 'medium_price': 9, 'thin_price':9, 'image': 'image', 'id': 8, 'status': '-'}
data = [dt, dt1, dt2, dt3, dt4, dt5]
send_message(data)
#send_quit_message()