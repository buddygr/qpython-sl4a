from .BaseWindow import *
XML="""<?xml version="1.0" encoding="utf-8"?>
<LinearLayout
	android:layout_width="fill_parent"
	android:layout_height="fill_parent"
	android:background="#7f3faf"
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
	android:textSize="7dp"
	android:text="%s"
	android:background="#af7f3f"
	android:textColor="#ffffff"
	android:textStyle="bold"
	android:gravity="center"
	/>
    </ScrollView>
    <ListView
        android:id="@+id/listview"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:layout_weight="20"
        android:background="#7f3faf"
    />
    <Button
	android:layout_width="fill_parent"
	android:layout_height="50dp"
	android:text="%s"
	android:id="@+id/but_canc"
	android:textAllCaps="false"
	android:textSize="5dp"
	android:background="#3faf7f"
	android:textColor="#ffffff"
	android:layout_weight="1"
	android:gravity="center"/>
</LinearLayout>"""
class MainScreen(Layout):
    def on_show(self):
        v=self.views
        c=v.listview
        jsla('fullSetList',"listview",self.List,True)
        c.add_event(itemclick_EventHandler(c,self.conf))
        d=v.but_canc
        c=d.add_event
        c(click_EventHandler(d,self.canc))
        c(key_EventHandler('4',d,self.canc))
    def on_close(self):
        pass
    def conf(self,view,dummy):
        MainScreen.List=int(dummy['data']['position'])
        FullScreenWrapper2App.close_layout()
    def canc(self,view,dummy):
        MainScreen.List=None
        FullScreenWrapper2App.close_layout()
def ListCmdHtml(Title='',List=(),Cancel='取消'):#主函数
#彩色命令按钮组(标题,命令按钮彩色文本组,取消按钮文本)
    MainScreen.List=List
    FullScreenWrapper2App.show_layout(MainScreen(XML%(Str2Xml(Title),Cancel)))
    FullScreenWrapper2App.eventloop()
    List=MainScreen.List
    del MainScreen.List
    return List
__all__=('ListCmdHtml','droid')