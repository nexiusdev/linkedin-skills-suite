Set objShell = CreateObject("Shell.Application")
Set objFSO = CreateObject("Scripting.FileSystemObject")

' Get the script's directory
strScriptPath = objFSO.GetParentFolderName(WScript.ScriptFullName)
strBatchFile = strScriptPath & "\SETUP-AUTOMATION.bat"

' Run the batch file as administrator
objShell.ShellExecute strBatchFile, "", "", "runas", 1
