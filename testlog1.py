import logclient
import time

client = logclient.LogClient("localhost","7000")
client.log("Client1 start.","Debug","#FF0000")
time.sleep(1)
client.log("Client1 end.","Debug","#FF0000")
