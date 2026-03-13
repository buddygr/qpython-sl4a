class fakeIO:
    new=[];old=[]
    def flush():
        pass
    def print(x=''):
        fakeIO.write(x+'\n')
        n=''.join(fakeIO.new)
        fakeIO.new.clear()
        o=''.join(fakeIO.old)
        fakeIO.old.clear()
        if ynText(n,o,('继续(保留)','复制','继续(清除)'),'on'):
            fakeIO.old.extend((o,n))
fakeIO.write=fakeIO.new.append
#替代系统标准输入接口:sys.stdin=fakeIO
#  也可以替代系统普通输入函数:input=fakeIO.input
#替代系统标准输出接口:sys.stdout=sys.stderr=fakeIO
#  之后写入输出内容进缓冲区:
#    print(...)
#    sys.stdout.write(...)
#  显示输出内容:fakeIO.print()
#    利用系统输入暂停时显示输出:input=fakeIO.print
#  也可以直接替代系统普通输出函数:print=fakeIO.print,但只支持一个str参数
try:
    #标准输入/长文本
    from .LongText import LongText
    fakeIO.input=LongText
except:
    from Dialog._ import Input
    fakeIO.input=lambda msg='':Input('',msg)
fakeIO.readline=fakeIO.input
try:
    #标准输出
    from .ynText import ynText
    fakeIO.old.append('蓝:最新输出,红:历史输出\n')
except:
    from Dialog._ import Button
    ynText=lambda New,Old,btn,Ord:Button('',Old+New,(btn[0],btn[2]))==1
try:
    #列表按钮
    from .RadioCmd import RadioCmd
    fakeIO.List=RadioCmd
except:
    from Dialog.Choice import List
    fakeIO.List=List
try:
    #短文本
    from .MultText import MultText
    def _Ipt(Ttl='',Msg='',Txt=''):
        Rst=MultText(Ttl,(Msg,Txt))
        if Rst!=None:
            Rst=Rst[0]
        return Rst
    fakeIO.Input=_Ipt
    del _Ipt
except:
    from Dialog._ import Input
    fakeIO.Input=Input
try:
    #三键按钮
    from .ButtonText import ButtonText
    fakeIO.Button=ButtonText
except:
    from Dialog._ import Button
    fakeIO.Button=Button