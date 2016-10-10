import logclient
import time


client = logclient.LogClient("localhost","7000")
client.log("Client2 start.","Info","#FF0000")
for i in range(3):
    message = "Client2 i={}".format(i)
    client.log(message, "Info","#000000")
    time.sleep(1)
client.log("Client2 end.","Info","#FF0000")
