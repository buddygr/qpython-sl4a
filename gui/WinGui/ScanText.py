from .BaseWindow import *
ET="""
	<EditText
		android:id="@+id/Title%s"
		android:layout_width="fill_parent"
		android:layout_height="wrap_content"
		android:textSize="8dp"
		android:text="%s"
		android:textColor="#ff0000"
		android:background="#afffaf"
		android:layout_weight="1"
		android:gravity="center"
	/>""","""
	<EditText
        android:background="#ffffff"
		android:id="@+id/Text%s"
		android:layout_width="fill_parent"
		android:layout_height="wrap_content"
		android:textSize="8dp"
		android:text="%s"
		android:textColor="#0000ff"
		android:layout_weight="1"
	/>""","""
	<Button
        android:background="#cfcfff"
		android:id="@+id/Scan%s"
		android:layout_width="fill_parent"
		android:layout_height="wrap_content"
		android:textSize="8dp"
		android:text="%s"
		android:textColor="#7f7f00"
		android:layout_weight="1"
	/>"""
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
		android:id="@+id/supTitle"
		android:layout_width="fill_parent"
		android:layout_height="wrap_content"
		android:textSize="8dp"
		android:text="%s"
		android:textColor="#007f00"
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
	</LinearLayout>
</LinearLayout>"""
def getText():
    j=[]
    for i in range(len(Text)):
        j.append(Text[i].text)
    return j
class MainScreen(Layout):
    def on_show(self):
        global Text,v
        v=self.views
        Text=[]
        for i in range(self.Count):
            Text.append(v.pop('Text%s'%i))
            try:
                b=v['Scan%s'%i]
                b.add_event(click_EventHandler(b,self.scan))
            except:
                pass
        self.text=Text
        v.but_conf.add_event(click_EventHandler(v.but_conf,self.conf))
        v.but_copy.add_event(click_EventHandler(v.but_copy,self.copy))
        v.but_canc.add_event(click_EventHandler(v.but_canc,self.canc))
    def on_close(self):
        pass
    def copy(self,view,dummy):
        droid.setClipboard(str(getText()))
        droid.makeToast("文本已复制")
    def conf(self,view,dummy):
        MainScreen.Text=getText()
        FullScreenWrapper2App.close_layout()
    def scan(self,view,dummy):
        t=rsla('scanBarcode')
        if t!=None:
            Text[int(dummy['data']['id'][4:])].text=t
    def canc(self,view,dummy):
        MainScreen.Text=None
        FullScreenWrapper2App.close_layout()
def ScanText(supTitle='',Contents=(),button=CCC):#主函数
#多段文本(总标题,多段文本标题内容(标题1,(标题2,内容2),(标题3,条形码提示3,内容3),(标题4,内容4),标题5,(标题6,条形码提示6,内容6),……),(确认按钮文本,复制按钮文本,取消按钮文本))
    m=[XML[0]%Str2Xml(supTitle)]
    Contents=list(Contents)
    j=len(Contents)
    if j<1:
        Contents.append('')
        j=1
    for i in range(j):
        j=Contents[i]
        if type(j)!=str:
            l=len(j)
            if l==2:
                j=ET[0]%(i,Str2Xml(j[0]))+ET[1]%(i,Str2Xml(j[1]))
            elif l==3:
                j=ET[0]%(i,Str2Xml(j[0]))+ET[2]%(i,Str2Xml(j[1]))+ET[1]%(i,Str2Xml(j[2]))
        else:
            j=ET[0]%(i,Str2Xml(j))+ET[1]%(i,'')
        m.append(j)
    m.append(XML[1]%tuple(button))
    m=''.join(m)
    MainScreen.Count=i+1
    FullScreenWrapper2App.show_layout(MainScreen(m))
    FullScreenWrapper2App.eventloop()
    m=MainScreen.Text
    del MainScreen.Text,MainScreen.Count
    return m
__all__=('ScanText','droid')