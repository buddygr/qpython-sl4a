#要求 QPython Plus 3.8.6 或以上
from android import *
import abc,pickle
from time import time
from hashlib import md5
from json import dumps,loads
class BaseDict(dict):
    def __init__(self,data=None):
        if data:
            dict.__init__(self,data)
        else:
            dict.__init__(self)
    def __setattr__(self,name,val):
            self[name]=val
    def __getattr__(self,name):
            return self[name]
    def __getstate__(self):
        return self.__dict__.copy()
    def __setstate__(self,dict):
        self.__dict__.update(dict)
    def copy(self):
        return pickle.loads(pickle.dumps(self))
class EventHandler(object):
    def __init__(self,event_name,compare_attribute,compare_value,view=None,handler_function=None):
        self.view=view
        self.event_name=event_name
        self.compare_attribute=compare_attribute
        self.compare_value=compare_value
        self.event_handler_fn=handler_function
    def match_event_data(self,event_data):
        try:
            if event_data["name"]==self.event_name:
                if self.compare_attribute !=None:
                    return event_data["data"][self.compare_attribute]==self.compare_value
                else:
                    return True
        except:
            return False
        else:
            return False
    def __str__(self):
        return str(self.event_name)+":"+str(self.compare_attribute)+"="+str(self.compare_value)
class click_EventHandler(EventHandler):
    EVENT_NAME="click"
    COMPARE_ATTRIBUTE="id"
    def __init__(self,view,handler_function=None):
        super(click_EventHandler,self).__init__(self.EVENT_NAME,self.COMPARE_ATTRIBUTE,view.view_id,view,handler_function)
class itemclick_EventHandler(EventHandler):
    EVENT_NAME="itemclick"
    COMPARE_ATTRIBUTE="id"
    def __init__(self,view,handler_function=None):
        super(itemclick_EventHandler,self).__init__(self.EVENT_NAME,self.COMPARE_ATTRIBUTE,view.view_id,view,handler_function)
class itemlongclick_EventHandler(EventHandler):
    EVENT_NAME="itemlongclick"
    COMPARE_ATTRIBUTE="id"
    def __init__(self,view,handler_function=None):
        super(itemlongclick_EventHandler,self).__init__(self.EVENT_NAME,self.COMPARE_ATTRIBUTE,view.view_id,view,handler_function)
class key_EventHandler(EventHandler):
    EVENT_NAME="key"
    COMPARE_ATTRIBUTE="key"
    def __init__(self,key_match_id="4",view=None,handler_function=None):
        super(key_EventHandler,self).__init__(self.EVENT_NAME,self.COMPARE_ATTRIBUTE,key_match_id,view,handler_function)
class View(object):
    def __init__(self,view_id,view_type):
        self.view_type=view_type
        self.view_id=view_id
        self._events={}
    def add_event(self,eventhandler):
        self._events[eventhandler.event_name]=eventhandler
    def remove_event(self,event_name):
        self._events.pop(event_name)
    def set_listitems(self,List=(),isHtml=False,listType=0):
        jsla('fullSetList',self.view_id,List,isHtml,listType)
    def __setattr__(self,name,value):
        if name in ("view_type","view_id","_events"):
            object.__setattr__(self,name,value)
        else:
            return jsla('fullSetProperty',self.id,name,value)
    def __getattr__(self,name):
        return rsla('fullGetProperty',self.view_id,name)
    def __str__(self):
        try:
            return self.text
        except AttributeError:
            return None
class Layout(object):
    __metaclass__=abc.ABCMeta
    #默认主题常数0，更多主题常数，参考 https://developer.android.google.cn/reference/android/R.style.html
    defaultTheme=0
    defaultTitle='QSL4A未来小程序'
    #初始化：自身,布局xml,标题,主题常数
    def __init__(self,xml,title=None,theme=None):
        self.uid=md5(str(str(title)+str(os.getpid())+str(time())).encode("UTF-8")).hexdigest()
        self.xml=xml
        if title==None:
            self.title=Layout.defaultTitle
        else:
            self.title=title
        if theme==None:
            self.theme=Layout.defaultTheme
        else:
            self.theme=theme
        self.views=BaseDict()
        self._reset()
    def _reset(self):
        self.views.clear()
        self.views[self.uid]=View(self.uid,"Layout")
    def add_event(self,eventhandler):
        self.views[self.uid].add_event(eventhandler)
    def remove_event(self,event_name):
        self.views[self.uid].remove_event(event_name)
    @abc.abstractmethod
    def on_show(self):
        pass
    @abc.abstractmethod
    def on_close(self):
        pass
