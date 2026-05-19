#标准输出
_c=[]
write=lambda a:_c.append(str(a))
def flush():pass
def print(*a):
    b=[''.join(_c)]
    _c.clear()
    for i in a:
        b.append(str(i))
        b.append(' ')
    b.append('\n')
    Output(''.join(b))
Output=lambda *a:f('Output')(*a)
#标准输入/0~1提示输入框
input=lambda *a:f('LongText',z='input')(*a)
def readline(n=-1):
    Rst=input('请输入内容：')
    if not Rst:
        Rst='\n'
    return Rst
#2提示输入框
MultText=lambda *a:f('MultText')(*a)
def Input(Ttl='',Msg='',Txt=''):
    Rst=MultText(Ttl,(Msg,Txt))
    if Rst!=None:
        Rst=Rst[0]
    return Rst
#登录窗口
LoginText=lambda *a:f('LoginText')(*a)
def Login(Ttl='登录',Msg=('用户名','密码')):
    Rst=LoginText(Ttl,{0:Msg[0],1:Msg[1]})
    if not (Rst and Rst[0] and Rst[1]):
        return None,None
    return Rst[0],Rst[1]
def Password(Ttl='登录',Msg='重复密码'):
    Rst=LoginText(Ttl,{2:Msg})
    if not (Rst and Rst[2]):
        return None
    return Rst[2]
#通用函数
def f(x,y=None,z=None):
    try:
        exec('from .%s import *'%x,_)
        if y==None:
            y=x
        if z==None:
            z=y
        y=eval(y)
        exec('global %s;%s=y'%(z,z))
        return y
    except:
        pass
_=globals()
#导入:from WinGui import winIO
#替代系统标准输入接口:sys.stdin=winIO
#  也可以替代系统普通输入函数:input=winIO.input
#替代系统标准输出接口:sys.stdout=sys.stderr=winIO
#  之后写入输出内容进缓冲区:
#    print(...)
#    sys.stdout.write(...)
#  显示输出内容:winIO.print()
#    利用系统输入暂停时显示输出:input=winIO.print
#  也可以直接替代系统普通输出函数:print=winIO.print