from android import jsla,rsla
from time import sleep,time
def ShakePhone(TestSecond=1,IntervalSecond=0.1,NumberOfHits=1):
    jsla('stopSensing')
    jsla('startSensingTimed',2,int(IntervalSecond*1000))
    k=[None]*3
    def Wait():
        global t
        t=time()
        sleep(IntervalSecond-(t-StartTime)%IntervalSecond)
    StartTime=time()
    Wait()
    while t-StartTime<TestSecond:
        a=rsla('sensorsReadAccelerometer')
        if a[0]==None:
            Wait()
            continue
        elif a!=True:
            for j in range(3):
                if k[j]!=None:
                    if abs(eval(a[j])-k[j])>3:
                        NumberOfHits-=1
                        break
                else:
                    k[j]=eval(a[j])
            if NumberOfHits<=0:
                break
            Wait()
            continue
    jsla('stopSensing')
    if NumberOfHits<=0:
        from WinGui.BaseWindow import FullScreenWrapper2App as i
        i.exit_FullScreenWrapper2App()
        return True
    return False
__all__=('ShakePhone',)