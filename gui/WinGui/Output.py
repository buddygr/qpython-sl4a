from .BaseWindow import *
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
        self.views.but_conf.add_event(click_EventHandler(self.views.but_conf,self.conf))
        self.views.but_copy.add_event(click_EventHandler(self.views.but_copy,self.copy))
        self.views.but_canc.add_event(click_EventHandler(self.views.but_canc,self.canc))
        self.views.editNew.text=clbr(self.New)
        global First
        if First:
            self.views.editOld.text=First
            First=None
        else:
            self.views.editOld.text=clbr(self.Old)
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
First='上/蓝:最新输出\n下/红:历史输出\n这是标准输出窗口\n此提示只显示一次'
def Output(Content=''):#主函数
#输出窗体(内容str)
#不会自动换行
    MainScreen.New=Content
    FullScreenWrapper2App.show_layout(MainScreen(XML))
    FullScreenWrapper2App.eventloop()
__all__=('Output','droid')