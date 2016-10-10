import string
import socket
import sys
import datetime, time


class LogClient:
    """
    """
    def __init__(self, host="localhost", port="7000"):
        self.timeout = 30 #seconds
        self.host = host
        self.port = port
    def log(self, message, channel = "Info", color = "#000000"): 
        sok = None
        for res in socket.getaddrinfo(self.host, self.port, socket.AF_UNSPEC, socket.SOCK_STREAM):
            af, socktype, proto, canonname, sa = res
            try:
                sok = socket.socket(af, socktype, proto)
            except socket.error as msg:
                sok = None
                continue
            try:
                sok.connect(sa)
            except socket.error as msg:
                sok.close()
                sok = None
                continue
            break
        if sok is None:
            print 'could not open socket'
        else:
            sok.settimeout(self.timeout)
            sok.send("{}:{}:{}".format(channel,color,message))
            sok.close()


if __name__ == "__main__":
    """
        Test module
    """
    print "Test module"
    try:
        client = LogClient("localhost","7000")
        if len(sys.argv) > 3:
            channel = sys.argv[1]
            color = sys.argv[2]
            NOW = datetime.datetime.now().strftime("%d %b %Y %H:%M.%S")
            message = NOW + " - " + string.join(sys.argv[3:], " ")
            client.log(message, channel, color)
        else:
            #demo
            client.log("Client start.","Debug","#FF0000")
            for i in range(10):
                client.log("Test {}".format(i),"Info","#0000FF")
                time.sleep(1)
            client.log("Client end.","Debug","#FF0000")
    except Exception as ex:
        print "Error:",ex
        raw_input("Press ENTER")

