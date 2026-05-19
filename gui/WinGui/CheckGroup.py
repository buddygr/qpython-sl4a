from .BaseWindow import *
CB="""
<CheckBox
    android:id="@+id/Check%s"
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
""","""
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
	<Button
		android:layout_width="fill_parent"
		android:layout_height="fill_parent"
		android:text="加载中…"
		android:id="@+id/but_alno"
		android:textAllCaps="false"
		android:background="#3f3f3f"
		android:textColor="#ffffffff"
		android:layout_weight="1"
		android:gravity="center"/>
	</LinearLayout>
</LinearLayout>"""
def getCheck(self):
    r=rsla('fullGetProperties',tuple('Check%s'%i for i in self.Range),'checked')
    s=[];a=s.append;c=self.Check
    if c:
        for i in self.Range:
            if r[i]=='true':
                a(c[i])
    else:
        for i in self.Range:
            if r[i]=='true':
                a(i)
    return s
class MainScreen(Layout):
    def on_show(self):
        v=self.views
        v.but_alno.text=self.AlNo[0]
        v.but_conf.add_event(click_EventHandler(v.but_conf,self.conf))
        v.but_copy.add_event(click_EventHandler(v.but_copy,self.copy))
        v.but_alno.add_event(click_EventHandler(v.but_alno,self.alno))
        v.but_canc.add_event(click_EventHandler(v.but_canc,self.canc))
        if not MainScreen.DV:
            return
        for i in MainScreen.DV:
            jsla('fullSetProperty','Check%s'%i,'checked','true')
    def on_close(self):
        pass
    def copy(self,view,dummy):
        droid.setClipboard(str(getCheck(self)))
        droid.makeToast('文本已复制')
    def alno(self,view,dummy):
        v=self.views.but_alno
        if v.text==self.AlNo[0]:
            a=self.AlNo[1];b='true'
        else:
            a=self.AlNo[0];b='false'
        v.text=a
        jsla('fullSetProperties',tuple('Check%s'%i for i in self.Range),'checked',b)
    def conf(self,view,dummy):
        MainScreen.Text=getCheck(self)
        FullScreenWrapper2App.close_layout()
    def canc(self,view,dummy):
        MainScreen.Text=None
        FullScreenWrapper2App.close_layout()
rcColor=('7f3f3f','3f3f7f')
def CheckGroup(Title='',Check=(),returnValue=False,defaultValue=None,ycnButton=CCC,anButton=ALNO):#主函数
#复选按钮组(标题,复选按钮文本组(按钮1,按钮2,……),返回数值,默认值,(确认按钮文本,复制按钮文本,取消按钮文本),(全选按钮文本,全不选按钮文本))
#返回数值：False时返回数字，例如[0,2]；True时返回按钮文本，例如["文本1","文本3"]。
#默认值：不需要时填None，为全不选；需要时，填写需要勾选的序号列表，例如[0,2]
    r=[XML[0]%Str2Xml(Title)];i=-1
    for i in range(len(Check)):
        r.append(CB%(i,Str2Xml(Check[i]),rcColor[i%2]))
    MainScreen.Count=i+1
    MainScreen.Range=range(MainScreen.Count)
    if returnValue:
        MainScreen.Check=Check
    else:
        MainScreen.Check=False
    MainScreen.RV=returnValue
    MainScreen.DV=defaultValue
    r.append(XML[1]%tuple(ycnButton))
    r=''.join(r)
    MainScreen.AlNo=anButton
    FullScreenWrapper2App.show_layout(MainScreen(r))
    FullScreenWrapper2App.eventloop()
    r=MainScreen.Text
    del MainScreen.Text,MainScreen.AlNo
    return r
__all__=('CheckGroup','droid')