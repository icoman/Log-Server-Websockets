"""
    Thread module for tcpip connections
"""

import socket
import sys
from datetime import datetime, timedelta
import thread,traceback,time

DEBUG = False



def thread_run_connex(conn, addr, parent, function, timeout):
    """ This function run in a new thread when client connect """
    parent.num_threads+=1
    conn.settimeout(timeout)    #timeout in seconds
    ip = addr[0]
    if DEBUG:
        now = datetime.now().strftime("%d-%b-%Y %H:%M")
        print "{0} start ip={1}".format(now, ip)
    while True:
        try:
            try: data = conn.recv(1024)
            except socket.timeout,e:
                if DEBUG:
                    print "Client timeout."
                break
            if not data:
                if DEBUG:
                    print "No data."
                break
            else:
                if DEBUG:
                    print "Recv:", data
                #call the most important function
                ret = function(data)
                if ret:
                    conn.send(ret)
        except Exception,e:
            if DEBUG:
                print "Error:", e
            break
    conn.close()
    if DEBUG:
        now = datetime.now().strftime("%d-%b-%Y %H:%M")
        print "{0} end  ip={1}".format(now, ip)
    parent.num_threads-=1


class TcpipTaskServer:
    """ This is tcpip daemon """
    
    def __init__(self, HOST, PORT, limit, function, timeout):
        """ Constructor """
        print "Start TcpipTaskServer"
        self.num_threads=0
        start_date = datetime.now()
        while True:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(30) #seconds
            try:
                s.bind((HOST, PORT))
                s.listen(1)
                try:
                    conn, addr = s.accept()
                    #we have a client
                    if self.num_threads >= limit:
                        s="Too many conexions!"
                        conn.send(s) #inform client
                        conn.close() #and close connection
                    else:
                        #deal with client in a new thread
                        thread.start_new_thread (thread_run_connex,
                                    (conn, addr, self, function, timeout) )
                except socket.timeout,e:
                    #if timeout on listen, then restart and start listen again
                    #if DEBUG:
                    #    print "TcpipTaskServer server timeout"
                    s.close()
            except Exception, ex:
                #This should never happend
                if DEBUG:
                    print ex
                break
        if DEBUG:
            #This should never happend
            print "TcpipTaskServer End"


def main():
    """
        Test module
    """
    import os
    def process(data):
        """
            Test function connection client-server.
        """
        print "Recv data:", data
        return "Server ok."
    try:
        HOST = os.environ.get('HOST','localhost')
        PORT = os.environ.get("PORT",7000)
        print "Start TcpipTaskServer: %s:%s." % (HOST, PORT)
        N = 3 #maximum number of clients
        timeout = 30 #seconds
        #start TcpipTaskServer as a thread
        thread.start_new_thread(TcpipTaskServer, (HOST, PORT, N, process, timeout) )
        time.sleep(1)
        while True:
            print "Master Task is running:", time.time()
            time.sleep(3)
    except Exception, e:
        print e
        raw_input("Program ended, press ENTER.")


if __name__ == "__main__":
    main()
