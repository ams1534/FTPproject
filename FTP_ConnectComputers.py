import socket 
import pickle
import optparse                                         # This is used to parse console input 
import string
# import threading                                      # used in server 

#def cd(newDirectory, socket):


def ls(socket):
    cmd = pickle.dumps('LS')
    socket.send(cmd)                                    # sends the requested commandInput in bytes
    data = socket.recv(1024)                            # receives data from command
    bytesRecv = pickle.loads(data)                      # pickle "decodes" the pickeled file dumped by the server                     
    return bytesRecv

def dir(newDirectory, socket):
    cmd = pickle.dumps('DIR')
    socket.send(cmd)                                    # sends the requested file name in bytes
    data = socket.recv(1024)                            # receives data from command
    bytesRecv = pickle.loads(data)                      # pickle "decodes" the pickeled file dumped by the server     
    return bytesRecv

def get(socket):    
    cmd = pickle.dumps('GET')
    socket.send(cmd)                                    # sends the requested file name in bytes
    filename = input("filename?")                       # gets file desired from client
    if filename != 'quit':                              # 'q' is the indication that the client would like to quit and no longer get a file
        filename = pickle.dumps(filename)
        socket.send(filename)                           # sends the requested file name in bytes
        data = socket.recv(1024)                        # accepts anything sent by server         low key limited to 1018 size file       
        data = pickle.loads(data)                       # special decode from the string 
        if data[:6] == 'EXISTS':
            filesize = data[6:]
            message = input("File exists, " + filesize + "Bytes, download? (Y/N)")
            if message == 'Y':                          # do a more specific check to verify that the user is saying yes i.e Y, y, yes, Yes, etc.
                socket.send(pickle.dumps('OK'))           # sends back string response
                f = open('new' + filename, 'wb')        # makes file with the word new infront 
                data = socket.recv(1024)
                totalRecv = len(data)
                f.write(data)
                while totalRecv < int(filesize):
                    data = set.recv(1024)               # continuously looks for data????????????
                    totalRecv += len(data)              # adds the newly received data to the count received
                    f.write(data)
                    print ("{0:.2f}".format((totalRecv/float(filesize))*100+"% Done")) # cute loading message
                print ("Download Complete!") 
        else:
            print ("File does not Exist!")
    elif filename == 'quit':                            # enters into disconnecting sequence
        socket.send('QUIT')
        quit(socket)

def putFile(socket):
    cmd = pickle.dumps('PUT')
    socket.send(cmd)                                    # sends the requested commandInput in bytes
    data = socket.recv(1024)                            # receives data from command
    bytesRecv = pickle.loads(data)                      # pickle "decodes" the pickeled file dumped by the server                     
    return bytesRecv


def multiget(socket):
    cmd = pickle.dumps('MGET')
    socket.send(cmd)                                    # sends the requested commandInput in bytes
    data = socket.recv(1024)                            # receives data from command
    bytesRecv = pickle.loads(data)                      # pickle "decodes" the pickeled file dumped by the server                     
    return bytesRecv

def multiput(socket):
    cmd = pickle.dumps('MPUT')
    socket.send(cmd)                                    # sends the requested commandInput in bytes
    data = socket.recv(1024)                            # receives data from command
    bytesRecv = pickle.loads(data)                      # pickle "decodes" the pickeled file dumped by the server                     
    return bytesRecv

def changeDir(socket):
    cmd = pickle.dumps('CD')
    socket.send(cmd)                                    # sends the requested commandInput in bytes
    data = socket.recv(1024)                            # receives data from command
    bytesRecv = pickle.loads(data)                      # pickle "decodes" the pickeled file dumped by the server                     
    return bytesRecv

def quit(socket):
    socket.close()



def Main():
    host = input("Enter the IP address of your server: ") # older versions of python will have to use raw_input
    #host = "169.254.145.232"                            # Todd's IP address, Personal IP: 10.20.120.61
    port  = 5000                                        # actual port 

    s = socket.socket()                                 # creates the "port" we use to connect

    s.connect((host,port))                              # This connects to the server
    login = str.decode(s.recv(1024))                    # Promted by server imedeately after connection 
    if login == "LOGIN":
        loginName = input("Please enter username: ")    # Prompt to see if account is already created
        if loginName == "anon":
            loginEmail = input("Please enter your e-mail: ")
            loginInfo = [loginName, loginEmail]
        else:
            password = input("Please enter your password: ")
            loginInfo = [loginName, password]
        data = pickle.dumps(loginInfo)
        s.send(data)
                                                        # Prompt user?
    while True:
        commandInput = input(">") 
        
        if commandInput == "ls":
            lis = ls(s)
            print(lis)

        if commandInput == "get":
            get(s)

        if commandInput == "cd":
            changeDir(s)
        
        if commandInput == "dir":
            ls(s)

        if commandInput == "get":
            get(s)

        if commandInput == "put":
            putFile(s)

        if commandInput == "mget":
            multiget(s)
        
        if commandInput == "mput": 
            multiput(s)

        if commandInput == "quit":
            quit(s)
    


if __name__ == '__main__':
    Main()
