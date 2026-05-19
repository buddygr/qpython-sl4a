from .BaseWindow import *
XML="""<?xml version="1.0" encoding="utf-8"?>
<LinearLayout
    android:layout_width="fill_parent"
    android:layout_height="fill_parent"
    android:background="#af7f3f"
    android:orientation="vertical"
    xmlns:android="http://schemas.android.com/apk/res/android">
	<ScrollView   
		android:layout_width="fill_parent"   
		android:layout_height="50dp"
		android:layout_weight="1" > 
	<TextView
		android:id="@+id/Title"
		android:layout_width="fill_parent"
		android:layout_height="wrap_content"
		android:textSize="10dp"
		android:text="%s"
		android:background="#af3f7f"
		android:textColor="#ffffff"
		android:textStyle="bold"
		android:gravity="center"
	/>
	</ScrollView>
	<ScrollView   
		android:layout_width="fill_parent"   
		android:layout_height="fill_parent"
		android:layout_weight="20" >
	<LinearLayout
		android:layout_width="fill_parent"
		android:layout_height="fill_parent"
		android:orientation="vertical" >""","""	</LinearLayout>
	</ScrollView>
	<LinearLayout
		android:layout_width="fill_parent"
		android:layout_height="50dp"
		android:orientation="horizontal"
		android:layout_weight="1" >
	<Button
		android:layout_width="fill_parent"
		android:layout_height="fill_parent"
		android:text="%s"
		android:id="@+id/but_conf"
		android:textAllCaps="false"
		android:background="#8faf2f"
		android:textColor="#ffffff"
		android:layout_weight="1"
		android:gravity="center"/>
	<Button
		android:layout_width="fill_parent"
		android:layout_height="fill_parent"
		android:text="%s"
		android:id="@+id/but_copy"
		android:textAllCaps="false"
		android:background="#7f3faf"
		android:textColor="#ffffff"
		android:layout_weight="1"
		android:gravity="center"/>
	<Button
		android:layout_width="fill_parent"
		android:layout_height="fill_parent"
		android:text="%s"
		android:id="@+id/but_canc"
		android:textAllCaps="false"
		android:background="#2faf8f"
		android:textColor="#ffffff"
		android:layout_weight="1"
		android:gravity="center"/>
	</LinearLayout>
</LinearLayout>"""
TV="""	<TextView
		android:layout_width="fill_parent"
		android:layout_height="wrap_content"
		android:textSize="9dp"
		android:text="%s"
		android:background="#afffff"
		android:textColor="#ff0000"
		android:gravity="center"
	/>"""
ET="""	<EditText
		android:id="@+id/edit%s"
		android:layout_width="fill_parent"
		android:layout_height="wrap_content"
		android:textSize="9dp"
		android:text="%s"
		android:background="#ffffaf"
		android:textColor="#0000ff"
	/>"""
SP="""	<Spinner
		android:id="@+id/spin%s"
		android:layout_width="match_parent"
		android:layout_height="40dp"
	/>"""
def getData(self):
    v=self.views
    L=self.List
    l=len(L)
    r=[];R=r.append
    V=self.returnValue
    textview=True
    for i in range(l):
        k=L[i]
        if type(k)==str:
            if textview:
                textview=False
            else:
                R(v['edit%s'%i].text)
                textview=True
        elif type(k)==int:
            continue
        else:
            i=int(v['spin%s'%i].selectedItemPosition)
            if V:
                i=k[i]
            R(i)
            textview=True
    return r
class MainScreen(Layout):
    def on_show(self):
        v=self.views
        L=self.List
        l=len(L)
        for i in range(l):
            k=L[i]
            if type(k)==str:
                continue
            elif type(k)==int:
                v['spin%s'%(i-1)].selection=str(k)
                continue
            c=v['spin%s'%i]
            c.set_listitems(k)
        d=v.but_canc
        c=d.add_event
        c(click_EventHandler(d,self.canc))
        c(key_EventHandler('4',d,self.canc))
        d=v.but_conf
        d.add_event(click_EventHandler(d,self.conf))
        d=v.but_copy
        d.add_event(click_EventHandler(d,self.copy))
    def on_close(self):
        pass
    def conf(self,view,dummy):
        MainScreen.List=getData(self)
        FullScreenWrapper2App.close_layout()
    def copy(self,view,dummy):
        rsla('setClipboard',str(getData(self)))
        rsla('makeToast','数据已复制')
    def canc(self,view,dummy):
        MainScreen.List=None
        FullScreenWrapper2App.close_layout()
def MenuGroup(Title='',MenuList=(),returnValue=False,button=CCC):#主函数
#菜单项目组(
#  标题,
#  多个菜单文本组(
#    菜单标题a0,
#    菜单a(
#      菜单项目a1,
#      菜单项目a2,
#      ……),
#    编辑框说明b0,
#    编辑框默认内容b,
#    菜单说明c0,
#    菜单c(
#      菜单项目c1,
#      菜单项目c2,
#      ……),
#    编辑框说明d0,
#    编辑框默认内容d,
#    ……),
#    菜单说明e0,
#    菜单e(
#      菜单项目e1,
#      菜单项目e2,
#      ……),
#    菜单默认位置e#,
#  返回数值,
#  底部按钮组(
#    确认按钮文本,
#    复制按钮文本,
#    取消按钮文本))
#
#MenuList连续输入单个字符串时：
#  不可编辑框->可编辑框->不可编辑框->可编辑框->……
#
#MenuList如果先输入一个/多个字符串/整数列表，再输单个字符串：
#  菜单列表->不可编辑框
#
#例子：print(MenuGroup('基本信息',['姓名','未知','性别',('男的','女的','未知性别'),2,'血型',('A','B','O','AB','未知血型'),4,'出生日期',list(range(1970,2024)),list(range(1,13)),list(range(1,32)),'学历',('无','大专','本科','硕士','博士'),'备注',''],True,('好的','拷贝','再想想')))
    MainScreen.List=MenuList
    MainScreen.returnValue=returnValue
    menuXml=[XML[0]%Str2Xml(Title)]
    a=menuXml.append
    l=len(MenuList)
    textview=True
    for i in range(l):
        k=MenuList[i]
        if type(k)==str:
            if textview:
                a(TV%Str2Xml(k))
                textview=False
            else:
                a(ET%(i,Str2Xml(k)))
                textview=True
        elif type(k)==int:
            continue
        else:
            a(SP%i)
            textview=True
    menuXml.append(XML[1]%tuple(button))
    FullScreenWrapper2App.show_layout(MainScreen('\n'.join(menuXml)))
    FullScreenWrapper2App.eventloop()
    List=MainScreen.List
    del MainScreen.List
    return List
__all__=('MenuGroup','droid')