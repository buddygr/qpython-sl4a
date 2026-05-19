from androidhelper import *
droid = Android()
import os
title='QPython SL4A'
print(droid)
movie=droid.dialogGetInput(title,'Input a Video File :','/sdcard/movies/movie.mp4')
print(movie)
if not movie.result:
    exit()
print(droid.videoPlay(movie.result))
input('Press Enter to Exit .')