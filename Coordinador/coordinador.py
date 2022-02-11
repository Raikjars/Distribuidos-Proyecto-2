import socket
import sys
import json

host0 = '192.168.1.100'
port0 = 12036
BUFFERSIZE = 1024

def conexion1(msg):
    host1 = '192.168.1.140'
    port1 = 12033
    with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as socket1:
        socket1.connect((host1,port1))
        
        data = '|'.join([str(item) for item in msg])      
        socket1.sendall(data.encode('utf-8')) 
        
        #data = '|'.join([str(item) for item in aux])    
        #li = list(string.split("|"))

        data1 = socket1.recv(BUFFERSIZE)
        return data1.decode("utf-8")

def conexion2(msg):
    host2 = '192.168.1.109'
    port2 = 12034
    with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as socket2:
        socket2.connect((host2,port2)) #probando conexion de forma local como un socket2

        data = '|'.join([str(item) for item in msg])      
        socket2.sendall(data.encode('utf-8')) 
        
        #data = '|'.join([str(item) for item in aux])    
        #li = list(string.split("|"))

        data2 = socket2.recv(BUFFERSIZE)
        return data2.decode("utf-8")


def replicarObjectos(data):
    msg = ["VOTE_REQUEST", data[1]]
    response1 = conexion1(msg)
    response2 = conexion2(msg)
    print("voto servidor 1: ", response1, " voto servidor 2: ", response2)
    if response1=="VOTE_COMMIT" and response2=="VOTE_COMMIT":
        msg = ["GLOBAL_COMMIT", data[2]]
        conexion1(msg)
        conexion2(msg)
        return "Replicacion Exitosa"
    else:
        return "Replicacion Fallida"

def restaurarObjetos():
    msg = ["RESTAURAR"]
    return conexion2(msg)

with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as socket0:
    socket0.bind((host0,port0))
    print("Servidor Coordinador Encendido..") 
    while True:
        socket0.listen()
        
        client, adr = socket0.accept()

        print(f"Conexion establecida - {adr}")

        with client:
            data_0 = client.recv(BUFFERSIZE)
            data = data_0.decode("utf-8")
            data = list(data.split("|"))
            
            if data[0]=='replicar':
                msg0 = replicarObjectos(data) #llamando al Servidor_Replicacion
            
            elif data[0]=='restaurar': 
                msg0 = restaurarObjetos()

            client.sendall(msg0.encode('utf-8'))