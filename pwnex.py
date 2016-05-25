import os,signal
import sys

def Exit(sig,frame):
    sys.exit(1)

def repwn(retry=1,timeout=0):
    def _repwn(func):
        def __repwn(*args, **kwargs):
            for i in range(retry):
                pid = os.fork()
                if pid > 0:
                    childPid,exitId = os.wait()
                    if childPid == pid and exitId == 0:
                        break
                else:
                    if timeout != 0:
                        signal.signal(signal.SIGALRM,Exit)
                        signal.alarm(timeout)
                    func(*args, **kwargs)
                    sys.exit(0)
        return  __repwn
    return _repwn

def padding(size, bList='\n\r\x00'):
    pad = ''
    for i in range(size):
        ch = os.urandom(1)
        if ch not in bList:
            pad += ch
    return pad