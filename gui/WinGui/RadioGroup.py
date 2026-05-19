from .BaseWindow import *
RB="""
<RadioButton
    android:id="@+id/Radio%s"
    android:layout_width="fill_parent"
    android:layout_height="wrap_content"
    android:textSize="8dp"
    android:text="%s"
    android:background="#%s"
/>
"""
XML="""<?xml version="1.0" encoding="utf-8"?>
<LinearLayout
	android:layout_width="fill_parent"
	android:layout_height="fill_parent"
	android:background="#4f3f2f"
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
		android:id="@+id/Title"
		android:layout_width="fill_parent"
		android:layout_height="wrap_content"
		android:textSize="8dp"
		android:text="%s"
		android:textColor="#ff0000"
		android:background="#ffffff"
		android:layout_weight="1"
		android:gravity="center"
	/>
    <RadioGroup
        android:id="@+id/RadioGroup"
        android:layout_width="fill_parent"
        android:layout_height="fill_parent"
        android:orientation="vertical">
""","""
    </RadioGroup>
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
def getRadio(self):
    if self.Choose==None:
        return None
    elif self.Radio:
        return self.Radio[self.Choose]
    else:
        return self.Choose
class MainScreen(Layout):
    def on_show(self):
        v=self.views
        for i in range(self.Count):
            c=v['Radio%s'%i]
            c.add_event(click_EventHandler(c,self.chng))
        self.Choose=None
        v.but_conf.add_event(click_EventHandler(v.but_conf,self.conf))
        v.but_copy.add_event(click_EventHandler(v.but_copy,self.copy))
        v.but_canc.add_event(click_EventHandler(v.but_canc,self.canc))
    def on_close(self):
        pass
    def chng(self,view,dummy):
        self.Choose=int(view.view_id[5:])
    def copy(self,view,dummy):
        droid.setClipboard(str(getRadio(self)))
        droid.makeToast("文本已复制")
    def conf(self,view,dummy):
        MainScreen.Text=getRadio(self)
        FullScreenWrapper2App.close_layout()
    def canc(self,view,dummy):
        MainScreen.Text=None
        FullScreenWrapper2App.close_layout()
rcColor=('7f3f3f','3f3f7f')
def RadioGroup(Title='',Radio=(),returnValue=False,button=CCC):#主函数
#单选按钮组(标题,单选按钮文本组(按钮1,按钮2,……),返回数值,(确认按钮文本,复制按钮文本,取消按钮文本))
    r=[XML[0]%Str2Xml(Title)];i=-1
    for i in range(len(Radio)):
        r.append(RB%(i,Str2Xml(Radio[i]),rcColor[i%2]))
    MainScreen.Count=i+1
    if returnValue:
        MainScreen.Radio=Radio
    else:
        MainScreen.Radio=False
    r.append(XML[1]%tuple(button))
    r=''.join(r)
    FullScreenWrapper2App.show_layout(MainScreen(r))
    FullScreenWrapper2App.eventloop()
    r=MainScreen.Text
    MainScreen.Text=True
    return r
__all__=('RadioGroup','droid')