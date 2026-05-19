#需要 QPython Plus >= 3.8.0
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
	<LinearLayout
		android:layout_width="fill_parent"
		android:layout_height="wrap_content"
		android:orientation="horizontal"
		android:layout_weight="1">
	<TextView
        android:background="#ffffff"
		android:id="@+id/SpdBear"
		android:layout_width="fill_parent"
		android:layout_height="fill_parent"
		android:textSize="10sp"
		android:text=""
		android:textColor="#ffffbf"
		android:background="@android:color/transparent"
		android:gravity="center"
		android:layout_weight="8"
		android:radius="10dp"
	/>
    <EditText
        android:background="#ffffaf"
		android:id="@+id/Title"
		android:layout_width="fill_parent"
		android:layout_height="wrap_content"
		android:textSize="8dp"
		android:text=""
		android:textColor="#ff0000"
		android:layout_weight="1"
		android:gravity="center"
	/>
	</LinearLayout>
	<EditText
        android:background="#ffffff"
		android:id="@+id/Text"
		android:layout_width="fill_parent"
		android:layout_height="wrap_content"
		android:textSize="8dp"
		android:text="正在获取位置信息"
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
	<RadioButton
		android:layout_width="fill_parent"
		android:layout_height="fill_parent"
		android:text="暂停"
		android:id="@+id/but_pause"
		android:textAllCaps="false"
		android:background="#007f7f"
		android:textColor="#ffffffff"
		android:layout_weight="1"
		android:gravity="center"/>
	<RadioButton
		android:layout_width="fill_parent"
		android:layout_height="fill_parent"
		android:text="复制"
		android:id="@+id/but_copy"
		android:textAllCaps="false"
		android:background="#7f7f00"
		android:textColor="#ffffffff"
		android:layout_weight="1"
		android:gravity="center"/>
	<RadioButton
		android:layout_width="fill_parent"
		android:layout_height="fill_parent"
		android:text="退出"
		android:id="@+id/but_exit"
		android:textAllCaps="false"
		android:background="#7f007f"
		android:textColor="#ffffffff"
		android:layout_weight="1"
		android:gravity="center"/>
	</LinearLayout>
</LinearLayout>"""
from time import time,localtime,strftime
def getAddrConti():
    jsla('startLocating',1000*timeInterval,1)
    t0=0
    while v.but_copy.checked=='false' and v.but_pause.checked=='false' and v.but_exit.checked=='false':
        t=time()
        if t-t0>=timeInterval:
            getAddrOnce()
            if timeInterval<0:
                #单次定位
                p=v.but_pause
                p.checked='true'
                p.text='继续'
            else:
                t0=t
def getAddrOnce():
    try:
        address = rsla('readLocation')
        if not address:
            address = rsla('getLastKnownLocation')
            fun = 'last'
        else:
            fun = 'read'
        if address == None:
            raise Exception('没有任何位置信息。')
        key='gps'
        location = address.get(key)
        if not location:
            key = tuple(address.keys())[0]
            location = address.get(key)
        try:
            address = rsla('geocode',location['latitude'],location['longitude'])[0]
        except:
            address = {}
        address['from'] = key + '/' + fun
        for i in 'country_name','admin_area','sub_admin_area','locality','sub_locality','feature_name':
            address.setdefault(i,'')
        address.update(location)
        rst=translate(address)
        T.text=rst
        if toFile:
            open(toFile,'a',encoding='utf-8').write(rst)
    except:
        from traceback import format_exc
        T.text='''
请打开QPython位置信息权限，
请打开系统定位功能；
请打开网络访问功能；

如果设置了ToFile参数，
请确保输出文件有效。

'''+format_exc()
        v.Title.text="错误信息"
        p=v.but_pause
        p.checked='true'
        p.text='继续'
def translate(Data):
    time=divmod(Data['time'],1000)
    time=strftime('%Y-%m-%d %H:%M:%S',localtime(time[0]))+str(time[1]/1000)[1:]
    Data['address']='  '.join((Data['country_name'],Data['admin_area'],Data['sub_admin_area'],Data['locality'],Data['sub_locality'],Data['feature_name']))
    i=Data['bearing']
    if Data['speed']>0:
        v.SpdBear.rotation=str(i-90)
        if i==0:
            v.SpdBear.textColor='#ff0000'
        else:
            v.SpdBear.textColor='#ffffbf'
        v.SpdBear.text='»'
    else:
        v.SpdBear.text=''
        v.SpdBear.rotation='0'
    return f"""
地点: {Data['address']}
纬度: {Data['latitude']}
经度: {Data['longitude']}
高度: {Data['altitude']}米
精度: {Data['accuracy']}米
速度: {Data['speed']}米/秒
速度: {Data['speed']*3.6}公里/小时
速度方位: {i}度\n  (见左上方,上北下南)
定位时间: {time}
定位来源：{Data['from']}

"""
def showInterval():
    if timeInterval<0:
        v.Title.text='单次(手动)定位'
    else:
        v.Title.text='连续(间隔%s秒)定位'%timeInterval
class MainScreen(Layout):
    def on_show(self):
        global v,T
        v=self.views
        T=v.Text
        v.but_pause.add_event(click_EventHandler(v.but_pause,self.pause))
        v.but_copy.add_event(click_EventHandler(v.but_copy,self.copy))
        v.but_exit.add_event(click_EventHandler(v.but_exit,self.exit))
        showInterval()
        getAddrConti()
    def on_close(self):
        pass
    def pause(self,view,dummy):
        p=v.but_pause
        p.checked='false'
        if p.text=='暂停':
            p.text='继续'
        else:
            p.text='暂停'
            showInterval()
            getAddrConti()
    def copy(self,view,dummy):
        jsla('setClipboard',T.text)
        v.but_copy.checked='false'
        jsla('makeToast','位置信息已复制')
        if v.but_pause.text=='暂停':
            getAddrConti()
    def exit(self,view,dummy):
        jsla('stopLocating')
        FullScreenWrapper2App.close_layout()
def LocationText(TimeInterval=1,ToFile=None):#主函数
#位置信息(时间间隔=1秒,导出文件=无)
#如果：时间间隔==-1，为单次(手动)定位
#如果：时间间隔>=0，为连续(自动)定位
    global timeInterval,toFile
    timeInterval=TimeInterval
    toFile=ToFile
    FullScreenWrapper2App.show_layout(MainScreen(XML))
    FullScreenWrapper2App.eventloop()
__all__=('LocationText','droid')
#by 乘着船 at https://www.bilibili.com/read/cv11339588