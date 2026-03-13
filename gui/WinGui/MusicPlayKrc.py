from .BaseWindow import *
from android import rsla,jsla
from os.path import abspath
from traceback import format_exc
import zlib,base64
from time import time
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
		android:textSize="8dp"
		android:background="#007f7f"
		android:textColor="#ffffffff"
		android:layout_weight="1"
		android:gravity="center"/>
	<RadioButton
		android:layout_width="fill_parent"
		android:layout_height="fill_parent"
		android:text="暂停"
		android:id="@+id/Pause"
		android:textSize="8dp"
		android:background="#7f7f00"
		android:textColor="#ffffffff"
		android:layout_weight="1"
		android:gravity="center"/>
	<RadioButton
		android:layout_width="fill_parent"
		android:layout_height="fill_parent"
		android:text="退出"
		android:id="@+id/Exit"
		android:textSize="8dp"
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
		android:textColor="#ff009f"
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
def KrcRead(File):
    krc_content=open(File,"rb").read()
    krc_text_decode = krc_decode(krc_content)
    make_krc_strc()
    krc_analyse_one(krc_text_decode)
    lrc_content = lrc_generate_all()
    optimize_krc_strc()
    return lrc_content
def krc_decode(krc_content):
    krc_content = krc_content[4:]
    krc_len = len(krc_content)
    krc_compress = []
    for krc_content_pos in range(0,krc_len):
        krc_compress.append( krc_content[krc_content_pos] ^ enKey[krc_content_pos % 16] )
    krc_compress = bytes(krc_compress)
    krc_text = zlib.decompress(krc_compress)
    krc_text = krc_text[3:].decode()
    return krc_text
def make_krc_strc():
    global KrcStrc
    class KrcStrc:
        colon=[]
        time=[]
        lineStart=[]
        lineEnd=[]
        wordStart=[]
        wordEnd=[]
        lyric=[]
        othLyric=[]
        wordLyric=[]
        othWordLyric=[]
enKey = (64, 71, 97, 119, 94, 50, 116, 71, 81, 54, 49, 45, 206, 210, 110, 105)
def krc_analyse_one(krc_text_decode):
    krc_lines = krc_text_decode.splitlines()
    for krc_line in krc_lines:
        krc_analyse_line(krc_line)
    KrcStrc.min = KrcStrc.lineStart[0]
    KrcStrc.max = KrcStrc.lineEnd[-1]
    KrcStrc.len = len(KrcStrc.lineStart)
def krc_analyse_line(krc_line):
    krc_line_content = [''] * 4
    krc_line_content[2:] = krc_line[1:].split("]",1)
    if krc_line_content[2].find(":")>0:
        Splitter=":"
    else:
        Splitter=","
    try:
        krc_line_content[0],krc_line_content[2] = krc_line_content[2].split(Splitter)
    except:
        return
    krc_line_content[1] = Splitter
    if krc_line_content[0] == 'guage':
        krc_line_content[0] = 'language'
    if Splitter==",":
        krc_comma(krc_line_content)
    elif krc_line_content[0] == 'language':
        krc_language(krc_line_content[2])
    else:
        krc_oth_colon(krc_line_content,KrcStrc.colon)
def krc_comma(krc_line_content):
    oldLine = check_and(krc_line_content[3])
    newLine = []
    LinePosition = 0
    krc_line_start = int(krc_line_content[0])
    krc_line_end = int(krc_line_content[2]) + krc_line_start
    krc_line_word_start = []
    krc_line_word_end = []
    krc_line_word_lyric = []
    while True:
        LeftBracketPosition = oldLine.find("<",LinePosition)
        if LeftBracketPosition == -1:
            break
        if LinePosition:
            krc_line_word_one = oldLine[LinePosition:LeftBracketPosition]
            krc_line_word_lyric.append(krc_line_word_one)
        newLine.append(oldLine[LinePosition:LeftBracketPosition])
        RightBracketPosition = oldLine.find(">",LeftBracketPosition+1)
        LinePosition = RightBracketPosition + 1
        krc_line_word_one_start_end =  oldLine[LeftBracketPosition+1:RightBracketPosition]
        krc_line_word_one_start_end = krc_line_word_one_start_end.split(',')
        krc_line_word_one_start = int(krc_line_word_one_start_end[0]) + krc_line_start
        krc_line_word_one_end = int(krc_line_word_one_start_end[1]) + krc_line_word_one_start
        krc_line_word_start.append(krc_line_word_one_start)
        krc_line_word_end.append(krc_line_word_one_end)
    krc_line_word_lyric.append(oldLine[LinePosition:])
    KrcStrc.lineStart.append(krc_line_start)
    KrcStrc.lineEnd.append(krc_line_end)
    KrcStrc.wordStart.append(krc_line_word_start)
    KrcStrc.wordEnd.append(krc_line_word_end)
    KrcStrc.wordLyric.append(krc_line_word_lyric)
    newLine.append(oldLine[LinePosition:])
    KrcLyric = KrcStrc.lyric
    KrcLyric.append("".join(newLine))
    KrcStrc.time.append(getMusicSecond(krc_line_start))
