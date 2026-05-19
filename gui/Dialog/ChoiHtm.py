from ._ import *

OCAN=('OK','Cancel','All','None')
CC=('Continue','Cancel')
OCE=('OK','Cancel','Edit')
ABCD=('<font color=red>Apple</font>','<font color=green>Banana<font>','<font color=blue>Cat</font>','Dog')
PNNs={'positive':1,'negative':0,'neutral':None}
PNNn=(1,1,0,None)

import os
isfile=os.path.isfile
isdir=os.path.isdir
listdir=os.listdir

def Input(title="Value",message="Please enter <big><font color=#ff00ff>a</font></big> value :",default=""):
    return rsla("dialogGetInput",title,message,default,True)

def List(title='Which is your choose ?',message="Choice <big><font color=#ff00ff>a</font></big> Fruit :",item=ABCD):
    jsla("dialogCreateAlert",title,message)
    jsla("dialogSetMessageIsHtml")
    jsla("dialogSetItems",item)
    jsla("dialogShow")
    try:
        return rsla("dialogGetResponse")['item']
    except:
        return None

def OneChoice(title='Which is animal ?',message='Choose <big><font color=#ff00ff>an</font></big> animal',item=ABCD,default=None,returnValue=False,button=OC):
    if default==None:
        default=-1
    while True:
        jsla("dialogCreateAlert",title,message)
        jsla("dialogSetMessageIsHtml")
        jsla("dialogSetSingleChoiceItems",item,default)
        ButtonText(button)
        jsla("dialogShow")
        try:
            w=Which()
        except:
            return None
        default=rsla("dialogGetSelectedItems")[0]
        if w==1:
            if returnValue:
                return item[default]
            else:
                return default
        else:
            return None
        
def MulChoice(title='Which are not fruit ?',message='Choose <big><font color=#ff00ff>all not</font></big> fruit',item=ABCD,default=(),returnValue=False,button=OCAN):
    All=tuple(range(len(item)))
    AN=2
    if default==None:
        default=[]
    while True:
        jsla("dialogCreateAlert",title,message)
        jsla("dialogSetMessageIsHtml")
        jsla("dialogSetMultiChoiceItems",item,default)
        ButtonText((button[0],button[1],button[AN]))
        jsla("dialogShow")
        try:
            w=Which()
        except:
            return None
        default=rsla("dialogGetSelectedItems")
        if w==1:
            rst=[]
            for i in default:
                if returnValue:
                    rst.append(item[i])
                else:
                    rst.append(i)
            return rst
        elif w==0:
            if AN==2:
                default=All
                AN=3
            else:
                default=()
                AN=2
        else:
            return None

def ynChoice(title='Math Problem',message='1+1=<big><font color=#ff00ff>3</font></big> ?',button=YNC):
    jsla("dialogCreateAlert",title,message)
    jsla("dialogSetMessageIsHtml")
    ButtonText(button)
    jsla("dialogShow")
    try:
        return PNNs[rsla("dialogGetResponse")['which']]
    except:
        return PNNn[len(button)]

def RunChoice(title='',message='Choose <big><font color=#ff00ff>one</font></big> to run',item=('One','Mul','YN','Pause','Exit'),run=(OneChoice,MulChoice,'print(ynChoice())','input()',None)):
    while True:
        a=List(title,message,item)
        if a==None:
            break
        a=run[a]
        if type(a)==str:
            exec(a)
        elif a==None:
            break
        else:
            a()

def FileChoice(title='选择一个文件(夹)',message='当前路径：',Path='/sdcard',FileName='',button=OCE):
    d=Path=PathStrip(Path)
    while True:
        try:
            l=listdir(d)
        except:
            l=[]
        D=[];F=[]
        l.sort()
        for i in l:
            j=d+i
            if isdir(j):
                D.append(d+i+'/')
            else:
                F.append(d+i)
        b=[]
        for i in D:
            b.append('<big><font color=#ffff00>'+i.rsplit('/',2)[-2]+'</font></big>:目录')
        for i in F:
            b.append('<big><font color=#ffaf30>'+i.rsplit('/',1)[-1]+'</font></big>:文件')
        l=len(b)
        n=len(D)
        m='%s\n<font color=#ff30ff>%s</font>'%(message,d)
        c=["<font color=#afafff>&lt;文件(夹)选择器功能键&gt;</font>"]
        c=List(title,m,c+b)
        if c==None:
            d=PathUp(d)
            continue
        elif c>0:
            c-=1
            if c<n:
                d=D[c]
                continue
            else:
                return F[c-n]
            continue
        c=List('选择要操作的功能',m,('选择该文件夹','向上一级文件夹','手动输入文件名','继续选择文件(夹)','回到初始路径 <font color=#ff30ff>'+Path+"</font>",'取消'))
        if c==0:
            return d
        elif c==1:
            d=PathUp(d)
        elif c==2:
            e=Input('输入文件名 :','当前路径 : <font color=#ff30ff>'+d+"</font>",FileName)
            if e!=None:
                return d+e
        elif c==4:
            d=Path
            continue
        elif c==5:
            return

def PathUp(x):
    y=x.rfind('/',0,-1)
    return x[:y+1]

def PathStrip(Path):
    Path=Path.strip()
    if Path=='' or Path[-1]!='/':
        Path+='/'
    return Path