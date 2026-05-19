#qpy:qpyapp:10
from androidhelper import Android
droid = Android()

from time import sleep
import os
from random import randint

print(droid.termuxStartService())
print(droid.termuxGetQSL4A())
path=__file__[:__file__.rfind('/')+1]+'TermuxRunQPythonSl4a/'
file=os.listdir(path)
file=file[randint(0,len(file)-1)]
droid.makeToast(file,0,None)
sleep(3)
print(droid.termuxRunCommand(
  path = '/data/data/com.termux/files/usr/bin/python',
  args = [path+file],
  workdir = None,
  background = False))