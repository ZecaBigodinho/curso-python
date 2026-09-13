Set WshShell = CreateObject("WScript.Shell")
WshShell.CurrentDirectory = "e:\chave\curso\CourseForge"
WshShell.Run "pythonw.exe ""e:\chave\curso\CourseForge\courseforge_watcher.py""", 0, False