def check_and(Str):
    if Str.find('&')==-1:
        return Str
    return Str.replace('&apos;',"'")
def getMusicSecond(MusicSec):
    MusicMin , MusicSec = divmod ( MusicSec , 60000 )
    MusicSec = round ( MusicSec / 1000 , 3 )
    return "%s:%.3f"%(MusicMin,MusicSec)
def krc_language(b64Content):
    LyricContents = eval(base64.b64decode(bytes(b64Content,'utf-8')))['content']
    for lyricContent in LyricContents:
        lyricContent = lyricContent['lyricContent']
        newLyricContent = []
        newWordLyricContent = []
        for lyricLine in lyricContent:
            joinLyricLine="".join(lyricLine)
            newLyricContent.append(joinLyricLine)
            newWordLyricContent.append(lyricLine)
        KrcStrc.othLyric.append(newLyricContent)
        KrcStrc.othWordLyric.append(newWordLyricContent)
def krc_oth_colon(krc_line_content,krc_list_colon):
    if krc_line_content[0] in ('language','hash','id'):
        return
    ColonContent = krc_line_content[0],krc_line_content[2]
    krc_list_colon.append("[%s:%s]"%ColonContent)
def lrc_generate_all():
    class lrc_list:
        colon = "\n".join(KrcStrc.colon)
        Content = KrcStrc.lyric
    lrc_content = lrc_generate_one(lrc_list)
    oth_lrc_contents = []
    for lrc_list.Content in KrcStrc.othLyric:
        oth_lrc_content = lrc_generate_one(lrc_list)
        oth_lrc_contents.append(oth_lrc_content)
    if oth_lrc_contents:
        lrc_content += "\n\n\n" + "\n\n".join(oth_lrc_contents)+ "\n\n\n"
    return lrc_content
def lrc_generate_one(lrc_list):
    lyricLines = [lrc_list.colon]
    lyricLineNo = 0
    for lyricLineContent in lrc_list.Content:
        lyricLine = "[%s]%s"%(KrcStrc.time[lyricLineNo],lyricLineContent)
        lyricLines.append(lyricLine)
        try:
            if KrcStrc.lineEnd[lyricLineNo]<KrcStrc.lineStart[lyricLineNo+1]:
                lyricLines.append("[%s]"%getMusicSecond(KrcStrc.lineEnd[lyricLineNo]))
        except:
            pass
        lyricLineNo += 1
    lyricLines.append("[%s]"%getMusicSecond(KrcStrc.wordEnd[-1][-1]))
    lrc_content = "\n".join(lyricLines)
    return lrc_content
def optimize_krc_strc():
    del KrcStrc.colon,KrcStrc.time
    for i in range(len(KrcStrc.lyric)):
        if len(KrcStrc.wordLyric[i])==len(KrcStrc.lyric[i]):
            KrcStrc.wordLyric[i]=KrcStrc.lyric[i]
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
def makeLrc(Time):
    global lastLine,lastWord,lastShowLyric
    Time+=off
    try:
        if KrcStrc.lineStart[lastLine]<=Time<KrcStrc.lineEnd[lastLine]:
            c=lastLine
        elif KrcStrc.lineEnd[lastLine]<=Time:
            c=lastLine+1
            lastLine=lastWord=None 
        else:
            c=0
            lastLine=lastWord=None
    except:
        c=0
        lastLine=lastWord=None
    try:
        if e[lastWord]<=Time<f[lastWord] or f[lastWord-1]<=Time<e[lastWord]:
            mnl.html = lastShowLyric
            return
        elif f[lastWord]<=Time:
            i=lastWord+1
            lastWord=None
        else:
            i=0
            lastWord=None
    except:
        i=0
        lastWord=None
    if Time<KrcStrc.min:
        k=(KrcStrc.min-Time)//1000
        if k<=4:
            mnl.html = AfterSing%Dot[1]*(4-k)+BeforeSing%Dot[0]*k
        else:
            mnl.html = ''
        return
    elif Time>=KrcStrc.max:
        mnl.html = '-- End --'
        return
    if c!=lastLine:
        while c<KrcStrc.len:
            if KrcStrc.lineStart[c]<=Time<KrcStrc.lineEnd[c]:
                break
            if c+1<KrcStrc.len and KrcStrc.lineEnd[c]<=Time<KrcStrc.lineStart[c+1]:
                k=(KrcStrc.lineStart[c+1]-Time)//1000
                c=KrcStrc.len
                break
            c+=1
        lastLine=c
    try:
        d=KrcStrc.wordLyric[c]
    except:
        try:
            if k>0:
                k = '%ss '%k
            else:
                k=''
        except:
            k=''
        mnl.html = BeforeSing%('-- Music %s --'%k)
        return
    e=KrcStrc.wordStart[c]
    f=KrcStrc.wordEnd[c]
    if Time<e[0] or Time>=f[-1]:
        mnl.html = ''
        return
    if i!=lastWord:
        i=0;h=len(d)
        while i<h:
            if e[i]<=Time<f[i]:
                j=i
                k=i+1
                break
            if f[i-1]<=Time<e[i]:
                j=k=i
                break
            i+=1
        lastWord=i
    g=makeSingingKrc(i,k,d)
    lastShowLyric=AfterSing%Str2Xml(''.join(d[:j]))+Singing%g+BeforeSing%Str2Xml(''.join(d[k:]))
    if KrcStrc.othLyric:
        transLyric=[]
        for othLyric in KrcStrc.othWordLyric:
            h=othLyric[c]
            g=makeSingingKrc(i,k,h)
            othLyric=AfterSingOth%Str2Xml(''.join(h[:j]))+SingingOth%g+BeforeSingOth%Str2Xml(''.join(h[k:]))
            transLyric.append(othLyric)
        transLyric='<br><i>'+"<br>".join(transLyric)+'</i>'
        lastShowLyric+=transLyric
    mnl.html = lastShowLyric
