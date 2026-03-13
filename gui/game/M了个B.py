#qpy:quiet
#标题：字母消除：M了个B
#作者：乘着船 @ Bilibili
#平台要求：QPython 3C >= 3.7.0
#脚本路径：qpython/scripts3/M了个B.py
from qsl4ahelper.fullscreenwrapper2 import *
from android import *
from time import sleep
XML="""<?xml version="1.0" encoding="utf-8"?>
<LinearLayout
	android:layout_width="fill_parent"
	android:layout_height="fill_parent"
	android:orientation="vertical"
	android:background="#7f3faf"
	xmlns:android="http://schemas.android.com/apk/res/android"
	xmlns:qpython="http://www.qpython.org">
    <TextView
		android:id="@+id/Title"
		android:layout_width="fill_parent"
		android:layout_height="wrap_content"
		android:textSize="7dp"
		android:text="%s"
		android:background="#af7f3f"
		android:textColor="#ffffff"
		android:textStyle="bold"
		android:gravity="center"
	/>
    <GridView
        android:id="@+id/Reserve"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:layout_weight="20"
        android:numColumns="%s"
        android:background="#7f3f3f"
    />
    <TextView
		android:id="@+id/Notice"
		android:layout_width="fill_parent"
		android:layout_height="wrap_content"
		qpython:html="%s"
		android:textColor="#ffffff"
		android:textSize="7sp"
	/>
    <GridView
        android:id="@+id/Occupy"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:layout_weight="20"
        android:numColumns="%s"
        android:background="#3f7f3f"
    />
	<TextView 
		android:layout_width="fill_parent"
		android:layout_height="wrap_content"
		android:text="%s"
		android:id="@+id/but_canc"
		android:textSize="7dp"
		android:background="#7f3faf"
		android:textColor="#ffffff"
		android:gravity="center"
		android:clickable="true" />
</LinearLayout>"""
class MainScreen(Layout):
    def on_show(self):
        global v,Notice
        v=self.views
        v.Reserve.add_event(itemclick_EventHandler(v.Reserve,self.Reserve))
        v.Occupy.add_event(itemclick_EventHandler(v.Occupy,self.Occupy))
        getReserveOccupy()
        d=v.but_canc
        c=d.add_event
        c(click_EventHandler(d,self.canc))
        Notice=Notice.split('<br>')[1].replace('砖块机会','')
    def on_close(self):
        pass
    def Reserve(self,view,dummy):
        global lock,total,Notice
        if lock:
            return
        elif lock==None:
            updateNotice()
            lock=False
        pos=int(dummy['data']['position'])
        a=stack[pos]
        if not a:
            return
        if len(Occupy)<OccupyLength:
            Occupy.append(a.pop(-1))
        Occupy.sort()
        a=None;c=d=0
        while d<len(Occupy):
            b=Occupy[d]
            if b!=a:
                a=b;c=1
            else:
                c+=1
                if c>=Eliminate:
                    getReserveOccupy()
                    d-=Eliminate-1
                    for c in range(Eliminate):
                        Occupy.pop(d)
                    total-=Eliminate
                    updateNotice()
                    jsla('makeToast','消除：<font color=#ff0000><big>%s</big></font>！'%a,0,True)
                    sleep(.8)
                    break
            d+=1
        if len(Occupy)>=OccupyLength:
            Notice+=LOSE
            updateNotice()
            lock=True
            jsla('makeToast',LOSE)
        elif total==0:
            Notice+=WIN
            updateNotice()
            lock=True
            jsla('makeToast',WIN)
        getReserveOccupy()
    def Occupy(self,view,dummy):
        if lock:
            return
        global RemoveOpportunity
        pos=int(dummy['data']['position'])
        if not RemoveOpportunity:
            return
        empty=[]
        for i in range(sizeSquare):
            if stack[i]:
                continue
            empty.append(i)
        if empty:
            i=empty[randint(0,len(empty)-1)]
        else:
            i=randint(0,sizeSquare-1)
        stack[i].append(Occupy.pop(pos))
        getReserveOccupy()
        RemoveOpportunity-=1
        updateNotice()
    def canc(self,view,dummy):
        FullScreenWrapper2App.close_layout()
b=__file__[:-3]+'.ini'
try:
    exec(open(b).read())
    for a in ReserveSize,OccupyLength,BrickType,BrickRepeat,Eliminate,RemoveOpportunity:
        if type(a)!=int:
            raise
    if type(Title)!=str:
        raise
except:
    a='''
Title="字母消除:M了个B"
ReserveSize=4 #保留区尺寸
OccupyLength=8 #占有区长度
BrickType=10 #砖块种类数
BrickRepeat=4 #砖块重复组数
Eliminate=3 #同种砖块消除个数
RemoveOpportunity=3 #移出机会
'''
    open(b,'w').write(a)
    exec(a)
Notice='字母表示砖块类型，数字表示砖块层数，持有%s个相同类型砖块即为消除。剩余砖块为0即为赢，持有砖块%s个即为输。'%(Eliminate,OccupyLength)+'<br>剩余搬回砖块机会：<font color=#00ff00><big>%s</big></font>，剩余砖块：<font color=#00ff00><big>%s</big></font>。'
Cancel='退出'
def getReserveOccupy():
    Reserve.clear()
    for a in range(sizeSquare):
        b=stack[a]
        c=len(b)
        if c==0:
            Reserve.append('')
        else:
            Reserve.append('<big>%s</big><small><font color=#00ff00>%s</font></small>'%(b[-1],c))
        jsla('fullSetListHtml',v.Reserve.view_id,Reserve)
    Occupy.sort()
    v.Occupy.set_listitems(Occupy)
Reserve=[];Occupy=[]
def updateNotice():
    v.Notice.html=Notice%(RemoveOpportunity,total)
def Str2Xml(s):
    t=[];r=t.append
    for i in s:
        j=ord(i)
        if j<256 and not (i.isalpha() or i.isdigit()):
            r('&#');r(str(j));r(";")
        else:
            r(i)
    return ''.join(t)
FullScreenWrapper2App.initialize(droid)
from random import randint
lock=[]
b=list(range(26))
for a in range(BrickType):
    lock.append(chr(65+b.pop(randint(0,len(b)-1))))
lock*=Eliminate*BrickRepeat
sizeSquare=ReserveSize*ReserveSize
total=len(lock)
stack=[]
for a in range(sizeSquare):
    stack.append([lock.pop(randint(0,len(lock)-1))])
b=sizeSquare-1
while lock:
    stack[randint(0,b)].append(lock.pop(randint(0,len(lock)-1)))
lock=None
LOSE='你输了！'
WIN='你赢了！'
del a,b
Layout.defaultTheme=16973833#Theme_Black_NoTitleBar
FullScreenWrapper2App.show_layout(MainScreen(XML%(Str2Xml(Title),ReserveSize,Str2Xml(Notice%(RemoveOpportunity,total)),ReserveSize,Cancel),title=Title))
FullScreenWrapper2App.eventloop()
#视频演示：https://www.bilibili.com/video/BV1ge4y1H7AW