import socket
import sys

def connect_to_server(host, port):
    print(host, port)
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # instantiate
    client_socket.connect((host, port))  # connect to the server
    return client_socket

def is_ascii(s):
    try:
        s.encode('ascii')
        return True
    except UnicodeEncodeError:
        return False

def login_logic(client_socket):
    # Login logic
    while True:
        username = input("Enter the username (no spaces): ")
        if ' ' in username:
            print(f"Invalide username, {username} contains space(s)")
        elif not is_ascii(username):
            print(f'Invalid username, {username} contains non-ascii characteser(s)')
        elif username == 'EXIT':
            print('You are exiting the program. Goodbye for.')
            client_socket.close()
        else:
            client_socket.send(('LOGIN ' + username).encode()) 
            break
    data = client_socket.recv(1024).decode()  # receive response
    print(f'Number of unread messages: {data}')

def read_logic(answer):
    # Read messages logic
    if answer == 'READ ERROR':
        print('No new messages')
    else:
        name, message = answer.split(' ', 1)
        print(f'{name} left the following message for you: "{message}"')
    
def compose_logic(client_socket, answer):
    # Composite messages logic
    recipient = input('Enter the recipient name (no spaces): ')
    if ' ' in recipient:
        print(f'Incorrect recipient name, {recipient} contains space(s).')
        return
    elif not is_ascii(recipient):
        print(f'Incorrect recipient name, {recipient}, it contains non-ascii character(s).')
        return
    else:
        message = input('Enter the message: ')
        if not is_ascii(message):
            print(f'Incorrect message, {message}, it contains non-ascii character(s).')
            return
        else:
            client_socket.send(('COMPOSE ' + recipient).encode())
            client_socket.send(message.encode())
            answer = client_socket.recv(1024).decode()
        print(answer)
        if answer == 'MESSAGE SENT':
            print(f'Messaged delivered succesfully to {recipient}')
        else:
            print(f'An error occurred the message was not delived to {recipient}')
            

def communication_with_server(client_socket):
   # Main logic of the client
    while True:
        option = input("Select one of the following: COMPOSE, READ, EXIT: ")
        if option == 'COMPOSE':
            compose_logic(client_socket, option)
        elif option == 'READ':
            client_socket.send(option.encode())
            answer = client_socket.recv(1024).decode()
            read_logic(answer)
        elif option == 'EXIT':
                break
        else:
             option = input("""Incorrect input. Please select one of the following: COMPOSE, READ, EXIT: """)
        
def  client_program(host, port):
    
    # Connect to server
    client_socket = connect_to_server(host, port)

    # Login logic
    login_logic(client_socket)
    
    # Interactive part
    communication_with_server(client_socket)
    
    # close the connection
    client_socket.close() 
   

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python script.py <hostname> <port>")
        sys.exit(1) 

    host = sys.argv[1]  #
    port = int(sys.argv[2]) 
    client_program(host, port)