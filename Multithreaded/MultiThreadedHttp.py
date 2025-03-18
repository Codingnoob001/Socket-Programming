"""
AUTHORS: Victor P Akolo and Cimone L Williams
PA1:
The main objective of this program and code is to familiarize myself with TCP socket Programming
and also get insight into HTTP protocol
"""""
# make necessary imports here
import socket
import threading
import os

# i define the program constants here, for this project.
HOST = '127.0.0.1'
PORT = 6789
FILE = "HelloWold.html"
HEADER_RESP_200 = "HTTP/1.1 200 OK\nContent-Type: text/html\n\n"
HEADER_RESP_400 = "HTTP/1.1 404 Not Found\nContent-Type: text/html\n\n"
BODY_RESP = "<h1>404 Error: File Not Found</h1>"

"""
The function below is designed to handle requests from a client. It is identical to SingleThreadedHttp.py but with few adjustments
we read the http request from our client and then extract the requested file from the Get request
we check if the requested file is available. if yes --> read the file and respond with 200, if no --> we return a 404 error
we then send the response back to the client and close all connections
"""


def handle_request(client_socket):
    print(f"[HANDLER] Starting to handle request from client...")
    # Receive and decode the request from the client
    request = client_socket.recv(1024).decode('utf-8')
    print(f"[HANDLER] Received request:\n{request}")

    # Extract the requested file path from the request
    requested_file = extract_requested_file(request)
    print(f"[HANDLER] Extracted requested file: '{requested_file}'")

    # Determine the appropriate response based on the file's existence
    response_header, response_body = prepare_response(requested_file)

    # Send the HTTP response back to the client
    send_response(client_socket, response_header, response_body)
    print(f"[HANDLER] Response sent to client")

    # Close the client socket
    client_socket.close()
    print(f"[HANDLER] Client connection closed")


def extract_requested_file(request):
    print("[EXTRACT] Extracting file from request...")
    try:
        requested_file = request.split()[1][1:]  # Remove the leading '/'
        print(f"[EXTRACT] Successfully extracted: '{requested_file}'")
    except IndexError:
        requested_file = FILE  # Use default file if path is not specified
        print(f"[EXTRACT] Error extracting path, using default file: '{requested_file}'")
    return requested_file or FILE  # Fallback to default file if empty


def prepare_response(requested_file):
    print(f"[RESPONSE] Preparing response for file: '{requested_file}'")
    if os.path.exists(requested_file):
        print(f"[RESPONSE] File exists, reading contents...")
        with open(requested_file, 'r') as f:
            response_body = f.read()
        response_header = HEADER_RESP_200
        print(f"[RESPONSE] Sending 200 OK response")
    else:
        print(f"[RESPONSE] File not found, preparing 404 response")
        response_body = BODY_RESP
        response_header = HEADER_RESP_400
    return response_header, response_body


def send_response(client_socket, header, body):
    print(f"[SEND] Sending response to client")
    response = header.encode('utf-8') + body.encode('utf-8')
    client_socket.sendall(response)
    print(f"[SEND] Response sent ({len(response)} bytes)")


"""
In this start server func, we initialize and start the http server.
first we create a TCP socket and bind the socket to the specified host and port
we then listen for incoming client connections
we then use a while loop to accept and handle requests
"""


def start_server():
    print("[SERVER] Starting server initialization...")
    # Initialize the server socket
    server_socket = initialize_server_socket()

    # Start listening for incoming connections
    start_listening(server_socket)

    # Continuously accept and handle client connections
    handle_client_connections(server_socket)


def initialize_server_socket():
    print(f"[INIT] Creating server socket...")
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    print(f"[INIT] Socket bound to {HOST}:{PORT}")
    return server_socket


def start_listening(server_socket):
    server_socket.listen(10)
    print(f"[LISTEN] Multithreaded Server started on http://{HOST}:{PORT}")
    print(f"[LISTEN] Server is now listening for connections (max 10 in queue)")


def handle_client_connections(server_socket):
    print("[ACCEPT] Entering connection acceptance loop")
    while True:
        print("[ACCEPT] Waiting for client connection...")
        client_socket, addr = server_socket.accept()
        print(f"[ACCEPT] New connection from {addr}")
        start_client_thread(client_socket)


def start_client_thread(client_socket):
    print("[THREAD] Starting new client thread")
    client_thread = threading.Thread(target=handle_request, args=(client_socket,))
    client_thread.daemon = True  # Makes thread exit when main thread exits
    client_thread.start()
    print(f"[THREAD] Thread started: {client_thread.name}")


if __name__ == "__main__":
    print("[MAIN] Script execution started")
    start_server()