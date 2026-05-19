from .BaseWindow import *
from android import rsla,jsla
from os.path import abspath
from traceback import format_exc
XML="""<?xml version="1.0" encoding="utf-8"?>
<LinearLayout
	android:layout_width="fill_parent"
	android:layout_height="fill_parent"
	android:background="#5f7faf"
	android:orientation="vertical"
	xmlns:android="http://schemas.android.com/apk/res/android">
	<LinearLayout
		android:layout_width="fill_parent"
		android:layout_height="wrap_content"
		android:orientation="vertical"
		android:layout_weight="25">
	<ScrollView   
        android:layout_width="fill_parent"   
        android:layout_height="fill_parent" > 
	<LinearLayout
		android:layout_width="fill_parent"
		android:layout_height="fill_parent"
		android:orientation="vertical" >	
    <EditText
        android:background="#ffffff"
		android:id="@+id/Title"
		android:layout_width="fill_parent"
		android:layout_height="wrap_content"
		android:textSize="8dp"
		android:text="%s"
		android:textColor="#ff0000"
		android:gravity="center"
		android:enabled="false"
	/>
	<EditText
        android:background="#ffffaf"
		android:id="@+id/MusicFileName"
		android:layout_width="fill_parent"
		android:layout_height="wrap_content"
		android:text="%s"
		android:textColor="#0000ff"
		android:enabled="false"
	/>%s
	</LinearLayout>
	</ScrollView>
	</LinearLayout>%s
	<SeekBar
		android:id="@+id/MusicTime"
		android:layout_width="fill_parent"
		android:layout_height="wrap_content"
		android:layout_weight="0.8"
		android:layout_marginLeft="10dp"
		android:layout_marginRight="10dp"
		android:background="#ffcfcf"
	/>
	<EditText
        android:background="#ffffff"
		android:id="@+id/MusicNowTime"
		android:layout_width="fill_parent"
		android:layout_height="wrap_content"
		android:text=" "
		android:textColor="#007f00"
		android:layout_weight="0.9"
		android:enabled="false"
		android:typeface="serif"
	/>
	<LinearLayout
		android:layout_width="fill_parent"
		android:layout_height="wrap_content"
		android:orientation="horizontal"
		android:layout_weight="1">
	<RadioButton
		android:layout_width="fill_parent"
		android:layout_height="fill_parent"
		android:text="停止"
		android:id="@+id/Play"
		android:textAllCaps="false"
		android:background="#007f7f"
		android:textColor="#ffffffff"
		android:layout_weight="1"
		android:gravity="center"/>
	<RadioButton
		android:layout_width="fill_parent"
		android:layout_height="fill_parent"
		android:text="暂停"
		android:id="@+id/Pause"
		android:textAllCaps="false"
		android:background="#7f7f00"
		android:textColor="#ffffffff"
		android:layout_weight="1"
		android:gravity="center"/>
	<RadioButton
		android:layout_width="fill_parent"
		android:layout_height="fill_parent"
		android:text="退出"
		android:id="@+id/Exit"
		android:textAllCaps="false"
		android:background="#7f3f3f"
		android:textColor="#ffffffff"
		android:layout_weight="1"
		android:gravity="center"/>
	</LinearLayout>
</LinearLayout>"""
LrcXml='''
    <EditText
        android:background="#ffffff"
		android:id="@+id/MusicNowLyric"
		android:layout_width="fill_parent"
		android:layout_height="wrap_content"
		android:textSize="8dp"
		android:text=" "
		android:textColor="#ef7000"
		android:layout_weight="0.8"
		android:enabled="false"
	/>''','''
	<EditText
        android:background="#bfffbf"
		android:id="@+id/Lyric"
		android:layout_width="fill_parent"
		android:layout_height="wrap_content"
		android:textColor="#cf00cf"
		android:enabled="false"
	/>'''
def getSec(Dict,Name):
    try:
        r=Dict[Name]
    except:
        return '0分0.000秒',0
    s,t=divmod(r,60000)
    s=int(s)
    t=round(t/1000,3)
    return '%2d分%6.3f秒'%(s,t),r
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
def shwLrc(Time):
    if Time<LrcT[0]:
        k=(LrcT[0]-Time)//1000
        if k<=4:
            k=Dot[1]*(4-k)+Dot[0]*k
        else:
            k=''
        v.MusicNowLyric.html=f"<font color=#bf6030>{k}</font>"
        return
    elif Time>=LrcT[lrcm]:
        shwLrcPlus(lrcm,Time)
        return
    a=0;b=lrcm
    while a!=b:
        c=(a+b)//2
        if Time<LrcT[c]:
            b=c
        elif Time>=LrcT[c+1]:
            a=c
        else:
            shwLrcPlus(c,Time)
            return
    else:
        shwLrcPlus(a,Time)
