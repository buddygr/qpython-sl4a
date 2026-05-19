#需要QPython Plus 3.8.1或以上，旧版QPython均无法正常运行
from .BaseWindow import *
from os import listdir,environ
from os.path import isdir,realpath
XML="""<?xml version="1.0" encoding="utf-8"?>
<LinearLayout
	android:layout_width="fill_parent"
	android:layout_height="fill_parent"
	android:background="#3faf7f"
	android:orientation="vertical"
	xmlns:android="http://schemas.android.com/apk/res/android">
	<LinearLayout
		android:layout_width="fill_parent"
		android:layout_height="fill_parent"
		android:orientation="vertical"
		android:layout_weight="20">
    <TextView
		android:id="@+id/Title"
		android:layout_width="fill_parent"
		android:layout_height="wrap_content"
		android:textSize="9dp"
		android:text="%s"
		android:textColor="#ffffff"
		android:textStyle="bold"
		android:layout_weight="1"
		android:gravity="center"
		android:background="#3faf7f"
	/>
	<TextView
		android:layout_width="fill_parent"
		android:layout_height="wrap_content"
		android:textSize="6dp"
		android:text="当前文件夹路径：%s"
		android:textColor="#ffffff"
		android:layout_weight="1"
		android:background="#3faf7f"/>
    <ListView
        android:id="@+id/listview"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:layout_weight="20"
        android:background="#3faf7f"
    />
    </LinearLayout>
    <LinearLayout
		android:layout_width="fill_parent"
		android:layout_height="160dp"
		android:orientation="vertical"
		android:layout_weight="10">	
    <LinearLayout
		android:layout_width="fill_parent"
		android:layout_height="fill_parent"
		android:orientation="horizontal"
		android:layout_weight="8">
    <TextView
		android:layout_width="wrap_content"
		android:layout_height="fill_parent"
		android:textSize="6dp"
		android:text="文件名"
		android:textColor="#ffffff"
		android:background="#af3f3f"
		android:layout_weight="1"
	/>
    <EditText
		android:id="@+id/FileName"
		android:layout_width="fill_parent"
		android:layout_height="fill_parent"
		android:textSize="6dp"
		android:text="%s"
		android:textColor="#0000ff"
		android:layout_weight="4"
		android:background="#ffffff"
	/>
	</LinearLayout>
    <LinearLayout
		android:layout_width="fill_parent"
		android:layout_height="fill_parent"
		android:orientation="horizontal"
		android:layout_weight="8">
	<Button
		android:layout_width="fill_parent"
		android:layout_height="fill_parent"
		android:text="确认"
		android:id="@+id/but_conf"
		android:textSize="6dp"
		android:background="#3f7faf"
		android:textColor="#ffffff"
		android:layout_weight="1"
		android:gravity="center"/>
	<Button
		android:layout_width="fill_parent"
		android:layout_height="fill_parent"
		android:text="向上"
		android:id="@+id/but_uppt"
		android:textSize="6dp"
		android:background="#6f1f00"
		android:textColor="#ffffff"
		android:layout_weight="1"
		android:gravity="center"/>
	<Button
		android:layout_width="fill_parent"
		android:layout_height="fill_parent"
		android:text="初始"
		android:id="@+id/but_strt"
		android:textSize="6dp"
		android:background="#2f005f"
		android:textColor="#ffffff"
		android:layout_weight="1"
		android:gravity="center"/>
	<Button
		android:layout_width="fill_parent"
		android:layout_height="fill_parent"
		android:text="取消"
		android:id="@+id/but_canc"
		android:textSize="6dp"
		android:background="#4f3f00"
		android:textColor="#ffffff"
		android:layout_weight="1"
		android:gravity="center"/>
	</LinearLayout>
    </LinearLayout>
</LinearLayout>"""
class MainScreen(Layout):
    def on_show(self):
        v=self.views
        v.listview.set_listitems(self.List)
        v.listview.add_event(itemclick_EventHandler(v.listview,self.clck))
        v.but_conf.add_event(click_EventHandler(v.but_conf,self.conf))
        v.but_canc.add_event(click_EventHandler(v.but_canc,self.canc))
        v.but_uppt.add_event(click_EventHandler(v.but_uppt,self.uppt))
        v.but_strt.add_event(click_EventHandler(v.but_strt,self.strt))
    def on_close(self):
        pass
    def clck(self,view,dummy):
        x=int(dummy['data']['position'])
        if x<self.DirCount:
            d=self.Dir[x]
            MainScreen.Path=(d,self.views.FileName.text)
        else:
            d=self.File[x-self.DirCount]
            x=d.rfind('/')
            if x>=0:
                d=d[x+1:]
            MainScreen.Path=(MainScreen.Path,d)
        FullScreenWrapper2App.close_layout()
    def conf(self,view,dummy):
        MainScreen.Path=self.Path+self.views.FileName.text
        FullScreenWrapper2App.close_layout()
    def uppt(self,view,dummy):
        MainScreen.Path=(PathUp(self.Path),self.views.FileName.text)
        FullScreenWrapper2App.close_layout()
    def canc(self,view,dummy):
        MainScreen.Path=None
        FullScreenWrapper2App.close_layout()
    def strt(self,view,dummy):
        MainScreen.Path=(MainScreen.sPath,self.views.FileName.text)
        FullScreenWrapper2App.close_layout()
EMU='/storage/emulated/'
SD=realpath('/sdcard')
defaultRoot={EMU:SD+'/'}
try:
    if int(environ['ANDROID_SDK'])>=30:
        raise
    defaultRoot['/']='/storage/'
except:
    defaultRoot['/']='/'
defaultRoot['']=defaultRoot['/']
def ListFile(Title='选择一个文件(夹)',Path=SD,FileName=''):#主函数
#文件(夹)选择器(标题,初始路径,初始文件名)
    MainScreen.sPath=d=MainScreen.Path=PathStrip(Path)
    while True:
        try:
            l=listdir(d)
        except:
            i=defaultRoot.copy()
            i=i.get(d)
            if i==None:
                l=[]
            elif i=='/':
                l=rsla('getSdCardPaths')
                for i in range(len(l)):
                    l[i]=l[i][1:]
                d='/'
            else:
                l=listdir(i)
                MainScreen.Path=d=i
        MainScreen.Dir=D=[]
        MainScreen.File=F=[]
        l.sort()
        for i in l:
            j=d+i
            if isdir(j):
                D.append(j+'/')
            else:
                F.append(j)
        MainScreen.List=b=[]
        for i in D:
            b.append(i.rsplit('/',2)[-2]+':目录')
        for i in F:
            b.append(i.rsplit('/',1)[-1]+':文件')
        MainScreen.Count=len(b)
        MainScreen.DirCount=len(D)
        r=XML%(Str2Xml(Title),Str2Xml(d),Str2Xml(FileName))
        FullScreenWrapper2App.show_layout(MainScreen(r))
        FullScreenWrapper2App.eventloop()
        d=MainScreen.Path
        if d==None:
            return
        elif type(d)!=tuple:
            return d
        d,FileName=d
        MainScreen.Path=d
def PathUp(x):
    y=x.rfind('/',0,-1)
    y=x[:y+1]
    if y==EMU:
        y=defaultRoot['']
    return y
def PathStrip(Path):
    Path=Path.strip()
    if Path[-1:]!='/':
        Path+='/'
    return Path
__all__=('ListFile','droid')