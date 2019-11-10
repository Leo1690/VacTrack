import socket;

import thread
from time import sleep
import time;
import requests;

from flask import Flask, request
from twilio.twiml.messaging_response import Message, MessagingResponse
import time
app = Flask(__name__)

LastSeen=-1;

def check_vacuum():
    global LastSeen
    lastSeen=LastSeen;
    if lastSeen==-1:
        return "Not Found"
    else:
        lp=time.time()-lastSeen;
        return "Last seen in college office "+str(lp/60.0)+" minutes ago"

@app.route('/sms', methods=['POST'])
def sms():
    number = request.form['From']
    message_body = request.form['Body']
    resp = MessagingResponse()
    #print(f'{number}, {message_body}')
    resp_msg = check_vacuum();
    resp.message(resp_msg)
    return str(resp)
   

#It closses the TCP service
#Input:
#    s: TCP socket
#    sc: TCP connection if the device is a server otherwise TCP socket
def close_connection(s):
    try:
        s.shutdown(1);
    except:
        pass;
    try:
        s.close();
    except:
        pass;
    try:
        s.close();
    except:
        pass;

def requestHttp():
    global LastSeen;
    for a in range(0,100):
        etime=(time.time()-LastSeen)/60.0;
        if etime>=0:
            response = requests.get(url = "https://vacuumatjacobs.appspot.com/set-key?avail="+str(round(etime,5)));
        else:
            response = requests.get(url = "https://vacuumatjacobs.appspot.com/set-key?avail=-1");
        sleep(10);

    
def start_server():
    global LastSeen
    s=None;
    sc=None;
    try:
        s = socket.socket();
        s.settimeout(1000);
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1);
        s.bind(('192.168.1.10',7000));
        
        for a in range(0,100):
            s.listen(1);
            sc, address = s.accept();
            LastSeen=time.time();               
            #print (LastSeen)
            print 'found'
        sc.settimeout(1000);
        return s,sc;
    except Exception as e: 
        print(e);
    close_connection(s);

thread.start_new_thread(start_server, ())
thread.start_new_thread(requestHttp, ())
print ('server on')

if __name__ == '__main__':
    app.run()
