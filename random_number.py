import random
import zmq

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")


while True:
    text = socket.recv(100).decode()
    print(text)
    if text == 'run':
        random_num = str(random.randint(0, 2))
        socket.send(random_num.encode())
    else:
        socket.send("400 Bad Request".encode())
        
        
