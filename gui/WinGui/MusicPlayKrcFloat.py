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
import zlib,base64
from time import time
def getSec(Dict,Name):
    try:
        return Dict[Name]
    except:
        return 0
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
def showLrc(lrcn,spe=False):
    global lrco,ftm
    if lrcn==lrco:#歌词不变
        #如果：首次1秒强制刷新
        if ftm and time()-ftm>1:
            ftm=lrco=None
        else:
            return
    data={'textSize':20,'backColor':'cfffffff','width':1000,'height':250,'index':0,lock[0]:lock[1]}
    if lrcn=='':
        data['html']=defaultText
        data['textColor']='007f00'
    elif spe:
        data['html']=lrcn
        data['textColor']='007f00'
    else:
        data['html']=lrcn
    try:
        data['html']+=showLrc.NextLrc
        if len(data['html'].split('<br>'))>3:
            data['height']=400
    except:
        pass
    jsla('floatView',data)
    lrco=lrcn
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
            return showLrc(lastShowLyric)
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
        makeNextLrc(0)
        if k<=4:
            return showLrc(AfterSing%Dot[1]*(4-k)+BeforeSing%Dot[0]*k)
        else:
            return showLrc('-- Music %ss --'%k,True)
    elif Time>=KrcStrc.max:
        return makeEndMusicText(Time)
    if c!=lastLine:
        while c<KrcStrc.len:
            if KrcStrc.lineStart[c]<=Time<KrcStrc.lineEnd[c]:
                makeNextLrc(c+1)
                break
            if c+1<KrcStrc.len and KrcStrc.lineEnd[c]<=Time<KrcStrc.lineStart[c+1]:
                makeNextLrc(c+1)
                k=(KrcStrc.lineStart[c+1]-Time)//1000
                c=KrcStrc.len
                break
            c+=1
        lastLine=c
    else:
        makeNextLrc(-1)
    try:
        d=KrcStrc.wordLyric[c]
    except:
        try:
            if k>0:
                k='-- Music %ss --'%k
            else:
                k=''
        except:
            k=''
        return showLrc(k,True)
    e=KrcStrc.wordStart[c]
    f=KrcStrc.wordEnd[c]
    if Time<e[0]:
        return showLrc('')
    elif Time>=f[-1]:
        if c>=KrcStrc.len-1:
            return makeEndMusicText(Time)
        return showLrc('')
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
            othLyric='<small>'+AfterSingOth%Str2Xml(''.join(h[:j]))+SingingOth%g+BeforeSingOth%Str2Xml(''.join(h[k:]))+'</small>'
            transLyric.append(othLyric)
        transLyric='<br><i>'+"<br>".join(transLyric)+'</i>'
        lastShowLyric='<small>'+lastShowLyric+transLyric+'</small>'
    showLrc(lastShowLyric)
def makeNextLrc(LineNo):
    if LineNo<0:return
    try:
        NextLrc=KrcStrc.lyric[LineNo]
        if KrcStrc.othLyric:
            transLyric=[NextLrc]
            for othLyric in KrcStrc.othLyric:
                transLyric.append('<small>'+Str2Xml(othLyric[LineNo])+'</small>')
            NextLrc="<br>".join(transLyric)
    except:
        if LineNo>=KrcStrc.len:
            NextLrc='--End--'
        else:
            return
    showLrc.NextLrc=NextSing%NextLrc
def makeSingingKrc(center,next,words):
    try:
        if center!=next:
            return Str2Xml(words[center])
        else:
            return ''
    except:
        return ''
def makeEndMusicText(Time):
    try:
        k=(KrcStrc.duration-Time)//1000
    except:
        KrcStrc.duration=rsla('mediaPlayInfo')['duration']
        k=(KrcStrc.duration-Time)//1000
    if k<=0:
        showLrc.NextLrc=''
        return showLrc(EndText,True)
    else:
        showLrc.NextLrc=NextSing%EndText
        return showLrc('-- Music %ss --'%k,True)
Dot='○●'
BeforeSing='<font color="#ef7000">%s</font>'
Singing='<font color="#ef00ef"><b>%s</b></font>'
AfterSing='<font color="#0070ef">%s</font>'
BeforeSingOth='<font color="#9fb000">%s</font>'
SingingOth='<font color="#bf50bf"><b>%s</b></font>'
AfterSingOth='<font color="#00b09f">%s</font>'
NextSing='<br><small><small><font color=#000000>%s</font></small></small>'
PPE=('Pause','Play','Exit')
F3=['false','false','false']
mtColor='f00','0f0','00f','808000','800080','008080','555555'
lrco=defaultText='--QPython音乐播放器--'
EndText='-- End --'
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
def Time():
    return int(time()*1000)
def Err():
    v.MusicFileName.text=v.MusicFileName.text+"\n"+format_exc()
    jsla('mediaPlayClose')
def MusicPlayKrcFloat(MusicPath='',Seek=0,LockFloatPosition=False):#主函数
#音乐播放-悬浮窗歌词(音乐文件路径,跳过毫秒数=0,锁定悬浮窗位置=否)
#音乐播放-悬浮窗歌词(音乐文件路径,跳过毫秒数=0,锁定悬浮窗位置={'x':x值,'y':y值})
#支持KRC歌词文件
#例如MusicPlayFloat("Aa/Bb.mp3")，如果"Aa/Bb.krc"同时存在，则两个文件会被同时导入
#如果不存在对应krc文件，可以播放音乐，但不会显示悬浮窗歌词
    global Path,ShwLrc,off,ftm,lock
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
        KrcRead(Path[:Path.rfind('.')]+'.krc')
        ShwLrc=makeLrc
        jsla('floatView',{'text':lrco,'textColor':'00af00','textSize':20,'backColor':'cfffffff','x':lock[2],'y':lock[3],'width':1000,'height':250,'index':0,lock[0]:lock[1]})
        jsla('makeToast',ftm)
    except:
        Lrc=()
        ShwLrc=lambda s:None
        ExitFloatView(ftm+'\n没有歌词')
    ftm=off
    if not rsla('mediaIsPlaying'):
        jsla('mediaPlay',Path)
        jsla('mediaPlaySeek',Seek)
    Info()
__all__=('MusicPlayKrcFloat',)
#参数传入格式 和 函数格式 基本相同，
#包含:MusicPath,Seek,LockFloatPosition，
#例如:
# 'MusicPlayKrcFloat.py' '/sdcard/Path/The Music.mp3' 500 '{x:-200,y:-500}'
# 'MusicPlayKrcFloat.py' '/sdcard/Path/The Music.mp3'
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
            del x,y
        s=tuple(s)
        MusicPlayKrcFloat(*s)
except:
    raise
#QPython Music Player by 乘着船 at https://www.bilibili.com/read/cv8698688