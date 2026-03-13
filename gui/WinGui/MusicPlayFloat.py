#qpy:quiet
#需要QPython Plus >= 3.9.1
try:
    from .BaseWindow import *
except:
    from BaseWindow import *
from android import rsla,jsla
from os.path import abspath
from traceback import format_exc
from time import time
def getSec(Dict,Name):
    try:
        return Dict[Name]
    except:
        return 0
def TxtRead(File):
    m=open(File,"rb").read()
    if m[0:3]==b'\xef\xbb\xbf':#UTF-8文件头
        return m[3:].decode("utf-8")
    else:
        try:
            return m.decode("utf-8")
        except:
            try:
                return m.decode("gbk")
            except:
                return m.decode("utf-16")
def LrcAna(con):
    global Lrc,lrcm,LrcT
    con=con.splitlines()
    Lrc=[]
    for a in con:
        b=a.rfind(']')
        if b==-1:
            continue
        c=a[b+1:]
        d=a[1:b].replace(' ','')
        e=d.split('][')
        for f in e:
            g=colon2Time(f)
            if g==-1:
                continue
            Lrc.append((g,c))
    Lrc=sorted(Lrc)
    lrcm=len(Lrc)
    LrcT=[]
    for a in range(lrcm):
        LrcT.append(Lrc[a][0])
        Lrc[a]=Lrc[a][1]
    lrcm-=1
    Lrc=tuple(Lrc)
    LrcT=tuple(LrcT)
def showLrc(lrcNow,lrcNext=''):
    global lrco,ftm
    lrcn=lrcNow,lrcNext
    if lrcn==lrco:#歌词不变
        #如果：首次1秒强制刷新
        if ftm and time()-ftm>1:
            ftm=lrco=None
        else:
            return
    if type(lrcNow)==str:
        if lrcNow!='':
            text=lrcNow
            color='0000ff'
        else:
            text=defaultText
            color='ff00ff'
    else:
        text='-- Music %ss --'%lrcNow
        color='ff00ff'
    html=HtmlTwoLine%(Str2Xml(text),Str2Xml(lrcNext))
    jsla('floatView',{'html':html,'textColor':color,'textSize':20,'backColor':'cfffff00','width':1000,'height':250,'index':0,lock[0]:lock[1]})
    lrco=lrcn
def shwLrc(Time):
    Time+=off
    if Time<LrcT[0]:
        k=(LrcT[0]-Time)//1000
        if k<=4:
            k=Dot[1]*(4-k)+Dot[0]*k
        if lrcm>=1:
            next=Lrc[0]
        else:
            next=''
        return showLrc(k,next)
    elif Time>=LrcT[lrcm]:
        return showLrcEnd(Time,lrcm)
    a=0;b=lrcm
    while a!=b:
        c=(a+b)//2
        if Time<LrcT[c]:
            b=c
        elif Time>=LrcT[c+1]:
            a=c
        else:
            return showLrcPlus(Time,c)
    else:
        return showLrcPlus(Time,a)
def showLrcPlus(Time,Position):
    if Lrc[Position]!='':
        Next=Lrc[Position+1]
        if Next=='':
            try:
                Next=Lrc[Position+2]
            except:
                pass
        return showLrc(Lrc[Position],Next)
    k=(LrcT[Position+1]-Time)//1000
    if k<=0:
        return showLrc('',Lrc[Position+1])
    else:
        return showLrc(k,Lrc[Position+1])
def showLrcEnd(Time,Position):
    lrc=Lrc[Position]
    if lrc!='':
        return showLrc(lrc,EndText)
    try:
        k=(showLrcEnd.duration-Time)//1000
    except:
        showLrcEnd.duration=rsla('mediaPlayInfo')['duration']
        k=(showLrcEnd.duration-Time)//1000
    if k<=0:
        return showLrc('',EndText)
    else:
        return showLrc(k,EndText)
def colon2Time(Time):
    T=Time.split(':',1)
    try:
        return int(Eval(T[0])*60000+Eval(T[1])*1000)
    except:
        return -1
