#需要QPython Plus 3.8.3或以上，旧版QPython均无法正常运行
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
def getMobileConti():
    t0=0
    v.Text.enabled='false'
    while v.but_copy.checked=='false' and v.but_pause.checked=='false' and v.but_exit.checked=='false':
        t=time()
        if t-t0>=timeInterval:
            getMobileOnce()
            if timeInterval<0:
                #单次测试
                p=v.but_pause
                p.checked='true'
                p.text='继续'
            else:
                t0=t
    v.Text.enabled='true'
def getMobileOnce():
    try:
        rst=rsla('getAllCellsLocation')
        if rst==None or len(rst)==0:
            rst=[{'No Cell Location':'No Signal, No Location Permission or No Phone Permission .'}]
        info=getInfo()
        rst.insert(0,{
'Time':Now(),
#Type:网络类型:WIFI/5G/4G/3G/Unknown
'Type':rsla('getNetworkType'),
#Level:信号等级:0到4(有的机型是5)
'Level':info['level'],
#Strength:综合信号强度
'Strength':info['dbm']
        })
        txt=[]
        r=txt.append;r('')
        for i in rst:
            for j in i:
                r('<font color=red>%s</font><font color=#007f00> = </font><font color=blue>%s</font>'%(Str2Xml(j),Str2Xml(str(i[j]))))
            r('')
        T.html='<br>'.join(txt)
    except:
        from traceback import format_exc
        T.text=format_exc()
        v.Title.text="错误信息"
        p=v.but_pause
        p.checked='true'
        p.text='继续'
def Int(x):
    try:
        return int(x)
    except:
        return -255
def Now():
    t=time()
    return strftime('%Y-%m-%d %H:%M:%S',localtime(t))+str(round(t-int(t),3))[1:]
sdk=int(os.environ['ANDROID_SDK'])
#detail:信号详细信息，如RSRP/RSRQ/SNR
#level:信号等级
#dbm:信号电平dbm
#getDbm解析综合信号强度
if sdk<=28:
    rsla('startTrackingSignalStrengths')
    def getInfo():
        detail=rsla('readSignalStrengths')
        try:
            level=detail.pop('level')
        except:
            level='Unknown'
        dbm=getDbm(detail)
        return {'detail':detail,'level':level,'dbm':dbm}
    def getDbm(detail):
        try:
            dbm=detail.pop('dbm')
        except:
            dbm=0
        if detail.get('lte_rsrp',0)==dbm and -40>=dbm>=-140:
            return 'LTE %sdbm %sasu'%(dbm,140+dbm)
        return '%sdbm'%dbm
else:
    def getInfo():
        detail=rsla('getTelephoneSignalStrengthDetail')
        level=rsla('getTelephoneSignalStrengthLevel')
        dbm=getDbm(detail)
        return {'detail':detail,'level':level,'dbm':dbm}
    def getDbm(detail):
        form={'ssRsrp':'NR','rsrp':'LTE'}
        if not detail:
            return 'No Signal'
        detail=detail.replace(' = ','=')
        for m in form:
            i=detail.find(m+'=')
            if i==-1:
                continue
            i+=len(m)+1
            j=detail.find(' ',i)
            dbm=Int(detail[i:j])
            if -40>=dbm>=-140:
                j=form[m]
                return '%s %sdbm %sasu'%(j,dbm,dbm+140)
        form=('rsrp','dbm','rssi','ss')
        detail=detail.lower()
        for m in form:
            i=0
            while True:
                i=detail.find(m+'=',i)
                if i==-1:
                    break
                i+=len(m)+1
                j=detail.find(' ',i)
                dbm=Int(detail[i:j])
                if -20>=dbm>=-140:
                    return '%sdbm'%dbm
                else:
                    i=j
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
        getMobileConti()
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
            getMobileConti()
    def copy(self,view,dummy):
        jsla('setClipboard',T.text)
        v.but_copy.checked='false'
        jsla('makeToast','移动网络信息已复制')
        if v.but_pause.text=='暂停':
            getMobileConti()
    def exit(self,view,dummy):
        FullScreenWrapper2App.close_layout()
def MobileText(TimeInterval=1):#主函数
#移动网络信息(时间间隔=1秒)
#如果：时间间隔==-1，为单次(手动)测试
#如果：时间间隔>=0，为连续(自动)测试
#请授予QPython位置和电话权限
    global timeInterval,remark
    timeInterval=TimeInterval
    FullScreenWrapper2App.show_layout(MainScreen(XML))
    FullScreenWrapper2App.eventloop()
__all__=('MobileText','droid')
#by 乘着船 at https://www.bilibili.com/read/cv16061380