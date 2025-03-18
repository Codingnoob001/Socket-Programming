"""
AUTHORS: Victor P Akolo and Cimone L Williams
PA1:
The main objective of this program and code is to familiarize myself with TCP socket Programming
and also get insight into HTTP protocol
"""""
# making necessary import
import socket

# i define the program constants here, for this project, I am using  a host of 127.0.0.1 and port of 6789
HOST = '127.0.0.1'
PORT = 6789
FILE_REQUEST = "HelloWorld.html"
YOUR_REQ = "Your request is "

"""
In our function below, we create a TCP client that connects to our server, sends a GET request, receives the response, and then prints out the output
first, we create a socket to communicate with the server and try to establish a connection with our server on our port and host
we then format the GET request for the requested file  and send it
we receive the response from our server, decode it, print it out in our terminal, and close our connection
"""


def send_request():
    print("Starting TCP client...")
    try:
        # Create socket
        print(f"Creating socket...")
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect to server
        print(f"Connecting to server at {HOST}:{PORT}...")
        client_socket.connect((HOST, PORT))
        print("Connection established successfully")

        # Format and send request
        request = f"GET /{FILE_REQUEST} HTTP/1.1\r\nHost: {HOST}\r\n\r\n"
        print(f"{YOUR_REQ}{request}")
        print("Sending request to server...")
        client_socket.sendall(request.encode())
        print("Request sent successfully")

        # Receive response
        print("Waiting for server response...")
        response = client_socket.recv(4096).decode()
        print("Response received")

        # Display response
        print("Server Response:\n", response)

        # Close connection
        print("Closing connection...")
        client_socket.close()
        print("Connection closed")

    except ConnectionRefusedError:
        print(f"ERROR: Connection refused. Is the server running at {HOST}:{PORT}?")
    except socket.error as e:
        print(f"ERROR: Socket error occurred: {e}")
    except Exception as e:
        print(f"ERROR: An unexpected error occurred: {e}")


if __name__ == "__main__":
    send_request()