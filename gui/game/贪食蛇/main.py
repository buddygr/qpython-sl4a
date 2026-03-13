#qpy:quiet
#脚本路径 Script Path：qpython/projects3/snake/main.py
from qsl4ahelper.fullscreenwrapper2 import *
from android import *
import time
l=__file__[:__file__.rfind('/')+1]
b=l+'config.ini'
from os import environ
l+='language/'+environ['LANG'][:2]+'.ini'
l=eval(open(l).read())
#标题 Title
Title=l['Title']
#作者 Author
i=Title+' (SL4A Game) in QPython by 乘着船 @ Bilibili'
#平台要求 Platform Requirement：QPython Plus >= 3.7.7
N={}
try:
    exec(open(b).read(),N,N)
    D=N['stepDuration']
except:
    open(b,'w').write('''
titleFontSize=8
matrixFontSize=6
matrixSize=20
stepDuration=0.5
highScore=0
''')
    exec(open(b).read(),N,N)
BT="""
    <RadioButton
        android:id="@+id/btn%s"
        android:textAllCaps="false"
		android:layout_width="fill_parent"
		android:layout_height="fill_parent"
		android:text="%s"
		android:textStyle="bold"
		android:background="#%s"
		android:textColor="#ffffffff"
		android:layout_weight="1"
		android:gravity="center"/>
"""
XML=f"""<?xml version="1.0" encoding="utf-8"?>
<LinearLayout
	android:layout_width="fill_parent"
	android:layout_height="fill_parent"
	android:background="#406090"
	android:orientation="vertical"
	xmlns:android="http://schemas.android.com/apk/res/android"
	xmlns:qpython="http://www.qpython.org">
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
		android:id="@+id/Title"
		android:layout_width="fill_parent"
		android:layout_height="wrap_content"
		android:textSize="{N['titleFontSize']}dp"
		android:text="%s"
		android:textColor="#0000ff"
		android:background="#ffffaf"
		android:layout_weight="1"
		android:gravity="center"
	/>
	<TextView
		android:id="@+id/Text"
		android:layout_width="fill_parent"
		android:layout_height="wrap_content"
		android:textSize="{N['matrixFontSize']}dp"
		qpython:html="%s"
		android:textColor="#af7f00"
		android:background="#ffffff"
		android:layout_weight="1"
		android:gravity="center"
	/>
	</LinearLayout>
	</ScrollView>
    </LinearLayout>
	<LinearLayout
		android:layout_width="fill_parent"
		android:layout_height="100dp"
		android:orientation="horizontal"
		android:layout_weight="8">
""","""
	</LinearLayout>
</LinearLayout>"""
N,D,b=N['matrixSize'],N['stepDuration'],N['highScore']
class MainScreen(Layout):
    def on_show(self):
        global View
        View=self.views
        for i in range(5):
            v=View['btn%s'%i]
            v.add_event(click_EventHandler(v,self.do))
            v.textOn=v.textOff=v.text
    def on_close(self):
        pass
    def do(self,view,dummy):
        view.checked='false'
        t=view.text
        while True:
            r=move(t)
            if r==None:return
            View.Text.html=r[0]
            View.Title.html=r[1]
            time.sleep(D)
            if rsla('fullGetProperties',Btis,'checked')!=allFalse or life<0:
                break
#初始化代码部分 Initialize Code Part
import os,random
def randN():
    return random.randint(0,N-1)
Btts='←↑x↓→'
Btcs='7f3f3f','7f7f00','3f3f7f','007f7f','7f007f'
Btis=[]
allFalse=['false']*5
FullScreenWrapper2App.initialize(droid)
def Str2Xml(s):
    t=[];r=t.append
    for i in s:
        j=ord(i)
        if j<256 and not (i.isalpha() or i.isdigit()):
            r('&#');r(str(j));r(";")
        else:
            r(i)
    return ''.join(t)
#游戏说明 Game Instructions
l['Instruction']=l['Instruction'][:7]+(b,)+l['Instruction'][7:]
text="""<font color=#af00af>
%s
</font>
<font color=#007f00>● = %s</font>
<font color=red>● = %s</font>
<font color=#ff7f00>● = %s </font>
<font color=blue>◆ = %s </font>
<font color=#5f5f5f>◆ = %s</font>

%s：%s
x = %s
"""%l['Instruction']
b=('○'*N+'\n')*N
text=b+text+i
text=text.replace('\n','<br>')
text=Str2Xml(text)
b=[]
for i in range(5):
    b.append(BT%(i,Btts[i],Btcs[i]))
    Btis.append('btn%s'%i)