def Eval(x):
    x=x.strip()
    if x[0]=='0':
        x=x[1:]
    if x=='':
        return 0
    else:
        return eval(x)
Dot=chr(9675),chr(9679)
lrco=defaultText='--QPython音乐播放器--'
HtmlTwoLine='%s<br><small><small><font color=#000000>%s</font></small></small>'
EndText='--End--'
def Info():
    global off
    t=rsla('mediaPlayInfo')
    i=getSec(t,'position')
    off=int((time()-off)*1000)
    ShwLrc(i)
    while rsla('mediaIsPlaying'):
        t=rsla('mediaPlayInfo')
        i=getSec(t,'position')
        ShwLrc(i)
    ExitFloatView('播放完成')
    jsla('sharedVariableRemove','MusicPlayFloat')
def ExitFloatView(Text):
    jsla('makeToast',Text)
    jsla('floatViewRemove')
def Err():
    showLrc(format_exc())
    jsla('mediaPlayClose')
def MusicPlayFloat(MusicPath,Seek=0,LockFloatPosition=False):#主函数
#音乐播放-悬浮窗歌词(音乐文件路径,跳过毫秒数=0,锁定悬浮窗位置=否)
#音乐播放-悬浮窗歌词(音乐文件路径,跳过毫秒数=0,锁定悬浮窗位置={'x':x值,'y':y值})
#支持LRC歌词文件
#例如MusicPlayFloat("Aa/Bb.mp3")，如果"Aa/Bb.lrc"同时存在，则两个文件会被同时导入
#如果不存在对应lrc文件，可以播放音乐，但不会显示悬浮窗歌词
    global Path,dur,Lrc,ShwLrc,off,ftm,lock
    if rsla('mediaIsPlaying'):
        if rsla('sharedVariableGet','MusicPlayFloat')!=None:
            jsla('makeToast','其他歌词悬浮窗守护进程正在运行')
            exit()
        Path=rsla('mediaPlayInfo')['url']
    else:
        Path=abspath(MusicPath)
    jsla('sharedVariableSet','MusicPlayFloat','')
    off=time()
    if LockFloatPosition:
        if type(LockFloatPosition)!=dict:
            LockFloatPosition={}
        #flag=Default_Not_Touchable(24)
        lock=('flag',24,LockFloatPosition.get('x',0),LockFloatPosition.get('y',-1000))
    else:
        #clickRemove=False
        lock=('clickRemove',False,0,-1000)
    try:
        ftm=Path[Path.rfind('/')+1:]
        dur=TxtRead(Path[:Path.rfind('.')]+'.lrc')
        LrcAna(dur)
        ShwLrc=shwLrc
        jsla('floatView',{'text':lrco,'textColor':'ff007f','textSize':20,'backColor':'cfffff00','x':lock[2],'y':lock[3],'width':1000,'height':250,'index':0,lock[0]:lock[1]})
        jsla('makeToast',ftm)
    except:
        dur='';Lrc=()
        ShwLrc=lambda s:None
        ExitFloatView(ftm+'\n没有歌词')
    ftm=off
    if not rsla('mediaIsPlaying'):
        jsla('mediaPlay',Path)
        jsla('mediaPlaySeek',Seek)
    Info()
__all__=('MusicPlayFloat',)
#参数传入格式 和 函数格式 基本相同，
#包含:MusicPath,Seek,LockFloatPosition，
#例如:
# 'MusicPlayFloat.py' '/sdcard/Path/The Music.mp3' 500 '{x:-200,y:-500}'
# 'MusicPlayFloat.py' '/sdcard/Path/The Music.mp3'
import sys as s
try:
    s=s.argv[1:]
    if s!=[]:
        path=s[0]
        if len(s)>1:
            s[1]=eval(s[1])
        if len(s)>2:
            x='x';y='y'
            s[2]=eval(s[2])
        s=tuple(s)
        MusicPlayFloat(*s)
except:
    raise
#QPython Music Player by 乘着船 at https://www.bilibili.com/read/cv8698688