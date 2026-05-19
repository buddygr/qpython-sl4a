from .BaseWindow import *
import sys,os
XML="""<?xml version="1.0" encoding="utf-8"?>
<LinearLayout
	android:layout_width="fill_parent"
	android:layout_height="fill_parent"
	android:background="#9f5f00"
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
    <EditText
        android:background="#ffffff"
		android:id="@+id/editNew"
		android:layout_width="fill_parent"
		android:layout_height="wrap_content"
		android:textSize="8dp"
		android:text=""
		android:textColor="#0000ff"
		android:layout_weight="1"
	/>
	<EditText
        android:background="#afffaf"
		android:id="@+id/editOld"
		android:layout_width="fill_parent"
		android:layout_height="wrap_content"
		android:textSize="8dp"
		android:text=""
		android:textColor="#ff0000"
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
	<Button
		android:layout_width="fill_parent"
		android:layout_height="fill_parent"
		android:text="继续(保留)"
		android:id="@+id/but_conf"
		android:background="#2f3f8f"
		android:textColor="#ffffffff"
		android:layout_weight="1"
		android:gravity="center"/>
	<Button
		android:layout_width="fill_parent"
		android:layout_height="fill_parent"
		android:text="复制"
		android:id="@+id/but_copy"
		android:background="#7f7f00"
		android:textColor="#ffffffff"
		android:layout_weight="1"
		android:gravity="center"/>
	<Button
		android:layout_width="fill_parent"
		android:layout_height="fill_parent"
		android:text="继续(清除)"
		android:id="@+id/but_canc"
		android:background="#6f1f6f"
		android:textColor="#ffffffff"
		android:layout_weight="1"
		android:gravity="center"/>
	</LinearLayout>
</LinearLayout>"""
class MainScreen(Layout):
    def on_show(self):
        global view
        view=self.views
        view.but_conf.add_event(click_EventHandler(view.but_conf,self.conf))
        view.but_copy.add_event(click_EventHandler(view.but_copy,self.copy))
        view.but_canc.add_event(click_EventHandler(view.but_canc,self.canc))
        view.editNew.html=clbr(self.New)
        global First
        if First:
            view.editOld.html=First
            First=None
        else:
            view.editOld.html=clbr(self.Old)
        MainScreen.Old=self.Old+self.New
        MainScreen.New=''
    def on_close(self):
        pass
    def copy(self,view,dummy):
        droid.setClipboard(self.Old)
        droid.makeToast("文本已复制")
    def conf(self,view,dummy):
        FullScreenWrapper2App.close_layout()
    def canc(self,view,dummy):
        MainScreen.Old=''
        FullScreenWrapper2App.close_layout()
    Old='';New=''
def clbr(x):
#去掉头尾空行
    t=True
    while t:
        t=False
        if x and x[0]=='\n':
            x=x[1:]
            t=True
        if x and x[-1]=='\n':
            x=x[:-1]
            t=True
    return x
First='<font color=blue>上/蓝:最新输出</font><br><font color=red>下/红:历史输出</font><br><font color=gray>这是标准输出窗口<br>此提示只显示一次</font>'
class out:
    buffer=[]
    def write(s):
        out.buffer.append(s)
        if out.HtmlMode:
            s=Htm2Txt(s)
        sys.__stdout__.write(s)
    flush=sys.__stdout__.flush
def Result2Html(s):
    s=str(s)
    t=[];a=t.append
    for i in s:
        j=ord(i)
        if j>255 or i.isalpha() or i.isdigit():
            a(i)
        elif j==10:
            a("<br>")
        elif j==32:
            a('&nbsp;')
        elif j==13:
            pass
        else:
            a('&#%s;'%j)
    return ''.join(t)
def Htm2Txt(s):
    t=[]
    l=len(s)
    a=b=0
    while True:
       a=s.find("<",b)
       if a==-1:
           t.append(s[b:])
           break
       t.append(s[b:a])
       b=s.find('>',a+1)
       b+=1
    return ''.join(t)
def OutCommand(Command='',Global=globals(),Local=locals(),HtmlMode=False):#副函数
#根据命令输出内容(命令,Html模式=否)
#不会自动换行
    import sys
    Out=sys.stdout
    sys.stdout=out
    out.HtmlMode=HtmlMode
    exec(Command,Global,Local)
    sys.stdout=Out
    text=''.join(out.buffer)
    out.buffer.clear()
    os.system('clear')
    OutHtml(text,HtmlMode)
def OutHtml(Content='',HtmlMode=True):#主函数
#输出内容(内容,Html模式=是)
#不会自动换行
    if not HtmlMode:
        Content=Result2Html(Content)
    MainScreen.New=Content
    FullScreenWrapper2App.show_layout(MainScreen(XML))
    FullScreenWrapper2App.eventloop()
__all__=('OutHtml','OutCommand','droid')