#需要QPython 3C 3.7.3或以上，旧版QPython均无法正常运行
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
    <TextView
        android:background="#7f007f"
		android:id="@+id/Title"
		android:layout_width="fill_parent"
		android:layout_height="wrap_content"
		android:textSize="6dp"
		android:text=""
		android:textColor="#00ff00"
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
from time import time
def getWebConti():
    t0=0
    v.Text.enabled='false'
    while v.but_copy.checked=='false' and v.but_pause.checked=='false' and v.but_exit.checked=='false':
        t=time()
        if t-t0>=timeInterval:
            getWebOnce()
            if timeInterval<0:
                #单次测试
                p=v.but_pause
                p.checked='true'
                p.text='继续'
            else:
                t0=t
    v.Text.enabled='true'
def getWebOnce():
    try:
        rst=netInfo()
        T.html=rst
    except:
        from traceback import format_exc
        T.text=format_exc()
        v.Title.text="错误信息"
        p=v.but_pause
        p.checked='true'
        p.text='继续'
def dictToStr(s):
    r=[];a=r.append
    def b(s,n):
        a(n*'&nbsp;&nbsp;'+s)
    _dictToStr('',s,b,-1)
    return '<br>'.join(r[1:-1])
def _dictToStr(k,s,r,n):
    r('<font color=red>%s</font><font color=#007f00> = {</font>'%k,n)
    m=n+1
    for i in s:
        t=s[i]
        j=type(t)
        if j==list:
            _listToStr(i,t,r,m)
        elif j==dict:
            _dictToStr(i,t,r,m)
        else:
            r('<font color=red>%s</font><font color=#007f00> = </font>%s'%(i,Str2Xml(str(t))),m)
    r('<font color=#007f00>}</font>',n)
def _listToStr(k,s,r,n):
    r('<font color=red>%s</font><font color=#007f00> = [</font>'%k,n)
    m=n+1
    for i in s:
        r(i,m)
    r('<font color=#007f00>]</font>',n)
from .MobileText import Int,getInfo,Now
def getSignalStrength():
    info=getInfo()
    return {
    #Type:网络类型:5G/4G/3G/2G/Unknown
    'Type':rsla('getNetworkType'),
    #Level:信号等级:0到4(有的机型是5)
    'Level':info['level'],
    #Strength:综合信号强度
    'Strength':info['dbm'],
    'CellLocation':getCellLocation(),
    #移动信号其他具体信息
    'Detail':info['detail']
    }
def getCellLocation():
    #获取周围基站个数
    #获取当前基站：LAC/CID/SID/NID/BID等
    #获取当前基站信号Dbm，与综合信号Dbm可不相等
    s=rsla('getCellLocation')
    try:
        for i in tuple(s):
            if s[i] in (-1,0,2147483647):
                s.pop(i)
    except:pass
    return s
def netInfo():
    S = {

    'System Time':Now(),
    'Mobile Network Signal':getSignalStrength(),

    'WiFi Information':{
    'Dhcp Information':rsla('getDhcpInfo'),
    'Connection Information':rsla('wifiGetConnectionInfo'),
    'WiFi HotSpot State':rsla('wifiGetApState')
    },

    'Internet Interface Address Information':rsla('getInternetInterfaceAddress'),
    
    'Web Speed ( since Startup )':getWebSpeed(),
    'Startup Time':startupTime()
    }
    return dictToStr(S)
def getWebSpeed():
    data={}
    stat=esla('getTrafficStats')
    try:
        time=getWebSpeed.Time
    except:
        pass
    Time=getWebSpeed.Time=stat['StartupTime']
    for j in 'Total:include SL4A','Mobile:only  Mobile','QPython:include SL4A':
        d={}
        j,n=j.split(':')
        for i in 'Tt↑','Rr↓':
            i,k,f=i
            exec(f'''
{j}{i}x=stat["{j}{i}xBytes"]
try:
    {j}{k}x=getWebSpeed.{j}{i}x
    {j}{k}x=({j}{i}x-{j}{k}x)*1000/(Time-time)
except:
    {j}{k}x=-1
getWebSpeed.{j}{i}x={j}{i}x
d["{f}"]=GetSpaceText({j}{i}x)+"　"+GetSpaceText({j}{k}x)+"/s"
''')
        exec(f'data["{j} ( {n} )"]=d')
    return data
def GetSpaceText(Bytes):
    if Bytes<KB:
        return Str(Bytes)+'B'
    elif Bytes<MB:
        return Str(Bytes/KB)+'KB'
    elif Bytes<GB:
        return Str(Bytes/MB)+'MB'
    elif Bytes<TB:
        return Str(Bytes/GB)+'GB'
    else:
        return Str(Bytes/TB)+'TB'
def Str(Val):
    Val=str(Val)[:5]
    if Val[-1:]=='.':
        Val=Val[:-1]
    return Val
def startupTime():
    ns=rsla('elapsedRealtimeNanos')
    s,ns=divmod(ns,1000000000)
    d,s=divmod(s,86400)
    h,s=divmod(s,3600)
    m,s=divmod(s,60)
    return f'{d}d:{h}h:{m}m:{s}s:{ns}ns'
KB=1024
MB=KB*1024
GB=MB*1024
TB=GB*1024
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
        getWebConti()
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
            getWebConti()
    def copy(self,view,dummy):
        jsla('setClipboard',T.text)
        v.but_copy.checked='false'
        jsla('makeToast','网络信息已复制')
        if v.but_pause.text=='暂停':
            getWebConti()
    def exit(self,view,dummy):
        FullScreenWrapper2App.close_layout()
def WebText(TimeInterval=1):#主函数
#Web信息(时间间隔=1秒,导出文件=无,备注=无)
#如果：时间间隔==-1，为单次(手动)测试
#如果：时间间隔>=0，为连续(自动)测试
#备注格式：{'bssid1':'备注1',......}
#请授予QPython电话、位置和WiFi权限
    global timeInterval
    timeInterval=TimeInterval
    FullScreenWrapper2App.show_layout(MainScreen(XML))
    FullScreenWrapper2App.eventloop()
__all__=('WebText','droid')
#by 乘着船 at https://www.bilibili.com/read/cv16061380