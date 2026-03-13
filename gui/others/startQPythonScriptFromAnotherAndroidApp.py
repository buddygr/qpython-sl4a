from androidhelper import *
droid=Android()
from qpy import projects,scripts
droid.startActivity(
    action='android.intent.action.VIEW',
    extras={
    'path':projects+'/Media_QPy',
    'isProj':True,
    'arg':None
    },
    packagename=droid.getSysInfo().result['packageName'],
    classname='org.qpython.qpy.main.activity.HomeMainActivity'
)
droid.startActivity(
    action='android.intent.action.VIEW',
    extras={
    'path':scripts+'/LongText_url_QPy.py',
    'isProj':False,
    'arg':None
    },
    packagename=droid.getSysInfo().result['packageName'],
    classname='org.qpython.qpy.main.activity.HomeMainActivity'
)