import socket
from threading import Thread, Lock
import threading
import sys

def handle_client(conn, addr, users, lock):
    thread_data = threading.local()
    thread_data.composing = False
    thread_data.logged_in = False
    while True:
        
        data = conn.recv(1024).decode()
        if not data:
            break
        
        ### LOGIN LOGIC
        if data.startswith('LOGIN ') and  not thread_data.logged_in:
            thread_data.username = data[len('LOGIN '):].strip()
            if ' ' in thread_data.username:
                conn.close()
                break
            lock.acquire()
            if thread_data.username not in users:
                users[thread_data.username] = []
            lock.release()
            conn.send((str(len(users[thread_data.username])) + "\n").encode())
            thread_data.logged_in = True
            
        ### Send message if COMPOSE <receiver> was already given
        if thread_data.composing:
            lock.acquire()
            users[thread_data.receiver].append((thread_data.username, data))
            lock.release()
            thread_data.composing = False
            
        ### COMPOSE LOGIC
        elif data.startswith('COMPOSE '):
            thread_data.receiver = data[len('COMPOSE '):].strip()
            if ' ' in thread_data.receiver:
                conn.close()
                break
            lock.acquire()
            try:
                if thread_data.receiver not in users:
                    users[thread_data.receiver] = []
                conn.send('MESSAGE SENT\n'.encode())
            except Exception as e:
                conn.send('MESSAGE FAILED\n'.encode())
            finally:
                lock.release()
                thread_data.composing = True    
        
        ### READ LOGIC
        elif data.startswith('READ\n'):
            lock.acquire()
            if users[thread_data.username]:
                sender, message = users[thread_data.username].pop(0)
                conn.send((sender + " " + message + "\n").encode())
            else:
                conn.send('READ ERROR\n'.encode())
            lock.release()
        
        ### EXIT LOGIC
        elif data == 'EXIT':
            conn.close()
            break


        ## BREAK CONNECTION IN ANY OTHER WAY
        elif thread_data.logged_in and not thread_data.composing and not data.startswith('LOGIN ') and not data.startswith('READ\n') and not data.startswith('COMPOSE '):
            if not thread_data.composing:
                conn.close()
                break
            
            
def server_program(port):
    host = socket.gethostname()
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen(5)

    users = {}
    lock = Lock()

    while True:
        conn, addr = server_socket.accept()
        client_thread = Thread(target=handle_client, args=(conn, addr, users, lock))
        client_thread.start()

if __name__ == '__main__':
    
     # Exit the program if no port number is provided
    if len(sys.argv) < 2:
        print("Usage: python script.py <port>")
        sys.exit(1) 
        
    # Convert the port argument from string to integer
    port = int(sys.argv[1]) 
    # Run server
    server_program(port)
