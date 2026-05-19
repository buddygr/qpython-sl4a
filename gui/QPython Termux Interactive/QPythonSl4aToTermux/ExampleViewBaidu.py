#qpy:quiet
from androidhelper import Android
droid = Android()

print(droid.termuxStartService())
print(droid.termuxRunCommand(
  path = '/data/data/com.termux/files/usr/bin/termux-open-url',
  args = ['https://www.baidu.com'],
  workdir = None,
  background = True))