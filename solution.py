from datastore import Datastore

#Creating object of class Datastore(File path is optional)
dt=Datastore()

dt.create('a',5)
dt.create('b',10)
dt.create('c',2,3600)

dt.read('a')
#5

dt.read('c')
#2

dt.delete('a')
#key is successfully deleted

dt.read('a')
#error: given key does not exist in database. Please enter a valid key