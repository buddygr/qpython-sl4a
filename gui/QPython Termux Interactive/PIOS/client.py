import time,socket,os,sys
def Connect(port=12000):
    global Socket
    Socket = socket.socket()
    host = socket.gethostname()
    startTime = time.time()
    while time.time()-startTime<=5:
        try:
            Socket.connect((host, port))
            break
        except:
            pass
    else:
        print('连接到服务端超时')
        exit()
    global isTermux
    isTermux=RemoteEval('os.environ.get("HOME","").find("termux")!=-1')[0] and os.environ.get('HOME','').find('qpython')!=-1
def Recv():
    a=bytearray()
    while True:
        b=Socket.recv(1024)
        a.extend(b)
        if len(b)<1024:
            break
    if len(b)>0:
        a=a[:-b[-1]]
    s=str(a,'utf-8').rsplit('\x00',1)
    try:
        return eval(s[0]),s[1]
        #数据类型解析成功
    except:
        #数据类型解析失败
        return [s[0],s[1]]
def Send(Data):
    Data=bytes(Data,'utf-8')
    if len(Data)%2==0:
        Data+=b'\x01'
    else:
        Data+=b'\x02\x02'
    Socket.sendall(Data)
def RemoteEval(code):
    try:
        Send('Eval:'+code)
    except:
        SendError()
    return Recv()
def RemoteExec(code):
    try:
        Send('Exec:'+code)
    except:
        SendError()
    return Recv()
def RemoteShell(code):
    try:
        Send('Shell:'+code)
    except:
        SendError()
    if isTermux:
        try:
            droid.launch(None,'com.termux',False)
        except:
            pass
    return Recv()
def RemoteSl4a(*args):
    method=args[0]
    params=repr(args[1:])
    code=method+params
    try:
        Send('Sl4a:'+code)
    except:
        SendError()
    return Recv()
def RemoteExit(text=""):
    Send(f'Exit:{text}')
    Socket.shutdown(2)
def SendError(text=""):
    Send(f'Error:{text}')
isTermux=None
if os.environ.get('HOME','').find('qpython')!=-1:
    from androidhelper import Android as droid
    droid=droid()
try:
    port=int(sys.argv[1])
except:
    port=12000
if __name__=='__main__':
    Connect(port)