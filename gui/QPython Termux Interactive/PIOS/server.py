from traceback import format_exc
import socket,time,os,sys
def Now():
    t=time.localtime()
    return "%04d-%02d-%02d,%02d:%02d:%02d"%(t.tm_year,t.tm_mon,t.tm_mday,t.tm_hour,t.tm_min,t.tm_sec)
def Accept():
    global Conn
    Conn,addr = Socket.accept()
    print(Now(),'对接地址',addr)
def Send(Result,Error):
    Data=bytes(repr(Result)+'\x00'+Error,'utf-8')
    if len(Data)%2==0:
        Data+=b'\x01'
    else:
        Data+=b'\x02\x02'
    Conn.sendall(Data)
def Recv():
    a=bytearray()
    while True:
        b=Conn.recv(1024)
        a.extend(b)
        if len(b)<1024:
            break
    if len(b)>0:
        a=a[:-b[-1]]
    return str(a,'utf-8')
class Out:
    result=[]
    error=''
    write=result.append
    def flush():
        pass
def RunEval(code):
    try:
        Out.result=eval(code,Env,Env)
    except:
        Out.error=format_exc()
        Out.result=''
def RunExec(code):
    sys.stdout=Out
    try:
        exec(code,Env,Env)
    except:
        Out.error=format_exc()
    Out.result=''.join(Out.result)
    sys.stdout=fileOut
def RunShell(code):
    code='os.system('+repr(code)+')'
    print()
    return RunEval(code)
def RunSl4a(code):
    code='droid.'+code
    try:
        data=eval(code,Env,Env)
        Out.result=data.result
        Out.error=data.error
        if Out.error==None:
            Out.error=''
    except:
        Out.error=format_exc()
        Out.result=''
def RunError(text):
    Out.error=Out.result=""
def Run(cmd):
    mode,code=cmd.split(':',1)
    Glb['Run'+mode](code)
    data=Out.result,Out.error
    Out.result=[]
    Out.write=Out.result.append
    Out.error=''
    return data
Glb=globals()
def Once():
    data=Recv()
    print(Now(),'传入指令',data)
    try:
        data=Run(data)
    except:
        print(Now(),'连接中断')
        exit()
    print(Now(),'返回结果',data)
    Send(*data)
def RunExit(text=""):   
    sys.stdout=fileOut
    Text=str(Text)
    Conn.close()
    Socket.shutdown(2)
    print(Now(),'对接结束')
    exit()
Env={'os':os}
def Start(port=12000):#对接流程
    global Socket
    print(Now(),'对接开始 端口号:%s'%port)
    Socket=socket.socket()
    host=socket.gethostname()
    try:
        Socket.bind((host,port))
        print(Now(),'已连接上',host,port)
    except:
        print(Now(),'连接失败，对接结束',format_exc(),host,port)
        exit()
    Socket.listen(5)
    Socket.settimeout(120)
    Accept()
    while True:
        Once()
projectPath=__file__[:__file__.rfind('/')]
os.chdir(projectPath)
try:
    port=int(sys.argv[1])
except:
    port=12000
if os.environ['HOME'].find('qpython')!=-1:
    from androidhelper import Android as droid
    droid=droid()
    Env['droid']=droid
fileOut=sys.__stdout__
print('日志文件:',fileOut)
sys.stdout=fileOut
if __name__=='__main__':
    Start(port)