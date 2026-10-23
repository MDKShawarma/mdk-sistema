Set WshShell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")
carpeta = fso.GetParentFolderName(WScript.ScriptFullName)
WshShell.Run """" & carpeta & "\IMPRIMIR_SIEMPRE.bat""", 0, False