from .BaseWindow import *
XML="""<?xml version="1.0" encoding="utf-8"?>
<LinearLayout
	android:layout_width="fill_parent"
	android:layout_height="fill_parent"
	android:background="#007f7f"
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
        android:background="#afffff"
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
		android:text="%s"
		android:id="@+id/but_conf"
		android:textAllCaps="false"
		android:background="#3f3f7f"
		android:textColor="#ffffffff"
		android:layout_weight="1"
		android:gravity="center"/>
	<Button
		android:layout_width="fill_parent"
		android:layout_height="fill_parent"
		android:text="%s"
		android:id="@+id/but_copy"
		android:textAllCaps="false"
		android:background="#7f7f00"
		android:textColor="#ffffffff"
		android:layout_weight="1"
		android:gravity="center"/>
	<Button
		android:layout_width="fill_parent"
		android:layout_height="fill_parent"
		android:text="%s"
		android:id="@+id/but_canc"
		android:textAllCaps="false"
		android:background="#7f3f3f"
		android:textColor="#ffffffff"
		android:layout_weight="1"
		android:gravity="center"/>
	</LinearLayout>
</LinearLayout>"""
class MainScreen(Layout):
    def on_show(self):
        self.views.but_conf.add_event(click_EventHandler(self.views.but_conf,self.conf))
        self.views.but_copy.add_event(click_EventHandler(self.views.but_copy,self.copy))
        self.views.but_canc.add_event(click_EventHandler(self.views.but_canc,self.canc))
        self.views.editNew.text=clbr(self.New)
        self.views.editOld.text=clbr(self.Old)
    def on_close(self):
        pass
    def copy(self,view,dummy):
        s=''
        for i in self.copyOrder:
            if i=='n':
                s+=self.New
            elif i=='o':
                s+=self.Old
        droid.setClipboard(s)
        droid.makeToast("文本已复制")
    def conf(self,view,dummy):
        MainScreen.New=True
        FullScreenWrapper2App.close_layout()
    def canc(self,view,dummy):
        MainScreen.New=False
        FullScreenWrapper2App.close_layout()
def clbr(x):
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
def ynText(New='',Old='',button=YCN,copyOrder='no'):#主函数
#是否窗体(新内容,旧内容,("是"按钮文本,"复制"按钮文本,"否"按钮文本),复制顺序='no/on/n/o')
    MainScreen.New=New
    MainScreen.Old=Old
    MainScreen.copyOrder=copyOrder
    FullScreenWrapper2App.show_layout(MainScreen(XML%tuple(button)))
    FullScreenWrapper2App.eventloop()
    i=MainScreen.New
    del MainScreen.New,MainScreen.Old
    return i
__all__=('ynText','droid')