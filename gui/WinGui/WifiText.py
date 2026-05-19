#需要QPython Plus 3.8.1或以上
from .BaseWindow import *
from os import environ
from time import strftime
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
		android:text="正在获取网络信息"
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
def getWifiConti():
    t0=0
    v.Text.enabled='false'
    while v.but_copy.checked=='false' and v.but_pause.checked=='false' and v.but_exit.checked=='false':
        t=time()
        if t-t0>=timeInterval:
            getWifiOnce()
            if timeInterval<0:
                #单次测试
                p=v.but_pause
                p.checked='true'
                p.text='继续'
            else:
                t0=t
    v.Text.enabled='true'
def getWifiOnce():
    try:
        rst=translate(rsla('wifiGetConnectionInfo'),rsla('wifiGetScanResults'))
        T.text=rst
        if toFile:
            open(toFile,'a',encoding='utf-8').write(rst+'\n\n')
    except:
        from traceback import format_exc
        T.text=format_exc()
        v.Title.text="错误信息"
        p=v.but_pause
        p.checked='true'
        p.text='继续'
def translate(This,All):
    if This==None:
        raise Exception('没有获取到WiFi信息，请稍后点击“继续”。')
    s=[];t=s.append
    i=time()
    i=strftime('%Y-%m-%d %H:%M:%S')+str(round(i-int(i),3))[1:]
    if This['ssid'][0]!='<':
        This['ssid']=This['ssid'][1:-1]
    This['bssid']=This.get('bssid','<unknown bssid>')
    if int(environ['ANDROID_SDK'])>=30:
        j='\n标准:'+This['standard']
    else:
        j=''
    try:
        This['remark']='\n备注:'+remark[This['bssid']]
    except:
        This['remark']=''
    t(f"""★当前连接：
网络名:{This['ssid']}
IP地址:{This['ip_address']}
信号强度:{This['rssi']}dbm
网络速率:{This['link_speed']}Mbps
频率:""")
    t(str(This.get('frequency',-1)))
    t(f"""MHz
网络号:{This['network_id']}
BSSID:{This['bssid']}{This['remark']}
请求状态:{This['supplicant_state']}
隐藏:{This['hidden_ssid']}{j}
时间:{i}

★其他连接：
""")
    l=len(All)
    i=0
    while i<l-1:
        j=i+1
        while j<l:
            if All[i]['level']<All[j]['level']:
                All[i],All[j]=All[j],All[i]
            j+=1
        i+=1
    for i in All:
        if int(environ['ANDROID_SDK'])>=30:
            j='\n标准:'+This['standard']
        else:
            j=''
        try:
            i['remark']='\n备注:'+remark[i['bssid']]
        except:
            i['remark']=''
        t(f"""
网络名:{i['ssid']}
频率:{i['frequency']}MHz
信号强度:{i['level']}dbm
功能:{i['capabilities']}
BSSID:{i['bssid']}{i['remark']}{j}
""")
        if s[1]=='-1' and i['bssid']==This['bssid'] and This['bssid'][0]!='<':
            s[1]=str(i['frequency'])+' '
    if s[1]=='-1' and This['link_speed']>0:
        if This['link_speed']<=150:
            s[1]='2400+'
        else:
            s[1]='5000+'
    return ''.join(s)
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
        getWifiConti()
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
            getWifiConti()
    def copy(self,view,dummy):
        jsla('setClipboard',T.text)
        v.but_copy.checked='false'
        jsla('makeToast','WiFi信息已复制')
        if v.but_pause.text=='暂停':
            getWifiConti()
    def exit(self,view,dummy):
        FullScreenWrapper2App.close_layout()
def WifiText(TimeInterval=1,ToFile=None,Remark=None):#主函数
#Wifi信息(时间间隔=1秒,导出文件=无,备注=无)
#如果：时间间隔==-1，为单次(手动)测试
#如果：时间间隔>=0，为连续(自动)测试
#备注格式：{'bssid1':'备注1',......}
#请授予QPython位置和WiFi权限
    global timeInterval,toFile,remark
    timeInterval=TimeInterval
    toFile=ToFile
    try:
        i=tuple(Remark)
        k={}
        for j in i:
            k[j.replace('-',':').lower()]=Remark.pop(j)
        remark=k
    except:
        remark=None
    FullScreenWrapper2App.show_layout(MainScreen(XML))
    FullScreenWrapper2App.eventloop()
__all__=('WifiText','droid')
#by 乘着船 at https://www.bilibili.com/read/cv13278468
