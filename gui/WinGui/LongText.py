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
    <EditText
        android:background="#ffffaf"
		android:id="@+id/editTitle"
		android:layout_width="fill_parent"
		android:layout_height="wrap_content"
		android:textSize="8dp"
		android:text=""
		android:textColor="#ff0000"
		android:layout_weight="1"
		android:gravity="center"
	/>
	<EditText
        android:background="#ffffff"
		android:id="@+id/editText"
		android:layout_width="fill_parent"
		android:layout_height="wrap_content"
		android:textSize="8dp"
		android:text=""
		android:textColor="#0000ff"
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
		android:background="#007f7f"
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
		android:background="#7f007f"
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
        self.views.editText.text=self.Message
        self.views.editTitle.text=self.Title
    def on_close(self):
        pass
    def copy(self,view,dummy):
        droid.setClipboard(self.views.editText.text)
        droid.makeToast("文本已复制")
    def conf(self,view,dummy):
        MainScreen.Message=self.views.editText.text
        FullScreenWrapper2App.close_layout()
    def canc(self,view,dummy):
        MainScreen.Message=None
        FullScreenWrapper2App.close_layout()
def LongText(Title='',Message='',Button=CCC):#主函数
#长文本(标题,多行文本,(确认按钮文本,复制按钮文本,取消按钮文本))
#替代系统输入函数:input=LongText
    MainScreen.Title=Title
    MainScreen.Message=Message
    FullScreenWrapper2App.show_layout(MainScreen(XML%tuple(Button)))
    FullScreenWrapper2App.eventloop()
    i=MainScreen.Message
    del MainScreen.Title,MainScreen.Message
    return i
__all__=('LongText','droid')
#LongText by 乘着船