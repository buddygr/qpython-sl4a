#需要 QPython Plus >= 3.8.6
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
    android:layout_height="%sdp"
    android:layout_weight="1" > 
<LinearLayout
    android:layout_width="fill_parent"
	android:layout_height="fill_parent"
	android:orientation="vertical"
	android:layout_weight="1"
	android:gravity="center">
%s
</LinearLayout>
</ScrollView>
<ListView
    android:id="@+id/listview"
    android:layout_width="match_parent"
    android:layout_height="wrap_content"
    android:layout_weight="20"
/>
<LinearLayout
    android:layout_width="fill_parent"
	android:layout_height="50dp"
	android:orientation="horizontal"
	android:layout_weight="1"
	android:gravity="bottom">
%s
<Button
	android:layout_width="fill_parent"
    android:layout_height="fill_parent"
    android:text="%s"
    android:id="@+id/but_canc"
    android:textAllCaps="false"
    android:textSize="5sp"
    android:background="#3faf7f"
    android:textColor="#ffffff"
    android:layout_weight="1"
    android:gravity="center"/>
</LinearLayout>
</LinearLayout>"""
CfAlNoBtn='''<Button
	android:layout_width="fill_parent"
    android:layout_height="fill_parent"
    android:text="%s"
    android:id="@+id/but_conf"
    android:textAllCaps="false"
    android:textSize="5sp"
    android:background="#7faf3f"
    android:textColor="#ffffff"
    android:layout_weight="1"
    android:gravity="center"/>
<Button
	android:layout_width="fill_parent"
    android:layout_height="fill_parent"
    android:text="%s"
    android:id="@+id/but_alno"
    android:textAllCaps="false"
    android:textSize="5sp"
    android:background="#af3f3f"
    android:textColor="#ffffff"
    android:layout_weight="1"
    android:gravity="center"/>'''
TextVw='''<TextView
	android:background="#ffffff"
	android:id="@+id/%s%s"
	android:layout_width="fill_parent"
	android:layout_height="wrap_content"
	android:textSize="6sp"
	android:%s="%s"
	android:textColor="#%s"
	android:layout_weight="1"
	android:layout_marginBottom="2dp"
	android:paddingLeft="5dp"
	android:paddingRight="5dp"
/>'''
TxtTtl='''<TextView
	android:background="#af7f3f"
	android:id="@+id/Title"
	android:layout_width="fill_parent"
	android:layout_height="wrap_content"
	android:textSize="7sp"
	android:%s="%s"
	android:gravity="center"
    android:textColor="#ffffff"
    %s
	android:layout_weight="1"
	android:layout_marginTop="2dp"
	android:paddingLeft="5dp"
	android:paddingRight="5dp"
/>'''
TxtBld='android:textStyle="bold"'
class MainScreen(Layout):
    def on_show(self):
        global v
        v=self.views
        jsla('fullSetList',"listview",self.List,self.IsHtml,self.ListType%10)
        if self.Selected:
            jsla('fullSetListSelected',"listview",self.Selected)
        d=v.but_canc
        c=d.add_event
        c(click_EventHandler(d,self.canc))
        c(key_EventHandler('4',d,self.canc))
        if self.ListType in (0,10):
            c=v.listview
            c.add_event(itemclick_EventHandler(c,self.itcl))
            if self.ListType==10:
                c.add_event(itemlongclick_EventHandler(c,self.itlc))
            return
        c=v.but_conf
        c.add_event(click_EventHandler(c,self.conf))
        c=v.but_alno
        if self.ListType<3:
            d=self.none
        else:
            d=self.alno
        c.add_event(click_EventHandler(c,d))
    def on_close(self):
        pass
    def itcl(self,view,dummy):
        MainScreen.List=int(dummy['data']['position'])
        FullScreenWrapper2App.close_layout()
    def itlc(self,view,dummy):
        MainScreen.List=float(dummy['data']['position'])
        FullScreenWrapper2App.close_layout()
    def conf(self,view,dummy):
        MainScreen.List=rsla("fullGetListSelected","listview")
        FullScreenWrapper2App.close_layout()
    def none(self,view,dummy):
        jsla("fullSetListSelected","listview",-1)
    def alno(self,view,dummy):
        jsla("fullSetListSelected","listview",MainScreen.All)
        MainScreen.All=not MainScreen.All
        v.but_alno.text=MainScreen.Button[0^MainScreen.All+2]
    def canc(self,view,dummy):
        MainScreen.List=None
        FullScreenWrapper2App.close_layout()

#默认按钮组
DftBtn=(CCC[2],CCC[0],ALNO[1],ALNO[0])

#主函数
def ListChoice(Text="",List=(),isHtml=False,ListType=0,Selected=None,Button=None,TextHeight=50):

#函数解释：
#  命令按钮组(标题文本组=空,命令按钮文本组(按钮1,按钮2,……),是否Html=否,列表类型=SIMPLE(0),默认选项=空,默认按钮文本组=空,标题文本组行高=50dp)

#标题文本组 Text：
#  单一字符串：仅标题
#  字符串数组：数组第一个是标题，第二个到最后一个是多行文字说明
#  过长标题文本组可以滚动

#列表内容 List
#是否Html  isHtml :
#  如果isHtml为True，List为Html
#  如果isHtml为False，List为Text

#列表类型 ListType :
#  SIMPLE=0  简易型列表
#  SIMPLE_LONG_CLICK=10  简易型列表(可长按)
#  SINGLE_CHOICE_LEFT=1  单选列表，圆形选项框在左
#  SINGLE_CHOICE_RIGHT=2  单选列表，圆形选项框在右
#  MULTI_CHOICE_LEFT=3  复选列表，方形选项框在左
#  MULTI_CHOICE_RIGHT=4  复选列表，方形选项框在右

#初始选项 Selected :
#  数据类型 可以是 单个整数、整数列表、True/False
#  针对 单选列表，数据类型 为 单个整数，假设选项组长度为N，则0为第一项，(N-1)为最后一项，-1为全不选
#  针对 复选列表，数据类型 为 整数列表，假设选项组长度为N，则0为第一项，(N-1)为最后一项，列表格式类似于 [0, 3, 5]，[ ] ( 空列表 ) 为全不选, [ 0, 1, 2, …… , N-1 ] 为全选
#  针对 复选列表，特殊值True为全选，特殊值False为全不选
#  针对 简易列表，该参数不起作用

#默认按钮文本组 Button：
#  简易型(单一字符串)："取消按钮文本"
#  单选型(字符串数组)：("取消按钮文本","确认按钮文本","全不选按钮文本")
#  复选型(字符串数组)：("取消按钮文本","确认按钮文本","全不选按钮文本","全选按钮文本")

#标题文本组高度 TextHeight

#返回值：
#  点“确认”后，不同列表类型，返回值不同
#    简易型：返回0,1,2,……
#    简易长按型：短按返回整数 0,1,2,……，长按返回浮点数 0.0,1.0,2.0,……
#    单选型：返回0,1,2,……，全不选返回-1
#    复选型：返回类似于[0,3,4]这样的列表，全不选返回空列表([ ])，全选返回[0,1,2,……,N-1](N为列表长度)
#  点“取消”后，返回None

#例子：

#  简易列表Html：
#    print(ListChoice(("<font color=#007f00>绿色</font>","<i>斜体</i>","<b>加粗</b>")*20,['<font color=#ffff00><b>转义</b></font><font color=#00ffff><u>字符</font></u>&#160;&#160;&amp;#%s; <span style="background-color:#afffaf;"><font color=#7f007f>&#%s;</font></span>'%(i,i) for i in range(1,256)],True,TextHeight=150))

#  单选列表Text(圆形选择按钮在左)：
#    print(ListChoice("100选1",["内容"+str(i) for i in range(100)],False,1,3,("放弃","提交","清空")))

#  复选列表Html(方形选择按钮在右)：
#    print(ListChoice(('选择幸运字母',"1.该说明组可以<b><font color=#3f7f3f>&#60;滚动&#62;</font></b>；","2.可以选择一个；<br>3.也可以选择多个；","4.可以都选；<br>5.也可以都不选。"),("<font color=red><span style='background-color:#ffffff;'><big>大</big>白底红色</span></font>","<span style='background-color:#ffff00;'><font color=#0000ff><small>小</small>黄底蓝字</font></font>","<br><sup><span style='background-color:#bfffbf;'><font color=#af00af>上标</font></span></sup>正常<sub><span style='background-color:#000000;'>下标</span></sub><br>",'<span style="background-color:#ffffff;"><font color=#000000>白底黑字</font></span>',"<u>下划线</u>","<del>删除线</del>")*20,True,4,[3,5],None,100))

    if not Button:
        Button=[]
    elif type(Button)==str:
        Button=[Button]
    if ListType in (0,10):
        BtnCnt=1
    elif 0<ListType<5:
        if ListType<3:
            BtnCnt=3
        else:
            BtnCnt=4
    else:
        raise Exception("非法ListType")
    if len(Button)<BtnCnt:
        Button=tuple(Button)+DftBtn[len(Button):BtnCnt]
    MainScreen.List=List
    MainScreen.IsHtml=isHtml
    MainScreen.ListType=ListType
    MainScreen.Button=Button
    MainScreen.Selected=Selected
    if BtnCnt==1:
        btn=""
    elif BtnCnt==3:
        btn=CfAlNoBtn%(Button[1],Button[2])
    else:
        MainScreen.All=not Selected
        btn=CfAlNoBtn%(Button[1],Button[2+bool(Selected)^1])
    if isHtml:
        TxtTyp="html"
        bld=""
    else:
        TxtTyp="text"
        bld=TxtBld
    FgColor="ff0000","0000ff"
    if type(Text)==str:
        Text=[Text]
    TxtScr="\n".join(Text[:4])
    if len(Text)<=1:
        if len(Text)==0:
            TxtScr=""
        else:
            TxtScr=TxtTtl%(TxtTyp,Str2Xml(Text[0]),bld)
    else:
        TxtScr=[TxtTtl%(TxtTyp,Str2Xml(Text[0]),bld)]
        for i in range(1,len(Text)):
            TxtScr.append(TextVw%(TxtTyp,i,TxtTyp,Str2Xml(Text[i]),FgColor[i%2]))
        TxtScr="\n".join(TxtScr)
    FullScreenWrapper2App.show_layout(MainScreen(XML%(TextHeight,TxtScr,btn,Button[0])))
    FullScreenWrapper2App.eventloop()
    return MainScreen.List
__all__=('ListChoice','droid')

# by 乘着船 @ Bilibili at 2025.03-2026.02