b=''.join(b)
b=[XML[0]%(Title,text),b,XML[1]]
b=''.join(b)
food=[randN(),randN()]
snake=[[randN(),randN()]]
life=1#生命值 Health
text=''
#贪食蛇运动函数 Snake Move Function
def move(a):
  global life,text,food
  if life<=0:
      if a=='x':
          return Close()
      elif life<0:
          jsla('executeQPy',__file__)
          return Close()
      life=-1
      writeHighScore()
      time.sleep(D)
      return text+l['ExitTip'],Title+'<br><small><font color=#ff00ff>%s</font><br><font color=#ff3f3f>%s</font></small>'%(l['LengthHealth']%(len(snake),0),l['GameOver'])
  matrix = [(['○']*N) for i in range(N)]
  if a=='↑':
      snake.append([(snake[-1][0]-1)%N,snake[-1][1]])
      del snake[0]
  elif a=='↓':
      snake.append([(snake[-1][0]+1)%N,snake[-1][1]])
      del snake[0]
  elif a=='←':
     snake.append([snake[-1][0],(snake[-1][1]-1)%N])
     del snake[0]
  elif a=='→':
     snake.append([snake[-1][0],(snake[-1][1]+1)%N])
     del snake[0]
  elif a=='x':
      return close()
  for i in snake:
      matrix[i[0]][i[1]]='<font color=#007f00>●</font>'
  if food in snake:
      i='#5f5f5f'
  else:
      i='blue'
  matrix[food[0]][food[1]]='<font color=%s>◆</font>'%i
  w=1
  for i in range(len(snake)-1):
      for j in range(i+1,len(snake)):
          if snake[i]==snake[j]:
              k=snake[j]
              matrix[k[0]][k[1]]='<font color=red>●</font>'
              if w:
                w=0
                life-=1
                jsla('makeToast',l['LifeDown'])
  if snake[-1]==food:
    k=snake[0]
    snake.insert(0,[k[0],k[1]])
    matrix[food[0]][food[1]]='<font color=#ff7f00>●</font>'
    food=[randN(),randN()]
    life+=1
    if w:
        jsla('makeToast',l['LifeUp'])
    else:
        jsla('makeToast',l['LifeUpDown'])
  text=[]
  for i in matrix:
      text.append(''.join(i))
  text='<br>'.join(text)
  i=N*life//len(snake)
  i='%s<br><small><font color=#ff00ff>%s</font><br><font color=#00ff00>%s</font><font color=#ff3f3f>%s</font></small>'%(Title,l['LengthHealth']%(len(snake),life),'█'*i,'█'*(N-i))
  return text,i
#贪食蛇退出函数 Snake Exit Function
def close():
    jsla("dialogCreateAlert",Title,l['ExitConfirm'])
    jsla("dialogSetNegativeButtonText",l['pause'])
    jsla("dialogSetPositiveButtonText",l['exit'])
    jsla("dialogSetNeutralButtonText",l['restart'])
    jsla("dialogShow")
    writeHighScore()
    try:
        r=esla("dialogGetResponse")['which']
    except:
        r='none'
    if r=='positive':
        Close()
    elif r=='neutral':
        jsla('executeQPy',__file__)
        Close()
def Close():
    FullScreenWrapper2App.close_layout()
    exit()
def writeHighScore():
    b=__file__[:__file__.rfind('/')+1]+'config.ini'
    n={}
    exec(open(b).read(),n,n)
    if n['highScore']>=len(snake):
        return
    n['highScore']=len(snake)
    s=[]
    for i in n:
        if i[0]!='_':
            s.append(i+'='+str(n[i]))
    open(b,'w').write('\n'.join(s))
#启动贪食蛇游戏 Start Snake Game
FullScreenWrapper2App.show_layout(MainScreen(b,title=Title))
FullScreenWrapper2App.eventloop()
#视频演示 Video Demo：https://www.bilibili.com/video/BV1rR4y1j7HF
#参考原作者文章 Refer to the original author's article：
#https://www.cnblogs.com/ksxh/p/9192124.html