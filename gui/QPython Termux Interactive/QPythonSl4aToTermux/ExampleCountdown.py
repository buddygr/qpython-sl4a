#qpy:qpyapp
from androidhelper import Android
droid = Android()

print(droid.termuxStartService())
print(droid.termuxRunCommand(
  path = '/data/data/com.termux/files/usr/bin/python',
  args = ['-c', '''
from time import sleep
for i in range(10,-1,-1):
    print(i)
    sleep(1)
'''],
  workdir = None,
  background = False))