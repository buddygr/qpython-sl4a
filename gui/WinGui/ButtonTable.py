from .BaseWindow import *
RB="""
<Button
    android:textAllCaps="false"
    android:id="@+id/Button_%s_%s"
    android:layout_width="fill_parent"
    android:layout_height="wrap_content"
    android:text="%s" />
"""
RW='\n<TableRow>\n','\n</TableRow>\n'
XML="""<?xml version="1.0" encoding="utf-8"?>
<LinearLayout
	android:layout_width="fill_parent"
	android:layout_height="fill_parent"
	android:background="#3f7faf"
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
		android:id="@+id/Title"
		android:layout_width="fill_parent"
		android:layout_height="wrap_content"
		android:textSize="9dp"
		android:text="%s"
		android:textColor="#ffff00"
		android:textStyle="bold"
		android:layout_weight="1"
		android:gravity="center"
	/>
	<HorizontalScrollView
        android:layout_width="fill_parent"   
        android:layout_height="wrap_content" >
	<TableLayout
        android:id="@+id/TableLayout"  
        android:layout_width="fill_parent"  
        android:layout_height="wrap_content"  
    >
""","""
    </TableLayout>
    </HorizontalScrollView>
	</LinearLayout>
	</ScrollView>
    </LinearLayout>
	<Button
		android:layout_width="fill_parent"
		android:layout_height="60dp"
		android:text="%s"
		android:id="@+id/but_canc"
		android:textSize="8dp"
		android:background="#007f00"
		android:textColor="#ffffff"
		android:layout_weight="1"
		android:gravity="center"/>
</LinearLayout>"""
class MainScreen(Layout):
    def on_show(self):
        v=self.views
        v.but_canc.add_event(click_EventHandler(v.but_canc,self.canc))
        def f(c):
            c=v[c]
            c.add_event(click_EventHandler(c,self.conf))
        n=self.Text
        for i in range(len(n)):
            m=n[i]
            if type(m)==str:
                f('Button_%s_'%i)
                continue
            for j in range(len(m)):
                f('Button_%s_%s'%(i,j))
    def on_close(self):
        pass
    def conf(self,view,dummy):
        a=dummy['data']['id'].split('_')
        try:
            b=int(a[1])
            a=int(a[2])
            b=b,a
        except:
            pass
        MainScreen.Text=b
        FullScreenWrapper2App.close_layout()
    def canc(self,view,dummy):
        MainScreen.Text=None
        FullScreenWrapper2App.close_layout()
Max=400#最大负载按钮数(手机性能不足时停止加载)
def ButtonTable(Title='',Buttons=(),Cancel='取消'):#主函数
#二维命令按钮组(标题,二维命令按钮文本组(一级按钮1,[二级按钮2.1,二级按钮2.2,…],一级按钮3,……),取消按钮文本)
#按“确认”返回：选择的Button的_行号/(行号,列号)
    o=0;i=-1
    r=[XML[0]%Str2Xml(Title)]
    for i in range(len(Buttons)):
        t=Buttons[i]
        if type(t)!=str:#type(t) is tuple,list
            r.append(RW[0])
            for j in range(len(t)):
                r.append(RB%(i,j,Str2Xml(t[j])))
            r.append(RW[1])
            o+=j+1
        else:
            r.append(RB%(i,'',Str2Xml(t)))
            o+=1
        if o>=Max and i<len(Buttons)-1:
            r.append('<TextView\nandroid:text="超载" />')
            Buttons=Buttons[:i+1]
            break
    MainScreen.Text=Buttons
    r.append(XML[1]%Cancel)
    r=''.join(r)
    FullScreenWrapper2App.show_layout(MainScreen(r))
    FullScreenWrapper2App.eventloop()
    r=MainScreen.Text
    del MainScreen.Text
    return r
__all__=('ButtonTable','droid')