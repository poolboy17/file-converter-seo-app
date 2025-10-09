' ==================================================================
' Create Desktop Shortcut for File Converter SEO App
' ==================================================================
' This script creates a shortcut on your desktop
' Double-click this file to create the shortcut
' ==================================================================

Set WshShell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")

' Get the current script directory
scriptDir = fso.GetParentFolderName(WScript.ScriptFullName)

' Get desktop path
desktopPath = WshShell.SpecialFolders("Desktop")

' Create shortcut path
shortcutPath = desktopPath & "\File Converter SEO.lnk"

' Create the shortcut
Set shortcut = WshShell.CreateShortcut(shortcutPath)

' Set shortcut properties
shortcut.TargetPath = scriptDir & "\File_Converter_SEO.bat"
shortcut.WorkingDirectory = scriptDir
shortcut.Description = "Convert CSV, DOCX, TXT, and WXR files to SEO-optimized Markdown"
shortcut.WindowStyle = 1 ' Normal window

' Try to use custom icon if available, otherwise use default
iconPath = scriptDir & "\app_icon.ico"
If fso.FileExists(iconPath) Then
    shortcut.IconLocation = iconPath & ",0"
Else
    ' Use a default Windows icon (documents icon)
    shortcut.IconLocation = "%SystemRoot%\System32\shell32.dll,70"
End If

' Save the shortcut
shortcut.Save

' Show success message
WScript.Echo "Success!" & vbCrLf & vbCrLf & _
             "Desktop shortcut created:" & vbCrLf & _
             """File Converter SEO""" & vbCrLf & vbCrLf & _
             "You can now double-click the shortcut on your desktop to launch the app!"

' Optionally, also create a Start Menu shortcut
createStartMenu = MsgBox("Would you like to also add a shortcut to the Start Menu?", vbYesNo + vbQuestion, "Start Menu Shortcut")

If createStartMenu = vbYes Then
    startMenuPath = WshShell.SpecialFolders("Programs")
    startShortcutPath = startMenuPath & "\File Converter SEO.lnk"
    
    Set startShortcut = WshShell.CreateShortcut(startShortcutPath)
    startShortcut.TargetPath = scriptDir & "\File_Converter_SEO.bat"
    startShortcut.WorkingDirectory = scriptDir
    startShortcut.Description = "Convert CSV, DOCX, TXT, and WXR files to SEO-optimized Markdown"
    startShortcut.WindowStyle = 1
    
    If fso.FileExists(iconPath) Then
        startShortcut.IconLocation = iconPath & ",0"
    Else
        startShortcut.IconLocation = "%SystemRoot%\System32\shell32.dll,70"
    End If
    
    startShortcut.Save
    
    WScript.Echo "Start Menu shortcut created!" & vbCrLf & _
                 "You can now find ""File Converter SEO"" in your Start Menu."
End If