def shwLrcPlus(k,Time):
    s=Lrc[k]
    if s!="":
        v.MusicNowLyric.text=s
        return
    if k>=lrcm:
        t=ttTime
    else:
        t=LrcT[k+1]
    s=(t-Time)//1000
    if s<1:
        s=""
    else:
        s=" %ss"%s
    v.MusicNowLyric.html=f"<font color=#bf6030>-- Music{s} --</font>"
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
PPE=('Pause','Play','Exit')
EDT=('Title','MusicFileName','MusicNowTime','MusicNowLyric','Lyric')
F3=['false','false','false']
mtColor='f00','303030','008080','0f0','800080','00f','808000'
def Info():
    global npo
    npo=mt.progress
    np=op=int(npo)
    jsla('fullSetProperties',EDT,'enabled','false')
    while True:
        if rsla('mediaIsPlaying'):
            s='播放中'
        else:
            s='未播放'
            v.Play.text='播放'
            v.Pause.text='继续'
        Seek()
        t=rsla('mediaPlayInfo')
        t,i=getSec(t,'position')
        ShwLrc(i)
        np=i//1000
        if np!=op:
            mt.progress=npo=str(np)
            if np%8==0:
                mt.progressColor='#'+mtColor[np%7]
            op=np
        v.MusicNowTime.text='%s/%s  %s'%(t,dur,s)
        if s=='未播放' or rsla('fullGetProperties',PPE,'checked')!=F3:
            jsla('fullSetProperties',EDT,'enabled','true')
            break
def Seek():
    if npo!=mt.progress:
        jsla('mediaPlaySeek',int(mt.progress)*1000)
def Err():
    v.MusicFileName.text=v.MusicFileName.text+"\n"+format_exc()
    jsla('mediaPlayClose')
class MainScreen(Layout):
    def on_show(self):
        global v,mt,ttTime
        v=self.views
        v.Play.add_event(click_EventHandler(v.Play,self.play))
        v.Pause.add_event(click_EventHandler(v.Pause,self.pause))
        mt=v.MusicTime
        mt.add_event(click_EventHandler(mt,Info))
        v.Exit.add_event(click_EventHandler(v.Exit,self.exit))
        try:
            if rsla('mediaIsPlaying'):
                jsla('mediaPlayClose')
            global dur
            if dur:
                v.Lyric.text=dur
            jsla('mediaPlay',Path)
            r=rsla('mediaPlayInfo')
            dur,ttTime=getSec(r,'duration')
            mt.max=str(ttTime//1000)
            if loop:
                jsla('mediaPlaySetLooping',True)
            Info()
        except:
            Err()
    def on_close(self):
        pass
    def play(self,view,dummy):
        try:
            if rsla('mediaIsPlaying'):
                jsla('mediaPlayClose')
            else:
                jsla('mediaPlay',Path)
                v.Play.text='停止'
                v.Pause.text='暂停'
            v.Play.checked='false'
            Info()
        except:
            Err()
    def pause(self,view,dummy):
        try:
            if rsla('mediaIsPlaying'):
                jsla('mediaPlayPause')
            else:
                Seek()
                jsla('mediaPlayStart')
                v.Pause.text='暂停'
                v.Play.text='停止'
            v.Pause.checked='false'
            Info()
        except:
            Err()
    def exit(self,view,dummy):
        if exitStop:
            jsla('mediaPlayClose')
        FullScreenWrapper2App.close_layout()
def MusicPlay(MusicPath='',Title='QPython Music Player',Loop=False,ExitPlay=False):#主函数
#音乐播放(音乐文件路径,标题,单曲循环,退出后继续播放)
#支持LRC歌词文件
#例如MusicPlay("Aa/Bb.mp3")，如果"Aa/Bb.lrc"同时存在，则两个文件会被同时导入
    global Path,Path2,dur,Lrc,ShwLrc,loop,exitStop
    Path=abspath(MusicPath)
    Path2=MusicPath
    try:
        dur=TxtRead(Path[:Path.rfind('.')]+'.lrc')
        LrcAna(dur)
        x=Str2Xml(Title),Str2Xml(Path2),LrcXml[1],LrcXml[0]
        ShwLrc=shwLrc
    except:
        dur='';Lrc=()
        x=Str2Xml(Title),Str2Xml(Path2),'',''
        ShwLrc=lambda s:None
    loop=Loop
    exitStop=not ExitPlay
    FullScreenWrapper2App.show_layout(MainScreen(XML%x))
    FullScreenWrapper2App.eventloop()
__all__=('MusicPlay','droid')
#QPython Music Player by 乘着船 at https://www.bilibili.com/read/cv8698688