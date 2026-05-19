from .BaseWindow import *
TI="""
	<EditText
		android:id="@+id/Title%s"
		android:layout_width="fill_parent"
		android:layout_height="wrap_content"
		android:textSize="8dp"
		android:text="%s"
		android:textColor="#ff0000"
		android:background="#afffaf"
		android:gravity="center"
	/>"""
TE="""
	<EditText
        android:background="#ffffaf"
		android:id="@+id/Text%s"
		android:layout_width="fill_parent"
		android:layout_height="wrap_content"
		android:textSize="8dp"
		android:text="%s"
		android:textColor="#0000ff"
	/>"""
SE="""
    <LinearLayout
	    android:layout_width="fill_parent"
    	android:layout_height="wrap_content"
    	android:orientation="vertical"
    	android:background="#ffcfcf" >
	<SeekBar
		android:id="@+id/Seek%s"
		android:layout_width="fill_parent"
		android:layout_height="wrap_content"
		android:layout_marginLeft="10dp"
		android:layout_marginRight="10dp"
		android:progress="%s"
		android:max="%s"
		android:progressColor="#%s"
	/>
	<TextView
		android:id="@+id/Posi%s"
		android:layout_width="fill_parent"
		android:layout_height="wrap_content"
		android:textSize="8dp"
		android:text="%s"
		android:textColor="#0000ff"
	/>
	</LinearLayout>
	"""
XML="""<?xml version="1.0" encoding="utf-8"?>
<LinearLayout
	android:layout_width="fill_parent"
	android:layout_height="fill_parent"
	android:background="#28285f"
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
        android:background="#cfcfff"
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
	<TextView
		android:layout_width="fill_parent"
		android:layout_height="wrap_content"
		android:textSize="8dp"
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
def getText(self):
    t=self.text
    j=[]
    for i in range(self.Count):
        c=contents[i]
        if type(c)==str:
            i=t[i].text
        else:
            i=int(t[i].progress)
            if len(c)>2:
                i=c[2](i)
        j.append(i)
    return j
class MainScreen(Layout):
    def on_show(self):
        global v
        v=self.views
        Text=[]
        for i in range(self.Count):
            if type(contents[i])==str:
                j=v.pop('Text%s'%i)
            else:
                j=v['Seek%s'%i]
                j.add_event(itemclick_EventHandler(j,self.drag))
            Text.append(j)
        self.text=Text
        v.but_conf.add_event(click_EventHandler(v.but_conf,self.conf))
        v.but_copy.add_event(click_EventHandler(v.but_copy,self.copy))
        v.but_canc.add_event(click_EventHandler(v.but_canc,self.canc))
    def on_close(self):
        pass
    def copy(self,view,dummy):
        droid.setClipboard(str(getText(self)))
        droid.makeToast("文本已复制")
    def drag(self,view,dummy):
        data=dummy['data']
        num=int(data['id'][4:])
        content=contents[num]
        progress=int(data['progress'])
        if len(content)>2:
            f=content[2]
            fProgress=f(progress)
            text='%s  %s'%(fProgress,f.range)
        else:
            max=content[1]
            percent=round(100*progress/max,1)
            text='%s/%s  %s%%'%(progress,max,percent)
        v['Posi%s'%num].text=text
    def conf(self,view,dummy):
        MainScreen.Text=getText(self)
        FullScreenWrapper2App.close_layout()
    def canc(self,view,dummy):
        MainScreen.Text=None
        FullScreenWrapper2App.close_layout()
seColor='f00','0f0','00f'
def MultSeek(supTitle='',Contents=(),button=CCC):#主函数
#按钮文本组=(确认按钮文本,复制按钮文本,取消按钮文本)
#多段文本(总标题,多段文本标题内容(标题1,内容文本1,标题2,内容文本2,……),按钮文本组)
#多段进度(总标题,多段进度标题内容(标题1,最大进度1,标题2,最大进度2,……),按钮文本组)
#多段进度(总标题,多段进度标题内容(标题1,(当前进度1,最大进度1),标题2,(当前进度2,最大进度2),……),按钮文本组)
#多段函数进度(总标题,多段函数进度标题内容(标题1,(当前进度1,最大进度1,换算函数1),标题2,(当前进度2,最大进度2,换算函数2),……),按钮文本组)
#多段{文本+进度+函数进度}(总标题,多段{文本+进度+函数进度}标题内容(标题1,内容文本1,标题2,最大进度2,标题3,(当前进度3,最大进度3),标题4,(当前进度4,最大进度4,换算函数4),……),按钮文本组)
#举例:print(MultSeek('考试成绩调查',('姓名','XXX','性别',(1,2,lambda x:'男？女'[x]),'出生年',(73,100,lambda x:x+1922),'出生月',(0,11,lambda x:x+1),'出生日',(0,30,lambda x:x+1),'身高(cm)',(160,200),'体重(kg)',(50,100),'考试成绩',150),('好的','复制','再想想')))
    global contents
    m=[XML[0]%Str2Xml(supTitle)]
    contents=[]
    Contents=list(Contents)
    j=len(Contents)
    if j<1:
        Contents.append('')
        j=1
    if j%2:
        Contents.append('')
    for i in range(0,j,2):
        k=i>>1
        g=Contents[i+1]
        h=type(g)
        if h==str:
            h=TE%(k,Str2Xml(g))
        else:
            if h==int:
                h='0/%s  0%%'%g
                g=0,g
            elif len(g)==2:
                h='%s/%s  %s%%'%(g[0],g[1],round(100*g[0]/g[1],1))
            else:
                f=g[2];f.min=f(0);f.max=f(g[1])
                f.range='(%s~%s)'%(f.min,f.max)
                h='%s  %s'%(f(g[0]),f.range)
            h=SE%(k,g[0],g[1],seColor[k%3],k,h)
        contents.append(g)
        g=TI%(k,Str2Xml(Contents[i]))
        m.append(g+h)
    m.append(XML[1]%tuple(button))
    m=''.join(m)
    MainScreen.Count=k+1
    FullScreenWrapper2App.show_layout(MainScreen(m))
    FullScreenWrapper2App.eventloop()
    m=MainScreen.Text
    del MainScreen.Text,MainScreen.Count
    return m
__all__=('MultSeek','droid')