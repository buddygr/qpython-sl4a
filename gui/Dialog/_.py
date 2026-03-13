#Dialog 20250616

from android import droid,rsla,jsla

OK=('OK',)
YN=('Yes','No')
OC=('OK','Cancel')
YNC=('Yes','No','Cancel')
PNNS={'positive':1,'negative':-1,'neutral':0}
PNNt=tuple(PNNS)

def Which():
    return PNNS[rsla("dialogGetResponse")['which']]

def ButtonText(button):
    Lc=len(button)
    if Lc>2:jsla("dialogSetNeutralButtonText",button[2])
    if Lc>1:jsla("dialogSetNegativeButtonText",button[1])
    if Lc==0:button=OK
    jsla("dialogSetPositiveButtonText",button[0])

def Button(title='Prompt',message='Are you sure ?',button=YNC):
    jsla("dialogCreateAlert",title,message)
    ButtonText(button)
    jsla("dialogShow")
    try:
        return Which()
    except:
        return 0

def ProgressCreate(title='标题',message='内容', maxValue=100):
    jsla("dialogCreateHorizontalProgress",title,message,maxValue)
    jsla("dialogShow")
def ProgressSet(CurrentValue):
    jsla('dialogSetCurrentProgress',CurrentValue)
def ProgressMax(MaxValue):
    jsla('dialogSetMaxProgress',MaxValue)
def ProgressDis():
    jsla('dialogDismiss')

def SeekBar(Start=50,Max=100,Title='标题',Message='内容',button=OC):
    jsla("dialogCreateSeekBar",Start,Max,Title,"%s\n\n0 ~ %s"%(Message,Max))
    jsla("dialogSetPositiveButtonText",button[0])
    jsla("dialogSetNegativeButtonText",button[1])
    jsla("dialogShow")
    r=rsla("dialogGetResponse")
    try:
        if r['which']=='positive':
            return r['progress']
    except:
        pass

def SpinCreate(title='标题',message='内容'):
  jsla("dialogCreateSpinnerProgress",title, message)
  jsla("dialogShow")
SpinDis=ProgressDis

def Login(title='Login',message=('Username','Password')):
    u=rsla("dialogGetInput",title,message[0])
    if not u:
        return None,None
    p=rsla("dialogGetPassword",title,message[1])
    if not p:
        return None,None
    return u,p

def Password(title="Password",message="Please enter password:"):
    return rsla("dialogGetPassword",title,message)

def setClip(Text):
    jsla('setClipboard',Text)
def getClip():
    return rsla("getClipboard")

def Vibrate(millisecond=250):
    jsla('vibrate',millisecond)
def Notify(title,message):
    jsla('notify',title,message)
def Toast(message):
    jsla('makeToast',message)
def Speak(message):
    jsla('ttsSpeak',message)