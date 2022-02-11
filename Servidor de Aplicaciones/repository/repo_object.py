from datetime import datetime
from logging import StreamHandler
from typing import List, Optional
import socket

from sqlalchemy.orm import Session

from database import engine
from model.object_model import ObjectInJson
import json

# nuestra base de datos va a ser un list
blogdb = []

class ObjectRepo:

    def create(self, new_object: ObjectInJson) -> ObjectInJson:
        object_dict = {**new_object.dict()}
        aux = 1
        data = {}
        data['object'] = []
        
        #obtiene la lista de Json
        with open('bd.json', 'r') as file:
            objectList = json.load(file)
            
            if(objectList!={}):
                for objectData in objectList['object']:
                    data['object'].append(objectData)
                    aux = objectData['id']
                object_dict["id"] = aux + 1
            else:
                object_dict["id"] = aux
            data['object'].append(object_dict)

        #agrega el nuevo objeto json    
        with open('bd.json', 'w') as file:
            json.dump(data, file, indent=4, default=str)
        
        objectBd = ObjectInJson(**object_dict)

        return objectBd

    def delete(self, *, id=int) -> ObjectInJson:
        data = {}
        data['object'] = []
        
        #obtiene la lista de Json
        with open('bd.json', 'r') as file:
            objectList = json.load(file)
            
            if(objectList!={}):
                for objectData in objectList['object']:
                    if(id!=objectData['id']):
                        data['object'].append(objectData)
                    
        if(data!=[]):
            #agrega el nuevo objeto json    
            with open('bd.json', 'w') as file:
                json.dump(data, file, indent=4, default=str)
        

        return id
    
    def get_all(self) -> List[ObjectInJson]:
        data = {}
        data['object'] = []
        
        #obtiene la lista de Json
        with open('bd.json', 'r') as file:
            objectList = json.load(file)
            
            if(objectList!={}):
                for objectData in objectList['object']:
                    data['object'].append(objectData) 
        return data['object']

    def get_by_id(self, *, id:int) -> List[ObjectInJson]:
        data = {}
        data['object'] = []
        
        #obtiene la lista de Json
        with open('bd.json', 'r') as file:
            objectList = json.load(file)
            
            if(objectList!={}):
                for objectData in objectList['object']:
                    if(id==objectData['id']):
                        data['object'].append(objectData)
        return data['object']
    
    def replicate(self, new_object: ObjectInJson) -> ObjectInJson:
        object_dict = {**new_object.dict()}
        aux = 1
        data = {}
        data['object'] = []
        
        #obtiene la lista de Json
        with open('bd.json', 'r') as file:
            objectList = json.load(file)
            
            if(objectList!={}):
                for objectData in objectList['object']:
                    data['object'].append(objectData)
                    aux = objectData['id']
                object_dict["id"] = aux + 1
            else:
                object_dict["id"] = aux
            data['object'].append(object_dict)

        #agrega el nuevo objeto json    
        with open('bd.json', 'w') as file:
            json.dump(data, file, indent=4, default=str)

        data = {}
        data['object'] = []
         #obtiene la lista de Json
        with open('bd.json', 'r') as file:
            objectList = json.load(file)
            
            if(objectList!={}):
                for objectData in objectList['object']:
                    data['object'].append(objectData)
        
        li = ["replicar", object_dict["Action"], data]
        objectBd = ObjectInJson(**object_dict)

        host2 = '192.168.1.100'
        port2 = 12036
        with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as socket2:
            socket2.connect((host2,port2)) #probando conexion de forma local como un socket2
            
            li = '|'.join([str(item) for item in li])   
            socket2.sendall(li.encode('utf-8')) 
            
            data2 = socket2.recv(1024)
            print(data2.decode("utf-8"))
        return objectBd

    def restore(self) -> List[ObjectInJson]:
        li = ["restaurar"]

        host2 = '192.168.1.100'
        port2 = 12036
        with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as socket2:
            socket2.connect((host2,port2)) #probando conexion de forma local como un socket2
            
            li = '|'.join([str(item) for item in li])   
            
            socket2.sendall(li.encode('utf-8')) 

            data2 = socket2.recv(1024)
            data = data2.decode("utf-8")
            data = list(data.split("|"))
            newData = data[1].replace('\'','\"')
            json_object = json.loads(newData)
            

            #agrega el nuevo objeto json    
            with open('bd.json', 'w') as file:
                json.dump(json_object, file, indent=4, default=str)

        return json_object['object']
    