
import socket
import ipaddress

def run():
    try:
        # Prompt user for server details
        server_ip = str(ipaddress.ip_address(input("Enter Server IP Address: ")))
        server_port = int(input("Enter Server Port: "))
        
        # Establish connection to server
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((server_ip, server_port))
        print("Connection established\n")
    except (ValueError, TypeError) as e:
        print(f"Error: Could not connect to the server. {e}")
        return

    max_bytes = 1024

    while True:
        query = queries()
        client_socket.send(bytearray(str(query), encoding='utf-8'))
        print(f"Message sent: {query}")

        if query == '4':  # Exit condition
            print("Exiting the program.")
            break

        # Receive and display the server's response
        server_response = client_socket.recv(max_bytes)
        print("Server's reply:", server_response.decode())

    client_socket.close()
    print("Connection with the server is now closed")

def queries():
    valid_input = ["1", "2", "3", "4"]
    user_input = None

    while user_input not in valid_input:
        print("Select one of the following queries:\n",
              "1. What is the average moisture inside my kitchen fridge in the past three hours?\n",
              "2. What is the average water consumption per cycle in my smart dishwasher?\n",
              "3. Which device consumed more electricity among my three IoT devices (two refrigerators and a dishwasher)?\n",
              "4. Exit the program.\n")

        user_input = str(input("Select '1', '2', '3', or '4': "))
        if user_input not in valid_input:
            print("Invalid input. Please try again.\n")

    return user_input

if __name__ == "__main__":
    run()