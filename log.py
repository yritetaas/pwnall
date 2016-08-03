import json
import os
from time import sleep

path = '/tmp/logging/'
logFile = '/tmp/alog'
recv = 1
send = 0
while True:
    for f in os.listdir(path):
        lo = {}
        fp = open(path+f)
        lines = fp.readlines()
        lo['token'] = 'no'
        lo['host'] = '127.0.0.1'
        lo['ip'] = '127.0.0.1'
        lo['dport'] = 0
        lo['sport'] = 0
        lo['data'] = []

        time = 0
        flag = None
        data = ''
        for i in lines:
            if i[:14] == 'input:1*a1?=+:':
                if time != 0:
                    lo['data'].append((time,flag,data[:-1]))
                flag = recv
                time = int(i[14:])
                data = ''
                continue
            elif i[:15] == 'output:1*a1?=+:':
                if time != 0:
                    lo['data'].append((time, flag, data[:-1]))
                flag = send
                time = int(i[15:])
                data = ''
                continue
            data += i
        if time != 0:
            lo['data'].append((time, flag, data))
        js =  json.dumps(lo)
        fp.close()
        os.unlink(path+f)
        fp = open(logFile,'a')
        fp.write(js+'\n')
    sleep(20)
