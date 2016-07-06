
#
# zmq serve localhost:5555, modified from Hello World server example.
# It accept simple message, which is same as 'hello world' example, 
# The message is decoded and parsed to json (dict), 
# the json is served as input, it must contain attribute of 'ask4',
#  {
#    'ask4': python_module_name, the module contain 'main(input) #=> output'
#    other_attribute_and_information ...
#  }
# 
# so, 'ask4' is a string, which
# is the name of python module (file), it must be valid name of python
# variable and module, so, underscore `(_)` instead of dot `('.')`
# If output can be found, it will be returned in json format:
#  {
#     input:  { the input is here for reference},
#     output: { ... }
#  }
# 
# Of course, the json is json.dumps()ed, and it encode to b'string'
# of python v3,
# then the string is pass to zmq as reply
#
# 2016 0525, 2016 06 30
#

import sys
import time
import json
from pprint import pprint

import zmq


#
Path_of_Workers = './workers'



def cycle_output_for_zmq_input():
    '''
    Works as server, waiting the input, gives output.

    The input is {'ask4': module_name, other parameters ...}
    and reply is {input:, output:}, the input is copied as referrence.

    The module_name will get import-ed, and
    module_name.main(input) #=> should return the output

    '''
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://127.0.0.1:5555")

    while True:
        try:
            # <<< receive
            # 
            message = socket.recv()

            print('message:', message)

            # do the message
            # reply should be a b'string' for zmq.
            reply = calculate(message);


            # >>> send
            socket.send(reply)

        except KeyboardInterrupt:
            print("KeyboardInterrupt, closing zmq binding")
            socket.close()
            context.destroy()
            sys.exit()
        except Exception as e:
            print(e)
            print('-- error, sleep 2 sec before running ...')
            time.sleep(12)


def calculate(msg):
    print('calculate')
    m = parse_msg(msg)
    o = output(m)
    e = encode_reply(m, o)
    return e

    #return b'abc'


def parse_msg(msg):
    if type(msg) is bytes:
        msg = msg.decode(encoding='utf-8')
        pass

    if type(msg) is dict:
        return msg

    if type(msg) is str:
        try:
            j = json.loads(msg)
        except:
            print('load json WRONG, something might be wrong')
            j = {} #?
        return j

    print('the msg is not JSON or str, something might be wrong')
    return msg


import finder

def output(input_json):
    '''
    Find the module to calculate the output, 'ask4' should be the module name.
    '''
    if 'ask4' not in input_json:
        #input_json['error'] = "no ask4 no done anything"
        return {error : "no ask4 no done anything"}

    asked = input_json['ask4'].replace('.', '_')

    try:
        main = finder.find(Path_of_Workers, asked)
        output = main(input_json) or {}
        
        return output

    except (Exception) as e:
        print('except exception:')
        print(e)

        # noop: no operation
        return noop_service(input_json)


def encode_reply(Input, Output):
    reply = {
            'input': Input,
            'output':Output,
            }
    jstring = json.dumps(reply)
    encoded = jstring.encode('utf-8')
    return encoded



#def find_main(path_of_module, modname):
#
#    main = finder.find(path_of_module, modname)
#    return main



def noop_service(info):
    output = {'noop': True}
    return output
    return encode_reply(info, output)



if __name__ == "__main__":
    cycle_output_for_zmq_input()

