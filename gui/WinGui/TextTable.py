from .BaseWindow import *
RB="""
<EditText
    android:id="@+id/Text_%s_%s"
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
    <EditText
		android:id="@+id/Title"
		android:layout_width="fill_parent"
		android:layout_height="wrap_content"
		android:textSize="9dp"
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
		android:layout_height="100dp"
		android:orientation="horizontal"
		android:layout_weight="8">
	<Button
		android:layout_width="fill_parent"
		android:layout_height="fill_parent"
		android:text="%s"
		android:id="@+id/but_conf"
		android:textSize="8dp"
		android:background="#007f7f"
		android:textColor="#ffffffff"
		android:layout_weight="1"
		android:gravity="center"/>
	<Button
		android:layout_width="fill_parent"
		android:layout_height="fill_parent"
		android:text="%s"
		android:id="@+id/but_copy"
		android:textSize="8dp"
		android:background="#7f7f00"
		android:textColor="#ffffffff"
		android:layout_weight="1"
		android:gravity="center"/>
	<Button
		android:layout_width="fill_parent"
		android:layout_height="fill_parent"
		android:text="%s"
		android:id="@+id/but_canc"
		android:textSize="8dp"
		android:background="#7f007f"
		android:textColor="#ffffffff"
		android:layout_weight="1"
		android:gravity="center"/>
	</LinearLayout>
</LinearLayout>"""
def getText(self):
    t=self.Text;d=[]
    for i in range(len(t)):
        s=t[i]
        if type(s)!=list:
            d.append(s.text)
            continue
        c=[]
        for j in range(len(s)):
            c.append(s[j].text)
        d.append(c)
    return d
def Csv(s):
    if s.find('"')!=-1 or s.find(',')!=-1 or s.find('\n')!=-1:
        s='"'+s.replace('"','""')+'"'
    return s
class MainScreen(Layout):
    def on_show(self):
        v=self.views
        v.but_conf.add_event(click_EventHandler(v.but_conf,self.conf))
        v.but_canc.add_event(click_EventHandler(v.but_canc,self.canc))
        v.but_copy.add_event(click_EventHandler(v.but_copy,self.copy))
        d=[];t=self.Text
        for i in range(len(t)):
            e=t[i]
            if type(e)==str:
                d.append(v.pop('Text_%s_'%i))
                continue
            c=[]
            for j in range(len(e)):
                c.append(v.pop('Text_%s_%s'%(i,j)))
            d.append(c)
        MainScreen.Text=d
    def on_close(self):
        pass
    def copy(self,view,dummy):
        r=getText(self)
        s=[];t=s.append
        for a in r:
            if type(a)==str:
                t(Csv(a))
                t('\n')
                continue
            for b in a:
                t(Csv(b))
                t(',')
            if a:
                s[-1]="\n"
        if r:
            s.pop(-1)
        jsla('setClipboard',''.join(s))
        jsla('makeToast',"csv文本已复制")
    def conf(self,view,dummy):
        MainScreen.Text=getText(self)
        FullScreenWrapper2App.close_layout()
    def canc(self,view,dummy):
        MainScreen.Text=None
        FullScreenWrapper2App.close_layout()
Max=400#最大负载按钮数(手机性能不足时停止加载)
def TextTable(Title='',Texts=(),button=('确认','复制','取消')):#主函数
#二维文本框组(标题,二维文本组(一级文本1,[二级文本2.1,二级文本2.2,…],一级文本3,……),('确认'按钮文本,'复制'按钮文本,'取消'按钮文本))
#按“确认”返回：修改后的Texts
    o=0;i=-1
    r=[XML[0]%Str2Xml(Title)]
    for i in range(len(Texts)):
        t=Texts[i]
        if type(t)!=str:#type(t) is tuple,list
            r.append(RW[0])
            for j in range(len(t)):
                r.append(RB%(i,j,Str2Xml(t[j])))
            r.append(RW[1])
            o+=j+1
        else:
            r.append(RB%(i,'',Str2Xml(t)))
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
    r=MainScreen.Text
    del MainScreen.Text
    return r
__all__=('TextTable','droid')