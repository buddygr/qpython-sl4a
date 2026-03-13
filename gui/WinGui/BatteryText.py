#需要QPython Plus 3.8.2或以上，旧版QPython均无法正常运行
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
        android:background="#afffaf"
		android:id="@+id/Title"
		android:layout_width="fill_parent"
		android:layout_height="wrap_content"
		android:textSize="8dp"
		android:text=""
		android:enabled="false"
		android:textColor="#000"
		android:layout_weight="1"
		android:gravity="center"
	/>
	<EditText
        android:background="#ffffff"
		android:id="@+id/Text"
		android:layout_width="fill_parent"
		android:layout_height="wrap_content"
		android:textSize="8dp"
		android:text="正在获取电池信息"
		android:textColor="#000"
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
		android:background="#007f7f"
		android:textColor="#ffffffff"
		android:layout_weight="1"
		android:gravity="center"/>
	<RadioButton
		android:layout_width="fill_parent"
		android:layout_height="fill_parent"
		android:text="复制"
		android:id="@+id/but_copy"
		android:background="#7f7f00"
		android:textColor="#ffffffff"
		android:layout_weight="1"
		android:gravity="center"/>
	<RadioButton
		android:layout_width="fill_parent"
		android:layout_height="fill_parent"
		android:text="退出"
		android:id="@+id/but_exit"
		android:background="#7f007f"
		android:textColor="#ffffffff"
		android:layout_weight="1"
		android:gravity="center"/>
	</LinearLayout>
</LinearLayout>"""
from time import time,localtime,strftime,sleep
def getBattConti():
    jsla('batteryStartMonitoring')
    v.Text.enabled="false"
    sleep(.5)
    t0=0
    while v.but_copy.checked==v.but_pause.checked==v.but_exit.checked=='false':
        t=time()
        if t-t0>=timeInterval:
            getBattOnce()
            if timeInterval<0:
                #单次监测
                p=v.but_pause
                p.checked='true'
                p.text='继续'
            else:
                t0=t
    jsla('batteryStopMonitoring')
    v.Text.enabled="true"
    if not v.but_copy.checked=="true":
        E.clear()
def getBattOnce():
    try:
        data = rsla('readBatteryData')
        if data is None:
            raise Exception('没有任何电池信息。')
        c=curChg(data.get('current',0))
        if c<-1020:c=-1020
        elif c>1020:c=1020
        c=c*abs(c)/1020
        c=c+1020
        c=int(round(c/8,0))
        T.textColor='#'+Hex(255-c)+'00'+Hex(c)
        translate(data)
        text=[]
        for i in data:
            text.append('%s = %s'%(i,data[i]))
        T.text='\n'.join(text)
    except:
        from traceback import format_exc
        T.text='''
请打开QPython电池信息权限
'''+format_exc()
        v.Title.text="错误信息"
        p=v.but_pause
        p.checked='true'
        p.text='继续'
E=[];K=False
def curChg(c):
    global K
    if K:
        c/=-1000
    elif abs(c)>20000:
        K=True
        c/=-1000
    return c
def translate(data):
    global N
    N=time()
    data['时间']=Now(N)
    try:
        data['电量(%)']=data.pop('level')
        data['温度(℃)']=data.pop('temperature')/10
        data['连接']=plugDict[data.pop('plugged')]
        data['状态']=statusDict[data.pop('status')]
        data['电压(mV)']=data.pop('voltage')
        i=curChg(data.pop('current'))
        data['电流(mA)']=i
        data['电量(mAh)']=data.pop('charge')/1000
        getPower(data)
        data['健康']=healthDict[data.pop('health')]
        data['电池技术']=data.pop('technology')
        data['当前电池']=data.pop('battery_present')
    except:
        pass
def getPower(data):
    P=data['电量(mAh)']*data['电压(mV)']/1e6
    data['能量(Wh)']=round(P,2)
    try:
        C=powerIntervalCount
    except:
        return
    if C==None:
        C=440-round(min(max(abs(data['电流(mA)']),500),2000)*0.16)
    else:
        C*=2
    le=len(E)
    if le and E[0]!=data['连接']:
        E.clear()
    elif le>1:
        E.append(P)
        E.append(N)
        i=E[-1]-E[2]
        data['功率(W)(%.2f秒)'%i]=round((E[-2]-E[1])*3600/i,2)
        if len(E)>C:
            E.pop(1);E.pop(1)
            if len(E)>C:
                E.pop(1);E.pop(1)
    else:
        E.append(data['连接'])
        E.append(P)
        E.append(N)
def Now(t):
    return strftime('%Y-%m-%d %H:%M:%S',localtime(t))+str(round(t-int(t),3))[1:]
def Hex(x):
    x=hex(x)[2:]
    if len(x)==1:
        return '0'+x
    return x
plugDict={
   -1:'未知',
    0:'未连接',
    1:'交流电',
    2:'USB',
    4:'无线充电'
}
statusDict={
    1:'未知',
    2:'正在充电',
    3:'正在放电',
    4:'未在充电',
    5:'已充满'
}
healthDict={
    1:'未知',
    2:'好',
    3:'过热',
    4:'挂了',
    5:'过压',
    6:'未定义的错误'
}
class MainScreen(Layout):
    def on_show(self):
        global v,T
        v=self.views
        T=v.Text
        v.but_pause.add_event(click_EventHandler(v.but_pause,self.pause))
        v.but_copy.add_event(click_EventHandler(v.but_copy,self.copy))
        v.but_exit.add_event(click_EventHandler(v.but_exit,self.exit))
        if timeInterval<0:
            v.Title.text='单次(手动)监测'
        else:
            v.Title.text='连续(间隔%s秒)监测'%timeInterval
        getBattConti()
    def on_close(self):
        pass
    def pause(self,view,dummy):
        p=v.but_pause
        p.checked='false'
        if p.text=='暂停':
            p.text='继续'
        else:
            p.text='暂停'
            getBattConti()
    def copy(self,view,dummy):
        jsla('setClipboard',T.text)
        v.but_copy.checked='false'
        jsla('makeToast','电池信息已复制')
        if v.but_pause.text=='暂停':
            getBattConti()
    def exit(self,view,dummy):
        FullScreenWrapper2App.close_layout()
def BatteryText(TimeInterval=1,PowerIntervalCount=None):#主函数
#电池信息(时间间隔=1,功率检测间隔数=None)
#如果：时间间隔==-1，为单次(手动)监测
#如果：时间间隔>=0，为连续(自动)监测，时间间隔单位：秒
#如果：时间间隔>0，功率检测间隔数>0，才会自动监测功率，功率检测间隔数单位：时间间隔次
#如果：功率检测间隔数==None，为自动控制功率监测频率
    global timeInterval,powerIntervalCount
    timeInterval=TimeInterval
    if TimeInterval>0:
        powerIntervalCount=PowerIntervalCount
    FullScreenWrapper2App.show_layout(MainScreen(XML))
    FullScreenWrapper2App.eventloop()
__all__=('BatteryText','droid')
#by 乘着船 at https://www.bilibili.com/read/cv17813243