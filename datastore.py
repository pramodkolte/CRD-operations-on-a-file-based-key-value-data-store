import os
import threading
import time
import json

class Datastore:   
    def __init__(self,path=os.path.abspath(os.getcwd())):
        if os.path.exists(path):
            self.filepath = os.path.join(path, 'datastore.json')
            open(self.filepath, "a")
            #datastore.json file will be created at specified path
        else:
            raise RuntimeError("Invalid path")

    #for reading current data from file
    def getJsonData(self):
        with open(self.filepath, "r") as outfile:
            return json.load(outfile)

    #for writing updated data to file
    def setJsonData(self,data):
        with open(self.filepath, "w") as outfile: 
            json.dump(data, outfile)

    #for create operation 
    #use syntax "create(key_name,value,timeout_value)" timeout is optional you can continue by passing two arguments without timeout
    def create(self,key,value,timeout=0):
        data=self.getJsonData()
        if key in data:
            print("error: this key already exists") #error message1
        else:
            if(key.isalpha()):
                if len(data)<(1024*1020*1024) and value<=(16*1024*1024): #constraints for file size less than 1GB and Jasonobject value less than 16KB 
                    if timeout==0:
                        l=[value,timeout]
                    else:
                        l=[value,time.time()+timeout]
                    if len(key)<=32: #constraints for input key_name capped at 32chars
                        data[key]=l
                        self.setJsonData(data)
                        print("key is successfully inserted")
                else:
                    print("error: Memory limit exceeded!! ")#error message2
            else:
                print("error: Invalind key_name!! key_name must contain only alphabets and no special characters or numbers")#error message3

    #for read operation
    #use syntax "read(key_name)"               
    def read(self,key):
        data=self.getJsonData()
        if key not in data:
            print("error: given key does not exist in database. Please enter a valid key") #error message4
        else:
            b=data[key]
            if b[1]!=0:
                if time.time()<b[1]: #comparing the present time with expiry time
                    stri=str(key)+":"+str(b[0]) #to return the value in the format of JasonObject i.e.,"key_name:value"
                    return stri
                else:
                    print("error: time-to-live of",key,"has expired") #error message5
            else:
                stri=str(key)+":"+str(b[0])
                return stri

    #for delete operation
    #use syntax "delete(key_name)"
    def delete(self,key):
        data=self.getJsonData()
        if key not in data:
            print("error: given key does not exist in database. Please enter a valid key") #error message4
        else:
            b=data[key]
            if b[1]!=0:
                if time.time()<b[1]: #comparing the current time with expiry time
                    del data[key]
                    self.setJsonData(data)
                    print("key is successfully deleted")
                else:
                    print("error: time-to-live of",key,"has expired") #error message5
            else:
                del data[key]
                self.setJsonData(data)
                print("key is successfully deleted")