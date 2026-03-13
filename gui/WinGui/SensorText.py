#需要QPython Plus 3.8.1或以上，旧版QPython均无法正常运行
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
        android:background="#7f007f"
		android:id="@+id/Title"
		android:layout_width="fill_parent"
		android:layout_height="fill_parent"
		android:textSize="8dp"
		android:text=""
		android:textColor="#00ff00"
		android:gravity="center"
		android:layout_weight="1"
	/>
	<TextView
        android:background="#ffffff"
		android:id="@+id/MagBear"
		android:layout_width="fill_parent"
		android:layout_height="fill_parent"
		android:textSize="10sp"
		android:text=""
		android:padding="2sp"
		android:textColor="#ffffbf"
		android:background="@android:color/transparent"
		android:gravity="center"
		android:layout_weight="8"
		android:radius="10dp"
	/>
	</LinearLayout>
	<EditText
        android:background="#ffffff"
		android:id="@+id/Text"
		android:layout_width="fill_parent"
		android:layout_height="wrap_content"
		android:textSize="6dp"
		android:text="正在获取传感器信息"
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
from math import sqrt,pi
def getSensorConti():
    t0=0
    v.Text.enabled='false'
    while v.but_copy.checked=='false' and v.but_pause.checked=='false' and v.but_exit.checked=='false':
        t=time()
        if t-t0>=timeInterval:
            getSensorOnce()
            if timeInterval<0:
                #单次测试
                p=v.but_pause
                p.checked='true'
                p.text='继续'
            else:
                t0=t
    v.Text.enabled='true'
def getSensorOnce():
    try:
        rst=sensorInfo()
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
            r('<font color=red>%s</font><font color=#007f00> = </font>%s'%(i,colord(str(t))),m)
    r('<font color=#007f00>}</font>',n)
def _listToStr(k,s,r,n):
    r('<font color=red>%s</font><font color=#007f00> = [</font>'%k,n)
    m=n+1
    for i in s:
        r(i,m)
    r('<font color=#007f00>]</font>',n)
def colord(s):
    t=[];a=t.append
    for i in s:
        o=ord(i)
        if i in '.:-':
            a('<font color=#000000><big>%s</big></font>'%i)
        elif 48<=o<=57:
            a(i)
        elif o==10:
            a('<br>')
        elif o==32:
            a('&nbsp;')
        else:
            a('<font color=#7f7f00>%s</font>'%i)
    return ''.join(t)
pid4=pi/4
def getTt(t):
    t=float(t[0]),float(t[1]),float(t[2])
    return sqrt(t[0]*t[0]+t[1]*t[1]+t[2]*t[2])
def sensorInfo():
    S = rsla('readSensors')
    #计步器StepCounter是从开机开始从0计数，关机或重启则自动清零
    if S==None:
        S={}
    else:
        try:
            i=S.pop('azimuth')
            if max(abs(S['roll']),abs(S['pitch']))>pid4:
                v.MagBear.text=''
                v.MagBear.rotation='0'
            else:
                v.MagBear.rotation=str((1-i/pi)*180)
                if i==0:
                    v.MagBear.textColor='#ff0000'
                else:
                    v.MagBear.textColor='#ffffbf'
                v.MagBear.text='V'
            i='%srad\n  (见右上方,箭头指北)'%i
            t=S.pop('xforce'),S.pop('yforce'),S.pop('zforce')
            S['加速度x']='%sm/s²'%t[0]
            S['加速度y']='%sm/s²'%t[1]
            S['加速度z']='%sm/s²'%t[2]
            S['加速度(合)']='%sm/s²'%getTt(t)
            S['磁力x']='%sμT'%S.pop('xMag')
            S['磁力y']='%sμT'%S.pop('yMag')
            S['磁力z']='%sμT'%S.pop('zMag')
            S['角速度x']='%srad/s'%S.pop('xAngularSpeed')
            S['角速度y']='%srad/s'%S.pop('yAngularSpeed')
            S['角速度z']='%srad/s'%S.pop('zAngularSpeed')
            S['光线']='%slux'%S.pop('light')
            S['磁方位角']=i
            S['横滚角']='%srad'%S.pop('roll')
            S['俯仰角']='%srad'%S.pop('pitch')
            S['计步器']='%s(开机以来)'%S.pop('stepCounter')
        except:
            pass
        try:
            t=S.pop('time')
            S['系统时间']=strftime('%Y-%m-%d %H:%M:%S',localtime(t))+str(round(t-int(t),3))[1:]
            ns=rsla('elapsedRealtimeNanos')
            s,ns=divmod(ns,1000000000)
            d,s=divmod(s,86400)
            h,s=divmod(s,3600)
            m,s=divmod(s,60)
            S['开机时间']=f'{d}d:{h}h:{m}m:{s}s:{ns}ns'
            S['精度位数']=S.pop('accuracy')
        except:
            pass
    return dictToStr(S)
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
        jsla('stopSensing')
        jsla('startSensingTimed',1,900)
        getSensorConti()
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
            getSensorConti()
    def copy(self,view,dummy):
        jsla('setClipboard',T.text)
        v.but_copy.checked='false'
        jsla('makeToast','传感器信息已复制')
        if v.but_pause.text=='暂停':
            getSensorConti()
    def exit(self,view,dummy):
        jsla('stopSensing')
        FullScreenWrapper2App.close_layout()
def SensorText(TimeInterval=1):#主函数
#传感器信息(时间间隔=1秒,导出文件=无,备注=无)
#如果：时间间隔==-1，为单次(手动)测试
#如果：时间间隔>=0，为连续(自动)测试
    global timeInterval
    timeInterval=TimeInterval
    FullScreenWrapper2App.show_layout(MainScreen(XML))
    FullScreenWrapper2App.eventloop()
__all__=('SensorText','droid')
#by 乘着船 at https://www.bilibili.com/read/cv16824060