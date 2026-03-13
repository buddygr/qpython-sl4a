from .BaseWindow import *
XML="""<?xml version="1.0" encoding="utf-8"?>
<LinearLayout
	android:layout_width="fill_parent"
	android:layout_height="fill_parent"
	android:background="#0E4200"
	android:orientation="vertical"
	xmlns:android="http://schemas.android.com/apk/res/android"
	xmlns:qpython="http://www.qpython.org">
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
		android:gravity="%s"
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
def getText(self):
    if MainScreen.ReturnHtml:
        return self.et.html
    else:
        i=self.et.text
        if MainScreen.ReturnHtml==None:
            return i
        else:
            return i.replace(chr(160),' ')
class MainScreen(Layout):
    def on_show(self):
        self.views.but_conf.add_event(click_EventHandler(self.views.but_conf,self.conf))
        self.views.but_copy.add_event(click_EventHandler(self.views.but_copy,self.copy))
        self.views.but_canc.add_event(click_EventHandler(self.views.but_canc,self.canc))
        self.et=self.views.editText
        if MainScreen.TitleHtml:
            self.views.editTitle.html=self.Title
        else:
            self.views.editTitle.text=self.Title
        if MainScreen.MessageHtml:
            self.et.html=self.Text
        else:
            self.et.text=self.Text
    def on_close(self):
        pass
    def copy(self,view,dummy):
        droid.setClipboard(getText(self))
        droid.makeToast("文本已复制")
    def conf(self,view,dummy):
        MainScreen.Text=getText(self)
        FullScreenWrapper2App.close_layout()
    def canc(self,view,dummy):
        try:
            if MainScreen.CancelConfirm and MainScreen.Text!=self.views.editText.text:
                jsla("dialogCreateAlert",'提示','文本已修改，不保存已修改内容?')
                jsla("dialogSetPositiveButtonText",'手滑了')
                jsla("dialogSetNeutralButtonText",'不保存')
                jsla('dialogShow')
                try:
                    i=rsla("dialogGetResponse")['which']
                except:
                    i=''
                if i!='neutral':
                    return
        except:
            from traceback import format_exc
            print(format_exc())
        MainScreen.Text=None
        FullScreenWrapper2App.close_layout()
def LongHtml(Title='',Message='',Button=CCC,**KW):#主函数
#KW包含：ReturnHtml=False，TitleHtml=True，MessageHtml=True，InputHtml=None，TitleGravity="center"，CancelConfirm=False
#彩色文本(标题,多行文本,(确认按钮文本,复制按钮文本,取消按钮文本))
#ReturnHtml：返回Html还是返回Text；ReturnHtml==True:结果返回Html；ReturnHtml==False:结果返回纯文本(空格ascii为32日常风格)；ReturnHtml==None:结果返回纯文本(空格ascii为160Html风格)
#TitleHtml：输入值Title是Html还是Text
#MessageHtml：输入值Message是Html还是Text
#InputHtml：两个输入值(Title,Message)是Html还是Text；默认值为None，表示具体分别由TitleHtml和MessageHtml决定；如果InputHtml为True或False，则TitleHtml和MessageHtml均失效
#TitleGravity：标题布局方式，值为"left","center","right"
#CancelConfirm：取消按钮是否进行放弃保存前提示
#例如：LongHtml('<font color=green>Hello</font><font color=blue>World</font>','<font color=red>你好</font><font color=green>世界</font>')
    MainScreen.Title=Title
    MainScreen.Text=Message
    MainScreen.ReturnHtml=KW.get("ReturnHtml",False)
    i=KW.get("InputHtml",None)
    if i==None:
        MainScreen.TitleHtml=KW.get("TitleHtml",True)
        MainScreen.MessageHtml=KW.get("MessageHtml",True)
    else:
        MainScreen.TitleHtml=MainScreen.MessageHtml=i
    MainScreen.CancelConfirm=KW.get("CancelConfirm",False)
    TitleGravity=KW.get("TitleGravity","center")
    FullScreenWrapper2App.show_layout(MainScreen(XML%(TitleGravity,*Button)))
    FullScreenWrapper2App.eventloop()
    i=MainScreen.Text
    del MainScreen.Title,MainScreen.Text
    return i
__all__=('LongHtml','droid')
#LongHtml by 乘着船 at 20241207