class FullScreenWrapper2App(object):
    _layouts=[]
    SHOW_LAYOUT_PUSH_OVER_CURRENT=0
    SHOW_LAYOUT_REPLACING_CURRENT=1
    _SHOW_LAYOUT_POP_CURRENT=2
    SIGNAL_DATA=[]
    EVENT_DATA=[]
    #默认全屏窗口显示
    @classmethod
    def show_layout(cls,layout,show_mode=SHOW_LAYOUT_REPLACING_CURRENT):
        if show_mode in (0,1,2):#SHOW_LAYOUT_PUSH_OVER_CURRENT,SHOW_LAYOUT_REPLACING_CURRENT,_SHOW_LAYOUT_POP_CURRENT
            _layout=cls._layouts
            curlayoutidx=len(_layout)-1
            if(curlayoutidx > -1):
                _layout[curlayoutidx].on_close()
            jsla('fullShow',layout.xml,layout.title,layout.theme)
            viewsdict=rsla('fullQuery')
            layout._reset()
            views=layout.views
            for viewname in viewsdict:
                views[viewname]=View(viewname,viewsdict[viewname]["type"])
            if show_mode==cls.SHOW_LAYOUT_PUSH_OVER_CURRENT:
                _layout.append(layout)
            elif show_mode==cls.SHOW_LAYOUT_REPLACING_CURRENT:
                if(curlayoutidx > -1):
                    _layout.pop()
                _layout.append(layout)
            elif show_mode==cls._SHOW_LAYOUT_POP_CURRENT:
                if(curlayoutidx > -1):
                    _layout.pop() 
            layout.on_show()
    @classmethod
    def close_layout(cls):
        curlayoutidx=len(cls._layouts)-1
        if curlayoutidx >0:
            cls.show_layout(cls._layouts[curlayoutidx-1],cls._SHOW_LAYOUT_POP_CURRENT)
        elif curlayoutidx==0:
            cls.exit_FullScreenWrapper2App()
    @classmethod
    def exit_FullScreenWrapper2App(cls):
        jsla('fullDismiss')
        cls.SIGNAL_DATA.append(os.getpid())
    @classmethod
    #插入FullScreenWrapper2App的eventloop前运行的函数内容
    def insert_function(cls,function,*args,**kwargs):
        cls.SIGNAL_DATA.append((function,args,kwargs))
    @classmethod
    def get_event(cls):
    #FullScreenWrapper2App的eventloop函数疯狂运行时，该函数可以探测是否有点击事件
        cls.EVENT_DATA.extend(rsla('eventPoll'))
        return cls.EVENT_DATA
    @classmethod
    def eventloop(cls):
        if len(cls._layouts)<1:
            raise RuntimeError("Trying to start eventloop without a layout visible")
        evt=True
        while(True):
            for evt in cls.SIGNAL_DATA:
                if type(evt)==int:
                    evt=None
                    break
                else:
                    function,args,kwargs=evt
                    function(*args,**kwargs)
            cls.SIGNAL_DATA.clear()
            if evt==None:
                break
            evt=cls.EVENT_DATA
            evt.extend(rsla('eventPoll'))
            while len(evt)>0:
                eventdata=evt.pop(0)
                try:
                    eventdata["data"]=loads(eventdata["data"])
                except:
                    pass
                curlayout=cls._layouts[len(cls._layouts)-1]
                views=curlayout.views
                for viewname in views:
                    view=views[viewname]
                    _events=view._events
                    for eventname in _events:
                        event=_events[eventname]
                        if event.match_event_data(eventdata):
                            if event.event_handler_fn !=None:
                                event.event_handler_fn(event.view,eventdata)
                                event_handled=True
                                break
    @classmethod
    def set_list_contents(cls,*s,**t):
        return jsla('fullSetList',*s,**t)
    @classmethod
    def set_property_value(cls,id,property,value):
        return jsla('fullSetProperty',id,property,value)
    @classmethod
    def get_property_value(cls,id,property):
        return rsla('fullGetProperty',id,property)
    _show_layout=show_layout
    #特殊全屏窗口显示：背景批量替换
    @classmethod
    #显示布局替换背景：自身,布局对象,不透明度(0~255),背景图片,显示模式
    def show_layout_replace_background(cls,layout,opacity=255,background_image=None,show_mode=SHOW_LAYOUT_REPLACING_CURRENT):
        xml=layout.xml
        new=[];c=0;h=0
        o=hex(opacity)[2:]
        if len(o)==1:o='0'+o
        d=new.append;f=xml.find
        while True:
            a=xml.find('android:background=',c)
            if a==-1:
                d(xml[c:])
                break
            d(xml[c:a])
            b=f('#',a)
            h+=1
            if background_image==None or h>1:
                b+=1
                d(xml[a:b])
                c=f(xml[b-2],b)
                e=xml[b:c]
                if len(e)==6:
                    d(o+e)
                else:
                    d(o+e[2:])
            else:
                d(xml[a:b])
                c=f(xml[b-1],b)
                e=xml[b:c]
                d('file://'+background_image)
        layout.xml=''.join(new)
        return cls._show_layout(layout,show_mode)
def Str2Xml(s):
    t=[];r=t.append
    for i in s:
        j=ord(i)
        if j<256 and not (i.isalpha() or i.isdigit()):
            r('&#');r(str(j));r(";")
        else:
            r(i)
    return ''.join(t)
#默认按钮
CCC=('确认','复制','取消')
YCN=('是','复制','否')
ALNO=('全选','全不选')