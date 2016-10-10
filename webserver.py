"""
    Webserver with bottle
    and Logserver with class TcpipTaskServer started in a thread
    
    A test solution which works like MQTT pub/sub.
    On webserver there are two python dictionary with log_channel as key:
    d_logs - keep last log message
    d_connex - keep a list with clients connected by websocket

"""

import os, sys, string
import time, thread, socket
from datetime import datetime
import tcpipconns

from gevent.pywsgi import WSGIServer
from geventwebsocket import WebSocketError
from geventwebsocket.handler import WebSocketHandler

import bottle
from bottle import request, Bottle, abort, view, static_file

DEBUG = True



current_dir = os.path.dirname(__file__)
template_folder = os.path.join(current_dir,'templates')
static_folder = os.path.join(current_dir,'static')
bottle.TEMPLATE_PATH.insert(0,template_folder)

app = Bottle()


d_logs = {} #py dict in format channel:last_message_for_that_channel
d_connex = {} #py dict in format channel:[list of websok-clients ]
lock = thread.allocate_lock()




@app.route('/static/<path:path>')
def webfunc(path):
    return static_file(path,root=static_folder)

@app.route('/')
@view('index')
def webfunc():
    title = "Logserver channels."
    channels = d_logs.keys()
    return dict(title=title, channels=channels)

@app.route('/log/<chan>')
@view('logwindow')
def webfunc(chan):
    title = "Logs for: "+chan
    return dict(title=title, chan=chan)

@app.route('/websocket/<chan>')
def handle_websocket(chan):
    wsock = request.environ.get('wsgi.websocket')
    if not wsock:
        abort(400, 'Expected WebSocket request.')
    if DEBUG:
        print "Start websok, channel=", chan
    with lock:
        L = d_connex.get(chan, [])
        L.append(wsock) #add websok-client to list
        d_connex[chan] = L
        logmsg = d_logs.get(chan, '')
    wsock.send(logmsg) #send last log on client connect
    while True:
        try:
            message = wsock.receive()
            #this feature is not used
            wsock.send("<br>Your message was: %r" % message)
        except WebSocketError:
            break
    #if network error or html browser window is closed
    if DEBUG:
        print "End websok, channel=", chan



def process(data):
    """
        This is the most important function.
        This function is called when each log-client send data.
        It update d_logs and d_connex, then inform websok-clients about change.
    """
    ret = "ok" #response to client
    try:
        L = data.split(":")
        channel = L[0]
        color = L[1]
        received_message = string.join(L[2:],":")
        if color:
            log_message = '\n<br><font color="{}">{}</font>'.format(color, received_message)
        else:
            log_message = '\n<br>{}'.format(received_message)
        with lock:
            #update d_logs
            #here a storage of logs can be implemented
            #but right now just store last message
            d_logs[channel] = log_message

            #update d_connex and inform clients
            client_list = []
            for ws in d_connex.get(channel, []):
                for i in range(3):
                    try:
                        #send the log_message to subscribed client
                        ws.send(log_message)
                        #if success, keep client in list
                        client_list.append(ws)
                        break
                    except Exception, ex:
                        if DEBUG:
                            print "Channel",channel,"try",i,"failed."
                        #socket is dead
                        #if network error or html browser window is closed
                        #print ex
                        pass
            d_connex[channel] = client_list #update client list
    except Exception, ex:
        ret = str(ex)
    return ret


def main():
    HOST = os.environ.get('HOST','localhost')
    WEBPORT = os.environ.get('WEBPORT',8080)
    LOGPORT = os.environ.get("LOGPORT",7000)
    print "Start Web Server: %s:%s." % (HOST,WEBPORT)
    print "Start Log Server: %s:%s." % (HOST,LOGPORT)
    #force display of two channels
    d_logs['Info'] = ''
    d_logs['Debug'] = ''
    
    N = 3 #how many log-clients connected at once
    timeout = 30 #seconds
    #thread
    thread.start_new_thread(tcpipconns.TcpipTaskServer, (HOST, LOGPORT, N, process, timeout) )
    #webserver cu websockets
    server = WSGIServer((HOST, WEBPORT), app,handler_class=WebSocketHandler)
    server.serve_forever()

if __name__ == "__main__":
    try:
        main()
    except Exception, e:
        print e



