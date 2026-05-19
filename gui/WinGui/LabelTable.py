from .BaseWindow import *
RB='''<TextView
    android:background="#%s"
    android:text="%s" />'''
RW='\n<TableRow>\n','\n</TableRow>\n'
XML="""<?xml version="1.0" encoding="utf-8"?>
<LinearLayout
	android:layout_width="fill_parent"
	android:layout_height="fill_parent"
	
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
		android:textSize="7dp"
		android:text="%s"
		android:textColor="#007f00"
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
	<LinearLayout
		android:layout_width="fill_parent"
		android:layout_height="80dp"
		android:orientation="horizontal"
		android:layout_weight="8">
	<Button
		android:layout_width="fill_parent"
		android:layout_height="fill_parent"
		android:text="%s"
		android:id="@+id/but_copy"
		android:textSize="7dp"
		android:background="#7f0000"
		android:textColor="#ffffffff"
		android:layout_weight="1"
		android:gravity="center"/>
	<Button
		android:layout_width="fill_parent"
		android:layout_height="fill_parent"
		android:text="%s"
		android:id="@+id/but_canc"
		android:textSize="7dp"
		android:background="#007f00"
		android:textColor="#ffffffff"
		android:layout_weight="1"
		android:gravity="center"/>
	</LinearLayout>
</LinearLayout>"""
def Csv(s):
    if s.find('"')!=-1 or s.find(',')!=-1 or s.find('\n')!=-1:
        s='"'+s.replace('"','""')+'"'
    return s
class MainScreen(Layout):
    def on_show(self):
        v=self.views
        v.but_canc.add_event(click_EventHandler(v.but_canc,self.canc))
        v.but_copy.add_event(click_EventHandler(v.but_copy,self.copy))
    def on_close(self):
        pass
    def copy(self,view,dummy):
        s=[];t=s.append
        for a in self.Text:
            if type(a)==str:
                t(Csv(a))
                t('\n')
                continue
            for b in a:
                t(Csv(b))
                t(',')
            if a:
                s[-1]="\n"
        if self.Text:
            s.pop(-1)
        jsla('setClipboard',''.join(s))
        jsla('makeToast',"csv文本已复制")
    def canc(self,view,dummy):
        FullScreenWrapper2App.close_layout()
Max=800#最大负载按钮数(手机性能不足时停止加载)
def LabelTable(Title='',Texts=(),button=('复制','完成')):#主函数
#二维标签组(标题,二维文本组(一级文本1,[二级文本2.1,二级文本2.2,…],一级文本3,……),('复制'按钮文本,'完成'按钮文本))
    o=0;i=-1
    c1=('7f3f3f','007f7f'),('2f4f5f','7f007f')
    c2=('00007f','3f3f00')
    r=[XML[0]%Str2Xml(Title)]
    for i in range(len(Texts)):
        t=Texts[i]
        if type(t)!=str:#type(t) is tuple,list
            c=c1[i%2]
            r.append(RW[0])
            for j in range(len(t)):
                r.append(RB%(c[j%2],Str2Xml(t[j])))
            r.append(RW[1])
            o+=j+1
        else:
            r.append(RB%(c2[i%2],Str2Xml(t)))
            o+=1
        if o>=Max and i<len(Texts)-1:
            Texts=Texts[:i+1]
            r.append('<TextView\nandroid:text="超载" />')
            break
    MainScreen.Text=Texts
    r.append(XML[1]%button)
    r=''.join(r)
    FullScreenWrapper2App.show_layout(MainScreen(r))
    FullScreenWrapper2App.eventloop()
    del MainScreen.Text
    return None
__all__=('LabelTable','droid')