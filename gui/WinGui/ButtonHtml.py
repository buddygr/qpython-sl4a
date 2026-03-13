from .BaseWindow import *
#Button的textAllCaps=false，解决英文字母自动全大写问题
BT="""
    <Button
        android:textAllCaps="false"
		android:layout_width="fill_parent"
		android:layout_height="fill_parent"
		android:text="%s"
		android:id="@+id/but_yes"
		android:background="#3f3f7f"
		android:textColor="#ffffffff"
		android:layout_weight="1"
		android:gravity="center"/>
""","""
	<Button
        android:textAllCaps="false"
		android:layout_width="fill_parent"
		android:layout_height="fill_parent"
		android:text="%s"
		android:id="@+id/but_can"
		android:background="#7f3f3f"
		android:textColor="#ffffffff"
		android:layout_weight="1"
		android:gravity="center"/>
""","""
	<Button
        android:textAllCaps="false"
		android:layout_width="fill_parent"
		android:layout_height="fill_parent"
		android:text="%s"
		android:id="@+id/but_noo"
		android:background="#7f7f00"
		android:textColor="#ffffffff"
		android:layout_weight="1"
		android:gravity="center"/>
"""
XML="""<?xml version="1.0" encoding="utf-8"?>
<LinearLayout
	android:layout_width="fill_parent"
	android:layout_height="fill_parent"
	android:background="#007f7f"
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
		android:text=""
		android:textColor="#0000ff"
		android:background="#ffffaf"
		android:layout_weight="1"
		android:gravity="center"
	/>
	<EditText
		android:id="@+id/Text"
		android:layout_width="fill_parent"
		android:layout_height="wrap_content"
		android:textSize="8dp"
		android:text=""
		android:textColor="#ff0000"
		android:background="#ffffff"
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
""","""
	</LinearLayout>
</LinearLayout>"""
class MainScreen(Layout):
    def on_show(self):
        #if self.Count>=0:
        self.views.but_yes.add_event(click_EventHandler(self.views.but_yes,self.yes))
        if self.Count>1:
            self.views.but_noo.add_event(click_EventHandler(self.views.but_noo,self.noo))
        if self.Count>2:
            self.views.but_can.add_event(click_EventHandler(self.views.but_can,self.can))
        self.views.Title.html=self.Title
        self.views.Text.html=self.Text
    def on_close(self):
        pass
    def yes(self,view,dummy):
        MainScreen.Text=1
        FullScreenWrapper2App.close_layout()
    def noo(self,view,dummy):
        MainScreen.Text=-1
        FullScreenWrapper2App.close_layout()
    def can(self,view,dummy):
        MainScreen.Text=0
        FullScreenWrapper2App.close_layout()
YNC=('是','否','取消')
def ButtonHtml(TitleHtml='',TextHtml='',button=YNC):#主函数
#三按钮对话框(标题,内容,("是"按钮文本,"否"按钮文本,"取消"按钮文本))
    MainScreen.Title=TitleHtml
    MainScreen.Text=TextHtml
    b=[XML[0]]
    MainScreen.Count=l=len(button)
    if l==3:
        a=(button[0],button[2],button[1])
    elif l==2:
        a=(button[0],'',button[1])
    elif l==1:
        a=(button[0],'','')
    else:#l==0
        a=('OK','','')
    for i in range(3):
        if a[i]:
            b.append(BT[i]%a[i])
    b.append(XML[1])
    b=''.join(b)
    FullScreenWrapper2App.show_layout(MainScreen(b))
    FullScreenWrapper2App.eventloop()
    b=MainScreen.Text
    del MainScreen.Title,MainScreen.Text,MainScreen.Count
    return b
__all__=('ButtonHtml','droid')