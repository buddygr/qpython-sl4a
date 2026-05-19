#qpy:console
from androidhelper import Android
droid = Android()

print(droid.termuxStartService())
print(droid.termuxRunCommand(
  path = '/data/data/com.termux/files/usr/bin/bash',
  args = ['-c','pkg search python & read'],
  workdir = None,
  background = False))