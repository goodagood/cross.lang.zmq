


#
#   Hello World client in Python
#   Connects REQ socket to tcp://localhost:5555
#   Sends "Hello" to server, expects "World" back
#

import sys
import json

import zmq


def send_bstring(bstr):
    context = zmq.Context()

    #  Socket to talk to server
    print("Connecting to tcp://127.0.0.1:5555 server…")
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://127.0.0.1:5555")

    #request = bstr.decode()
    #print("Sending request %s …" % request)
    socket.send(bstr)

    #  Get the reply.
    message = socket.recv()
    print("message  %s " % (message))
    #print("request, message %s [ %s ]" % (request, message))



    print("closing zmq binding, start to close socket and destroy context")
    socket.close()
    context.destroy()

    return message


def send(jsonData):
    bstr = json.dumps(jsonData).encode('utf-8')
    send_bstring(bstr)



class ReqClient:
    def __init__(self, addr='tcp://127.0.0.1:5555'):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REQ)
        self.socket.connect(addr)


    def json_to_bstring(self, j):
        return json.dumps(j).encode('utf-8')

    def bstring_to_json(self, bstring):
        s = bstring.decode('utf-8')
        j = json.loads(s)
        return j


    def get_output(self, input_json):
        bstr = self.json_to_bstring(input_json)
        self.socket.send(bstr)


        #  Get the reply.
        message = self.socket.recv()
        j = self.bstring_to_json(message)

        return j


    def close(self):
        self.socket.close()
        self.context.destroy()


def output_with_input(input_json):
    rc = ReqClient()
    output = rc.get_output(input_json)
    rc.close()
    return output


if __name__ == "__main__":
    j = {

            'ask4': 'foo',
            'ask': 'some_thing',
            'more': 'less'
            }
    ja = {
            'ask4': 'foo_a'
            }

    #bstr = json.dumps(j).encode('utf-8')
    #send_bstring(bstr)

    #rc = ReqClient()
    #rc.get_output(j)
    pass
