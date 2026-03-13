from .BaseWindow import *
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
        android:background="#ffffff"
		android:id="@+id/Title"
		android:layout_width="fill_parent"
		android:layout_height="wrap_content"
		android:textSize="8dp"
		android:text=""
		android:textColor="#ff0000"
		android:layout_weight="0"
		android:gravity="center"
	/>
	<EditText
        android:background="#ffffaf"
		android:id="@+id/Text"
		android:layout_width="fill_parent"
		android:layout_height="wrap_content"
		android:textSize="8dp"
		android:text=""
		android:textColor="#0000ff"
		android:layout_weight="0"
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
IV='''	<ImageView
		android:id="@+id/Image%s"
		android:layout_width="fill_parent"
		android:layout_height="0dp"
		android:layout_weight="1"
		android:adjustViewBounds="true"
        android:scaleType="fitXY"
	/>'''
class MainScreen(Layout):
    def on_show(self):
        v=self.views
        v.but_conf.add_event(click_EventHandler(self.views.but_conf,self.conf))
        v.but_copy.add_event(click_EventHandler(self.views.but_copy,self.copy))
        v.but_canc.add_event(click_EventHandler(self.views.but_canc,self.canc))
        v['Title'].text=self.Title
        v['Text'].text=self.Text
        c=self.Count
        i=self.Images
        for c in range(c):
            v['Image%s'%c].src=i[c]
    def on_close(self):
        pass
    def copy(self,view,dummy):
        droid.setClipboard(self.views.Text.text)
        droid.makeToast("文本已复制")
    def conf(self,view,dummy):
        MainScreen.Text=self.views.Text.text
        FullScreenWrapper2App.close_layout()
    def canc(self,view,dummy):
        MainScreen.Text=None
        FullScreenWrapper2App.close_layout()
def ImageText(Title='',Text='',Images='',button=CCC):#主函数
#图像长文本(标题,多行文本,图像文件名列表,(确认按钮文本,复制按钮文本,取消按钮文本))
    i=type(Images)
    if i==str:
        Images=[Images,]
    elif i==tuple:
        Images=list(Images)
    a=[XML[0]]
    for i in range(len(Images)):
        if Images[i].find('://')==-1:
            Images[i]='file://'+Images[i]
        a.append(IV%i)
    MainScreen.Images=Images
    MainScreen.Count=i+1
    MainScreen.Title=Title
    MainScreen.Text=Text
    a.append(XML[1]%button)
    FullScreenWrapper2App.show_layout(MainScreen('\n'.join(a)))
    FullScreenWrapper2App.eventloop()
    i=MainScreen.Text
    del MainScreen.Text,MainScreen.Title,MainScreen.Count,MainScreen.Images
    return i
__all__=('ImageText','droid')


#另，更改背景图片的方法：
#
#1.全Activity或大范围更改
#
#<LinearLayout
# android:background="file:///sdcard/……/xxx.jpg"
# #其他内容# >
#
#2.小控件更改
#
#<EditText
# android:background="file:///sdcard/……/xxx.jpg"
# #其他内容#
#/>