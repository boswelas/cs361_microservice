import zmq
import time
import json

context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

with open("students.json") as f:
    file_1_contents = json.load(f)
    f.close()
socket.send_json(file_1_contents)
time.sleep(1)

file_name = socket.recv(100).decode()
msg1 = socket.send("received name".encode())
file_size = socket.recv(100).decode()
msg2 = socket.send("received size".encode())

with open("./" + file_name, "wb") as file:
    count = 0
    while count < int(file_size):
        data = socket.recv(1024)
        if not data:
            break
        file.write(data)
        socket.send("got data".encode())
        count += len(data)
socket.recv(100).decode()
socket.close()


