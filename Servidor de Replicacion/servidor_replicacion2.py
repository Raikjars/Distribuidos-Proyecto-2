import socket
import sys
import json
from random import randint
host = '127.0.0.1' #192.168.1.118 (si se conecta con el server en una maquina virtual)
port = 12034
BUFFERSIZE = 1024

def replicarObjeto(data):
    if data[1]=="COMMIT":
        return "VOTE_COMMIT"
    elif data[1]=="ABORT":
        return "VOTE_ABORT"
    elif data[1]=="AZAR":
        for _ in range(1):
            value = randint(0, 1)
            if(value==1):
                return "VOTE_COMMIT"
            else:
                return "VOTE_ABORT"

def confirmarReplica(data):
    #agrega el nuevo objeto json
    newData = data[1].replace('\'','\"')
    json_object = json.loads(newData)
    with open('Servidor de Replicacion\\bd2.json', 'w') as file:
        json.dump(json_object, file, indent=4, default=str)

def recibirObjeto():
    data = {}
    data['object'] = []
    
    #obtiene la lista de Json
    with open('Servidor de Replicacion\\bd2.json', 'r') as file:
        objectList = json.load(file)
        
        if(objectList!={}):
            for objectData in objectList['object']:
                data['object'].append(objectData) 
    li = ["restauracion exitosa", data]      
    msg = '|'.join([str(item) for item in li]) 
    return msg

print("Servidor de Replicas Encendido")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socket0:
    socket0.bind((host,port))
    while True:
        socket0.listen()

        conn, adr = socket0.accept()
        print(f"Conexion establecida por: {adr}")

        with conn:

            data0 = conn.recv(BUFFERSIZE)
            data = data0.decode("utf-8")
            data = list(data.split("|"))
            
            if data[0]== "VOTE_REQUEST":
                msg = replicarObjeto(data)
            if data[0]== "GLOBAL_COMMIT":
                confirmarReplica(data)
                msg = "Replica Exitosa"
            if data[0]== "RESTAURAR":
                msg = recibirObjeto()
            print(msg)
            conn.send(msg.encode('utf-8'))