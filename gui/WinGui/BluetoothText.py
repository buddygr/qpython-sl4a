#需要 QPython Plus v3.8.3 或以上
from .BaseWindow import *
from time import strftime,localtime,time
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
    <TextView
        android:background="#ffffaf"
		android:id="@+id/Title"
		android:layout_width="fill_parent"
		android:layout_height="wrap_content"
		android:textSize="6dp"
		android:text=""
		android:textColor="#ff0000"
		android:layout_weight="1"
		android:gravity="center"
	/>
	<EditText
        android:background="#ffffff"
		android:id="@+id/Text"
		android:layout_width="fill_parent"
		android:layout_height="wrap_content"
		android:textSize="6dp"
		android:text="正在获取蓝牙设备，请打开蓝牙"
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
def getBluetoothConti():
    t0=0
    jsla('bluetoothDiscoveryStart')
    jsla('bluetoothGetBondedDevicesRssi',timeInterval*900)
    v.Text.enabled='false'
    while v.but_copy.checked=='false' and v.but_pause.checked=='false' and v.but_exit.checked=='false':
        t=time()
        if t-t0>=timeInterval:
            getBluetoothOnce()
            if timeInterval<0:
                #单次测试
                p=v.but_pause
                p.checked='true'
                p.text='继续'
            else:
                t0=t
    v.Text.enabled='true'
    jsla('bluetoothGetBondedDevicesRssi',-1)
    jsla('bluetoothDiscoveryCancel')
def getBluetoothOnce():
    try:
        rst=translate(rsla('bluetoothGetBondedDevices'),rsla('bluetoothGetReceivedDevices'))
        T.text=rst
    except:
        from traceback import format_exc
        T.text=format_exc()
        v.Title.text="错误信息"
        p=v.but_pause
        p.checked='true'
        p.text='继续'
def translate(Bond,Receive):
    Bond=translateGroup(Bond)
    Receive=translateGroup(Receive)
    return f"""★绑定设备：

{Bond}

★扫描设备：

{Receive}"""
def append(Prompt,Value):
    append.List.append(f'{Prompt}：{Value}')
BondState={12:'已绑定',10:'未绑定'}
Types={0:'未知',1:'经典',2:'低能耗',3:'双模式'}
def translateGroup(Dict):
    s=[]
    for i in Dict:
        s.append(translateOne(Dict[i],i))
    return '\n\n'.join(s)
def translateOne(Dict,Addr):
    append.List=[]
    append.Dict=Dict
    append('地址',Addr)
    if Dict.get('name'):
        append('名称',Dict['name'])
    append('绑定状态',BondState.get(Dict['bondState'],'未知'))
    if Dict.get('uuid'):
        append('UUID数',len(Dict['uuid']))
    append('类型',Types[Dict['type']])
    if Dict.get('connected')!=None:
        append('连接状态',Dict['connected'])
        if Dict.get('battery')!=None:
            append('电量',Dict['battery'])
    if Dict.get('rssi')!=None:
        append('信号强度',Dict['rssi'])
        i=Dict['time']/1000
        i=strftime('%Y-%m-%d %H:%M:%S',localtime(i))+str(round(i-int(i),3))[1:]
        append('信号时间',i)
    return '\n'.join(append.List)
def showInterval():
    if timeInterval<0:
        v.Title.text='单次(手动)测试'
    else:
        v.Title.text='连续(间隔%s秒)测试'%timeInterval
class MainScreen(Layout):
    def on_show(self):
        global v,T
        v=self.views
        T=v.Text
        v.but_pause.add_event(click_EventHandler(v.but_pause,self.pause))
        v.but_copy.add_event(click_EventHandler(v.but_copy,self.copy))
        v.but_exit.add_event(click_EventHandler(v.but_exit,self.exit))
        showInterval()
        getBluetoothConti()
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
            getBluetoothConti()
    def copy(self,view,dummy):
        jsla('setClipboard',T.text)
        v.but_copy.checked='false'
        jsla('makeToast','蓝牙信息已复制')
        if v.but_pause.text=='暂停':
            getBluetoothConti()
    def exit(self,view,dummy):
        FullScreenWrapper2App.close_layout()
def BluetoothText(TimeInterval=1):#主函数
#蓝牙信息(时间间隔=1秒,导出文件=无,备注=无)
#如果：时间间隔==-1，为单次(手动)测试
#如果：时间间隔>=0，为连续(自动)测试
#请授予QPython位置和蓝牙权限
    global timeInterval
    timeInterval=TimeInterval
    FullScreenWrapper2App.show_layout(MainScreen(XML))
    FullScreenWrapper2App.eventloop()
__all__=('BluetoothText','droid')
#by 乘着船 at https://www.bilibili.com/read/cv13278468