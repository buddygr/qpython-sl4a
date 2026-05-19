#需要QPython 3C 3.6.7或以上，旧版QPython均无法正常运行
from .BaseWindow import *
XML="""<?xml version="1.0" encoding="utf-8"?>
<LinearLayout
	android:layout_width="fill_parent"
	android:layout_height="fill_parent"
	android:background="#0E4200"
	android:orientation="vertical"
	xmlns:android="http://schemas.android.com/apk/res/android">
	<LinearLayout
		android:layout_width="fill_parent"
		android:layout_height="fill_parent"
		android:orientation="vertical"
		android:layout_weight="20">
	<ScrollView   
        android:layout_width="fill_parent"   
        android:layout_height="fill_parent" > 
	<LinearLayout
		android:layout_width="fill_parent"
		android:layout_height="fill_parent"
		android:orientation="vertical"
		android:layout_weight="20">	
    <TextView
        android:background="#7f007f"
		android:id="@+id/Title"
		android:layout_width="fill_parent"
		android:layout_height="wrap_content"
		android:textSize="6dp"
		android:text=""
		android:textColor="#00ff00"
		android:layout_weight="1"
		android:gravity="center"
	/>
	<EditText
        android:background="#ffffff"
		android:id="@+id/Text"
		android:layout_width="fill_parent"
		android:layout_height="wrap_content"
		android:textSize="10dp"
		android:text="正在获取声音信息"
		android:textColor="#000000"
		android:layout_weight="1"
	/>
	</LinearLayout>
	</ScrollView>
    </LinearLayout>
	<LinearLayout
		android:layout_width="fill_parent"
		android:layout_height="100dp"
		android:orientation="horizontal"
		android:layout_weight="8">
	<RadioButton
		android:layout_width="fill_parent"
		android:layout_height="fill_parent"
		android:text="暂停"
		android:id="@+id/but_pause"
		android:textAllCaps="false"
		android:background="#007f7f"
		android:textColor="#ffffffff"
		android:layout_weight="1"
		android:gravity="center"/>
	<RadioButton
		android:layout_width="fill_parent"
		android:layout_height="fill_parent"
		android:text="复制"
		android:id="@+id/but_copy"
		android:textAllCaps="false"
		android:background="#7f7f00"
		android:textColor="#ffffffff"
		android:layout_weight="1"
		android:gravity="center"/>
	<RadioButton
		android:layout_width="fill_parent"
		android:layout_height="fill_parent"
		android:text="退出"
		android:id="@+id/but_exit"
		android:textAllCaps="false"
		android:background="#7f007f"
		android:textColor="#ffffffff"
		android:layout_weight="1"
		android:gravity="center"/>
	</LinearLayout>
</LinearLayout>"""
from time import time,localtime,strftime
def getSoundConti():
    t0=0
    v.Text.enabled='false'
    while v.but_copy.checked=='false' and v.but_pause.checked=='false' and v.but_exit.checked=='false':
        t=time()
        if t-t0>=timeInterval:
            getSoundOnce()
            if timeInterval<0:
                #单次测试
                p=v.but_pause
                p.checked='true'
                p.text='继续'
            else:
                t0=t
    v.Text.enabled='true'
mdb=-1
def getSoundOnce():
    try:
        global mdb
        db=getDb()
        if db==None:
            db=-255
        if db==-255:
            note='\n请确认QPython麦克风权限。'
        else:
            note=''
        if db>mdb:
            mdb=db
        T.html=colord(db,mdb,note)
    except:
        from traceback import format_exc
        T.text=format_exc()
        v.Title.text="错误信息"
        p=v.but_pause
        p.checked='true'
        p.text='继续'
def split(x):
    x=str(round(x,2)).split('.')
    if len(x)<2:
        x.append('0')
    return x
def colord(c,m,n):
    c=split(c)
    m=split(m)
    t=time()
    t=strftime('<font color=#7f007f>%Y-%m-%d</font> <font color=#7f7f00>%H:%M:%S</font><font color=#7f7f7f>',localtime(t))+str(round(t-int(t),3))[1:]
    if n:
        n='<br>'+n
    return '<big><font color=#007f00>当前分贝</font>：<br><big><font color=#ff0000>%s</font>.</big><font color=#0000ff>%s</font></big><br><font color=#007f00>最大分贝</font>：<br><big><font color=#ff0000>%s</font>.</big><font color=#0000ff>%s</font><br><small><font color=#007f7f>系统时间</font>：<br>%s</font></small>%s'%(c[0],c[1],m[0],m[1],t,n)
def getDb():
    return rsla('recorderSoundVolumeGetDb')
def showInterval():
    if timeInterval<0:
        v.Title.text='单次(手动)测试'
    else:
        v.Title.text='连续(间隔%s秒)测试'%timeInterval
class MainScreen(Layout):
    def on_show(self):
        global v,T
        if timeInterval>0:
            v=int(timeInterval*900)
        else:
            v=100
        jsla('recorderSoundVolumeDetect',v)
        v=self.views
        T=v.Text
        v.but_pause.add_event(click_EventHandler(v.but_pause,self.pause))
        v.but_copy.add_event(click_EventHandler(v.but_copy,self.copy))
        v.but_exit.add_event(click_EventHandler(v.but_exit,self.exit))
        showInterval()
        getSoundConti()
    def on_close(self):
        pass
    def pause(self,view,dummy):
        p=v.but_pause
        p.checked='false'
        if p.text=='暂停':
            p.text='继续'
        else:
            p.text='暂停'
            showInterval()
            getSoundConti()
    def copy(self,view,dummy):
        jsla('setClipboard',T.text)
        v.but_copy.checked='false'
        jsla('makeToast','分贝信息已复制')
        if v.but_pause.text=='暂停':
            getSoundConti()
    def exit(self,view,dummy):
        jsla('recorderSoundVolumeDetect',-1)
        FullScreenWrapper2App.close_layout()
def SoundDbText(TimeInterval=0.5):#主函数
#分贝计(时间间隔=0.5秒)
#如果：时间间隔==-1，为单次(手动)测试
#如果：时间间隔>=0，为连续(自动)测试
    global timeInterval
    timeInterval=TimeInterval
    FullScreenWrapper2App.show_layout(MainScreen(XML))
    FullScreenWrapper2App.eventloop()
__all__=('SoundDbText','droid')
#by 乘着船 at https://www.bilibili.com/read/cv18422794