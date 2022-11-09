import os
import pandas as pd
import zmq
import matplotlib.pyplot as plt
import time


context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")


def create_table(df):
    """Create a table from the given JSON file."""

    fig, ax = plt.subplots()

    fig.patch.set_visible(False)
    ax.axis('off')
    ax.axis('tight')

    # Create the table
    alternating_colors = ([['white'] * len(df.columns), ['lightgray'] * len(df.columns)] * len(df))
    alternating_colors = alternating_colors[:len(df)]
    table = ax.table(cellText=df.values,
                     colLabels=df.columns,
                     colColours=['lightblue']*len(df.columns),
                     cellColours=alternating_colors,
                     loc='center',
                     cellLoc='center')

    # Save figure as a PDF
    plt.savefig("./student_roster.pdf", format="pdf", bbox_inches="tight")
    plt.close()


while True:
    json_file = socket.recv_json()
    df = pd.DataFrame(json_file, columns=['First', 'Last', 'id'])
    create_table(df)
    file_name = "student_roster.pdf"
    time.sleep(1)
    file_size = os.path.getsize(file_name)

    socket.send(file_name.encode())
    msg1 = socket.recv(100).decode()
    file_size_str = str(file_size)
    socket.send(file_size_str.encode())
    msg2 = socket.recv(100).decode()

    with open(file_name, "rb") as file:
        count = 0
        while count < file_size:
            data = file.read(1024)
            if not data:
                break
            socket.send(data)
            count += len(data)
            data_msg = socket.recv(100).decode()
    socket.send("sent all".encode())
