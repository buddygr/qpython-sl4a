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
		android:textSize="10dp"
		android:text="%s"
		android:background="#af7f3f"
		android:textColor="#ffffff"
		android:textStyle="bold"
		android:gravity="center"
	/>
	</ScrollView>
    <GridView
        android:id="@+id/listview"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:layout_weight="20"
        android:numColumns="%s"
    />
	<Button
		android:layout_width="fill_parent"
		android:layout_height="50dp"
		android:text="%s"
		android:id="@+id/but_canc"
		android:textSize="8dp"
		android:background="#3faf7f"
		android:textColor="#ffffff"
		android:layout_weight="1"
		android:gravity="center"/>
</LinearLayout>"""
class MainScreen(Layout):
    def on_show(self):
        v=self.views
        v.listview.set_listitems(self.List)
        v.listview.add_event(itemclick_EventHandler(v.listview,self.conf))
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
def GridCmd(Title='',List=(),numCols=2,Cancel='取消'):#主函数
#命令按钮组(标题,命令按钮文本组(按钮1,按钮2,……),每行按钮个数,取消按钮文本)
    MainScreen.List=List
    FullScreenWrapper2App.show_layout(MainScreen(XML%(Str2Xml(Title),numCols,Cancel)))
    FullScreenWrapper2App.eventloop()
    List=MainScreen.List
    del MainScreen.List
    return List
__all__=('GridCmd','droid')