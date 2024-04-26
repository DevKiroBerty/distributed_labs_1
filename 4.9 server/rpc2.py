import channel, pickle
from constRPC import * #-
import multiprocessing
from time import sleep
     
channelID = 1
serverID  = 10
clientID  = 20    
                                                #-
class DBList:                                   #-
  def __init__(self, basicList):                #-
    self.value = list(basicList)                #-
                                                #-
  def append(self, data):                       #-
    self.value.extend(data) #-
    return self                                 #-


class Server:
  def __init__(self, channelID, serverID):                           #-
    self.channel = channel.Channel(channelID) #-
    self.channel.join(serverID)     #-
    self.server  = serverID #-
#-
  def append(self, data, dbList):     #-         
    assert isinstance(dbList, DBList) #- Make sure we have a list
    return dbList.append(data)        #-
                                      #-
  def run(self):
    while True:
      msgreq = self.channel.recvFromAny() # wait for any request
      client = msgreq[0]                  # see who is the caller 
      msgrpc = pickle.loads(msgreq[1])    # unwrap the call
      if APPEND == msgrpc[0]:             # check what is being requested
        result = self.append(msgrpc[1], msgrpc[2]) # do local call 
        msgres = pickle.dumps(result)              # wrap the result
        self.channel.sendTo(client,msgres)         # send response
      elif STOP == msgrpc[0]: #- Time to stop
        return #-
      else:                                        #-
        pass # unsupported request, simply ignore  #-
    
def server(channelID, serverID):
	s = Server(channelID, serverID) 
	sleep(2)  # Simple wait so that client can get into the system
	s.run()   # In particular, get the server into a loop

if __name__ == "__main__":
	chan = channel.Channel(channelID, True)
	s = multiprocessing.Process(target=server,args=(channelID,serverID,))
	
	s.start()
	s.join()