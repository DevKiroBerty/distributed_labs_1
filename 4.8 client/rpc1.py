import channel, pickle
from constRPC import * #-
import multiprocessing
from time import sleep
channelID = 1
serverID  = 10
clientID  = 20
class DBList:
  def __init__(self, basicList): #-
    self.value = list(basicList) #-
                                 #-
  def append(self, data):
    self.value.extend(data)
    return self

class Client: 
  def __init__(self, channelID, clientID, serverID):                            #-
    self.channel = channel.Channel(channelID) #-
    self.channel.join(clientID) #-
    self.client  = clientID #-
    self.server  = serverID #-
                                                #-
  def append(self, data, dbList):
    assert isinstance(dbList, DBList)        #-
    msglst = (APPEND, data, dbList)             # message payload
    self.channel.sendTo(self.server, msglst)    # send message to server 
    msgrcv = self.channel.recvFrom(self.server) # wait for an incoming message

    # A call to recvFrom returns a [senderID, message] pair
    return msgrcv[1]                            # pass returned message to caller
#-
  def stop(self): #-
    msglst = (STOP, '', '') #-
    self.channel.sendTo(self.server, msglst) #-
    return #-

def client(channelID, clientID, serverID):
	c	 = Client(channelID, clientID, serverID) # Create client stub
	s1 = DBList((1,2))      # Create a local list
	s2 = c.append('c',s1)        # Pass local list to stub and wait for result
	print("Value s1:", s1.value) # This is what client started with
	print("Value s2:", s2.value) # This is what the server did after call to append
	c.stop()
 
 
client(channelID=channelID,clientID=clientID,serverID=serverID)
 
