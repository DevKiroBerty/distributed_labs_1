
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

class Server:
  def __init__(self, channelID, serverID):  #-
    self.channel = channel.Channel(channelID) #-
    self.channel.join(serverID) #-
    self.server  = serverID #-
#-
  def append(self, data, dbList):              
    assert isinstance(dbList, DBList) #- Make sure we have a list
    return dbList.append(data)

  def run(self):
    while True:
      msgreq = self.channel.recvFromAny() # wait for any request
      client = msgreq[0]                  # see who is the caller 
      msgrpc = msgreq[1]                  # fetch the actual request

      # At this point, msgreq should have the form (operation, data, list) 
      if APPEND == msgrpc[0]:          # check what is being requested
        result = self.append(msgrpc[1], msgrpc[2]) # do local call
        self.channel.sendTo(client,result)         # return response
      elif STOP == msgrpc[0]: #- Time to stop
        return #-
      else:  #-
        pass # unsupported request, simply ignore  #-
    
def server(channelID, serverID):
	s = Server(channelID, serverID) 
	#c = multiprocessing.Process(targeargs=(channelID, clientID, serverID,))
	sleep(2)  # Simple wait so that client can get into the system
	#c.start() # Now start the client
	s.run()   # In particular, get the server into a loop

if __name__ == "__main__":
	chan = channel.Channel(channelID, True)
	s = multiprocessing.Process(target=server,args=(channelID,serverID,))
	
	s.start()
	s.join()