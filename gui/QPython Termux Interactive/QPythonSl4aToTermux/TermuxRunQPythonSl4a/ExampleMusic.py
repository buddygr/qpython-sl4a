from androidhelper import *
droid = Android()
import os
title='QPython SL4A'
print(droid)
music=droid.dialogGetInput(title,'Input a Music File :','/sdcard/music/sound.wav')
print(music)
if not music.result:
    exit()
print(droid.musicPlay(music.result))
info=droid.mediaPlayInfo()
print(info)
droid.dialogShowAlert(title,str(info))
from time import sleep
sleep(5)
print(droid.musicPlayClose())
input('Press Enter to Exit .')