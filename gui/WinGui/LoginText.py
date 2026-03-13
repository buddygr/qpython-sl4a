from .BaseWindow import *
ET="""
<EditText
    android:id="@+id/Title%s"
    android:layout_width="fill_parent"
    android:layout_height="wrap_content"
    android:textSize="8dp"
    android:text="%s"
    android:textColor="#007f00"
    android:background="#%s"
    android:layout_weight="1"
    android:gravity="center"
	/>
<EditText
    android:background="#ffffff"
    android:id="@+id/Text%s"
    android:layout_width="fill_parent"
    android:layout_height="wrap_content"
    android:textSize="8dp"
    android:text="%s"
    android:textColor="#0000ff"
    android:layout_weight="1"
    %s
	/>
"""
PS='android:inputType="textPassword"'
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
    android:textColor="#ff0000"
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
        v=self.views
        Text={}
        for i in self.Contain:
            Text[i]=v.pop('Text%s'%i)
        self.text=Text
        v.but_conf.add_event(click_EventHandler(v.but_conf,self.conf))
        v.but_canc.add_event(click_EventHandler(v.but_canc,self.canc))
    def on_close(self):
        pass
    def conf(self,view,dummy):
        t=self.text
        j={}
        for i in self.Contain:
            j[i]=t[i].text
        MainScreen.Text=j
        FullScreenWrapper2App.close_layout()
    def canc(self,view,dummy):
        MainScreen.Text=None
        FullScreenWrapper2App.close_layout()
CC=('确认','取消')
UP={0:'用户名',1:'密码',2:'重复密码'}
def LoginText(Title='登录',Items=UP,button=CC):#主函数
#登录窗口_用户名密码(标题,项目组,("确认"按钮文本,"取消"按钮文本))
#项目组格式1：{0:"用户名"提示文本,1:"首次密码"提示文本,2:"二次密码"提示文本,3:"三次密码"提示文本,……}
#按“确认”返回：{0:用户名,1:首次密码,2:二次密码,3:三次密码,……}
#项目组格式2：{……,-2:("二级用户名"提示文本,"二级用户名"默认值),-1:("初级用户名"提示文本,"初级用户名"默认值),1:"首次密码"提示文本,2:"二次密码"提示文本,……}
#按“确认”返回：{……,-2:二级用户名,-1:初级用户名,1:首次密码,2:二次密码,……}
    m=[XML[0]%Str2Xml(Title)]
    MainScreen.Contain=d=list(Items)
    d.sort()#按照键值自动排序
    for i in d:
        try:
            c=Items[i]
        except:
            continue
        if i<=0:#明文区
            k=''
            y='cfcfff'
            if type(c)!=str:
                j=Str2Xml(c[1])
                c=Str2Xml(c[0])
            else:
                j=''
                c=Str2Xml(c)
        else:#密码区:i>0
            k=PS
            y='ffcfcf'
            j=''
            c=Str2Xml(c)
        m.append(ET%(i,c,y,i,j,k))
    m.append(XML[1]%tuple(button))
    m=''.join(m)
    FullScreenWrapper2App.show_layout(MainScreen(m))
    FullScreenWrapper2App.eventloop()
    m=MainScreen.Text
    del MainScreen.Text,MainScreen.Contain
    return m
__all__=('LoginText','droid')