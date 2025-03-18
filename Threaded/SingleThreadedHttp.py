"""
AUTHORS: Victor P Akolo and Cimone L Williams
PA1:
The main objective of this program and code is to familiarize myself with TCP socket Programming
and also get insight into HTTP protocol
"""""
#make necessary imports here
import socket
import os

#i define the program constants here, for this project, I am using  a host of 127.0.0.1 and port of 6789
HOST = '127.0.0.1'  # Localhost
PORT = 6789
FILE = ("HelloWorld.html")
HEADER_RESP_200 = "HTTP/1.1 200 OK\nContent-Type: text/html\n\n"
HEADER_RESP_400 = "HTTP/1.1 404 Not Found\nContent-Type: text/html\n\n"
BODY_RESP = "<h1>404 Error: File Not Found</h1>"

"""
The function below is designed to handle requests from a client.
we read the http request from our client and then extract the requested file from the Get request
we check if the requested file is available. if yes --> read the file and respond with 200, if no --> we return a 404 error
we then send the response back to the client and close all connections
"""
def handle_request(client_socket):
    request = client_socket.recv(1024).decode('utf-8')
    print(f"Received request:\n{request}")
    requested_file = extract_requested_file(request)
    response_header, response_body = prepare_response(requested_file)
    send_response(client_socket, response_header, response_body)
    client_socket.close()

def extract_requested_file(request):
    try:
        requested_file = request.split()[1][1:]  # Remove any leading '/'
    except IndexError:
        requested_file = FILE
    return requested_file or FILE

def prepare_response(requested_file):
    if os.path.exists(requested_file):
        with open(requested_file, 'r') as f:
            response_body = f.read()
        response_header = HEADER_RESP_200
    else:
        response_body = BODY_RESP
        response_header = HEADER_RESP_400
    return response_header, response_body

def send_response(client_socket, header, body):
    client_socket.sendall(header.encode('utf-8') + body.encode('utf-8'))
"""
In this start server func, we initialize and start the http server.
first we create a TCP socket and bind the socket to the specified host and port
we then listen for incoming client connections
we then use a while loop to accept and handle requests
"""
def start_server():
    # Initialize the server socket
    server_socket = initialize_server_socket()
    start_listening(server_socket)
    handle_client_connections(server_socket)

def initialize_server_socket():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    return server_socket

def start_listening(server_socket):
    server_socket.listen(5)
    print(f"Server started on http://{HOST}:{PORT}")

def handle_client_connections(server_socket):
    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connection from {addr}")
        handle_request(client_socket)

if __name__ == "__main__":
    start_server()