def makeSingingKrc(center,next,words):
    try:
        if center!=next:
            return Str2Xml(words[center])
        else:
            return ''
    except:
        return ''
Dot='○●'
BeforeSing='<font color="#ef7000">%s</font>'
Singing='<font color="#ef00ef"><b>%s</b></font>'
AfterSing='<font color="#0070ef">%s</font>'
BeforeSingOth='<font color="#9fb000">%s</font>'
SingingOth='<font color="#bf50bf"><b>%s</b></font>'
AfterSingOth='<font color="#00b09f">%s</font>'
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
def Time():
    return int(time()*1000)
def Err():
    v.MusicFileName.text=v.MusicFileName.text+"\n"+format_exc()
    jsla('mediaPlayClose')
class MainScreen(Layout):
    def on_show(self):
        global v,mt,mnl,off,dur
        v=self.views
        v.Play.add_event(click_EventHandler(v.Play,self.play))
        v.Pause.add_event(click_EventHandler(v.Pause,self.pause))
        mt=v.MusicTime
        mt.add_event(click_EventHandler(mt,Info))
        v.Exit.add_event(click_EventHandler(v.Exit,self.exit))
        if ShwLrc==makeLrc:
            mnl=v.MusicNowLyric
        try:
            if rsla('mediaIsPlaying'):
                jsla('mediaPlayClose')
            if dur:
                v.Lyric.text=dur
            off=Time()
            jsla('mediaPlay',Path)
            r=rsla('mediaPlayInfo')
            off=Time()-off
            dur,r=getSec(r,'duration')
            mt.max=str(r//1000)
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
                off=Time()
                jsla('mediaPlay',Path)
                v.Play.text='停止'
                v.Pause.text='暂停'
                off=Time()-off
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
                off=Time()
                jsla('mediaPlayStart')
                v.Pause.text='暂停'
                v.Play.text='停止'
                off=Time()-off
            v.Pause.checked='false'
            Info()
        except:
            Err()
    def exit(self,view,dummy):
        if exitStop:
            jsla('mediaPlayClose')
        FullScreenWrapper2App.close_layout()
def MusicPlayKrc(MusicPath='',Title='QPython Music Player',Loop=False,ExitPlay=False):#主函数
#音乐播放(音乐文件路径,标题,单曲循环,退出后继续播放)
#支持酷狗KRC歌词文件
#例如MusicPlay("Aa/Bb.mp3")，如果"Aa/Bb.krc"同时存在，则两个文件会被同时导入
    global Path,Path2,dur,ShwLrc,loop,exitStop
    Path=abspath(MusicPath)
    Path2=MusicPath
    try:
        dur=KrcRead(Path[:Path.rfind('.')]+'.krc')
        x=Str2Xml(Title),Str2Xml(Path2),LrcXml[1],LrcXml[0]
        ShwLrc=makeLrc
    except:
        dur=''
        x=Str2Xml(Title),Str2Xml(Path2),'',''
        ShwLrc=lambda s:None
    loop=Loop
    exitStop=not ExitPlay
    FullScreenWrapper2App.show_layout(MainScreen(XML%x))
    FullScreenWrapper2App.eventloop()
__all__=('MusicPlayKrc','droid')
#QPython Music Player for Krc by 乘着船 at https://www.bilibili.com/read/cv8698688