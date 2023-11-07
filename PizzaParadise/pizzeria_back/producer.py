# coding=utf-8
import zmq

context = zmq.Context()

#  Socket to talk to server
print("Connecting to server…")
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

def send_message(data):
    #  Do 10 requests, waiting each time for a response
    for request in range(10):
        print(f"Sending request {request}")

        socket.send_json(data)

        #  Get the reply. Любой (либо подтвержден либо нет)
        message = socket.recv()
        print(f"Received reply {request} [ {message} ]")


def send_quit_message():
    socket.send_json({"order_id": -1})

dt = {"name": "Pizza 1", "order_id": 12, "description": "cheese, beef, tomato", "price": 15}
send_message(dt)
#send_quit_message()