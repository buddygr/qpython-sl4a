#需要QPython Plus 3.7.7或以上
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
        android:background="#ffffaf"
		android:id="@+id/Title"
		android:layout_width="fill_parent"
		android:layout_height="wrap_content"
		android:text=""
		android:textSize="6dp"
		android:textColor="#ff0000"
		android:layout_weight="1"
		android:gravity="center"
	/>
	<EditText
        android:background="#ffffff"
		android:id="@+id/Text"
		android:layout_width="fill_parent"
		android:layout_height="wrap_content"
		android:text="正在获取定位/卫星信息"
		android:textSize="6dp"
		android:textColor="#0000ff"
		android:layout_weight="1"
		android:enabled="false"
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
F3=['false']*3
PCE=['but_pause','but_copy','but_exit']
def getAddrConti():
    jsla('startLocating',1000*timeInterval,1,True)
    t0=0
    v.Text.enabled='false'
    while rsla('fullGetProperties',PCE,'checked')==F3:
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
    v.Text.enabled='true'
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
        location['satellite']=rsla('readGnssStatus')
        location['from']='%s/%s'%(key,fun)
        T.text=translate(location)
    except:
        from traceback import format_exc
        T.text='''
请打开QPython位置信息权限，
请打开系统定位功能。
'''+format_exc()
        v.Title.text="错误信息"
        p=v.but_pause
        p.checked='true'
        p.text='继续'
YN={True:'是',False:'否'}
def translate(Data):
    t=divmod(Data['time'],1000)
    t=strftime('%Y-%m-%d %H:%M:%S',localtime(t[0]))+str(t[1]/1000)[1:]
    Str=[];a=Str.append
    n={}
    n['纬度']=Data.get('latitude')
    n['经度']=Data.get('longitude')
    n['高度']='%s米'%Data.get('altitude')
    n['精度']='%s米'%Data.get('accuracy')
    n['速度']='%s米/秒'%Data.get('speed',0)
    n['速度方位']='%s度'%Data.get('bearing',0)
    n['定位时间']=t
    n['定位来源']=Data.get('from')
    for i in n:
        a('%s：%s'%(i,n[i]))
    Str=['\n'.join(Str)]
    a=Str.append
    Satellite=Data['satellite']
    if Satellite!=None:
        a(None)
        u=n=0;t={}
        for i in Satellite:
            i=Satellite[n]
            k=i['ConstellationType']
            m=t.get(k,[0,0,0])
            if i['UsedInFix']:
                m[0]+=1
            m[2]+=1
            c=i['Cn0DbHz']
            if c>m[1]:
                m[1]=c
            t[k]=m
            i['星座']=i.pop('ConstellationType')
            i['卫星号']=i.pop('Svid')
            i['方位角']=i.pop('AzimuthDegrees')
            i['高度角']=i.pop('ElevationDegrees')
            i['载噪比']=i.pop('Cn0DbHz')
            try:
                i['频点']=i.pop('CarrierFrequencyHz')
            except:
                pass
            m=i.pop('UsedInFix')
            i['可用=']=YN[m]
            n+=1
            if m:
                u+=1
            m=[];c=m.append
            for j in i:
                c('%s%s'%(j,i[j]))
            a('卫星%s:'%n+','.join(m))
        c=[];i=c.append
        for j in t:
            k=t[j]
            k.append(j)
            i(k)
        c.sort(reverse=True)
        n=['卫星：可用%s / 发现%s'%(u,n)];t=n.append
        for k in c:
            t('%s:可用%s,发现%s,最大载噪比%s'%(k[3],k[0],k[2],k[1]))
        Str[1]='\n'.join(n)
    else:
        try:
            sdk=int(os.environ['ANDROID_SDK'])
        except:
            sdk=0
        if sdk<26:
            a('卫星：需要Android>=8')
        else:
            a('卫星：未发现或者正在寻星')
    return '\n'.join(Str)
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
        jsla('makeToast','定位/卫星信息已复制')
        if v.but_pause.text=='暂停':
            getAddrConti()
    def exit(self,view,dummy):
        jsla('stopLocating')
        FullScreenWrapper2App.close_layout()
def NavigationSatelliteText(TimeInterval=1):#主函数
#导航卫星信息(时间间隔=1秒)
#如果：时间间隔==-1，为单次(手动)定位
#如果：时间间隔>=0，为连续(自动)定位
    global timeInterval
    timeInterval=TimeInterval
    FullScreenWrapper2App.show_layout(MainScreen(XML))
    FullScreenWrapper2App.eventloop()
__all__=('NavigationSatelliteText','droid')
#by 乘着船 at https://www.bilibili.com/read/cv18956157
