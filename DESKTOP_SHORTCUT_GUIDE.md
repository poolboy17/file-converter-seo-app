# 🖥️ Desktop Shortcut Setup Guide

This guide will help you create a desktop shortcut to launch the File Converter SEO App with a single click.

## ✨ Quick Setup (2 Steps)

### Step 1: Create Desktop Shortcut
**Double-click this file:**
```
Create_Desktop_Shortcut.vbs
```

This will:
- ✅ Create a shortcut on your Desktop named "File Converter SEO"
- ✅ Use a custom icon (blue document with arrow)
- ✅ Optionally add a Start Menu shortcut

### Step 2: Use Your App!
**Double-click the Desktop shortcut:**
- The app will start automatically
- Your browser will open to http://localhost:8501
- Ready to convert files!

## 📁 Files Created

| File | Purpose |
|------|---------|
| `File_Converter_SEO.bat` | Main launcher (can be run directly) |
| `Create_Desktop_Shortcut.vbs` | Creates desktop shortcut |
| `app_icon.ico` | Custom app icon (auto-generated) |
| `app_icon.png` | Icon preview |
| `generate_icon.py` | Icon generator script |

## 🎯 Using the App

### From Desktop Shortcut (Recommended)
1. **Double-click** "File Converter SEO" on your desktop
2. Wait for terminal window to open
3. App opens in browser automatically
4. Start converting files!

### From Batch File Directly
1. Navigate to app folder
2. **Double-click** `File_Converter_SEO.bat`
3. App starts in terminal
4. Browser opens automatically

### From Windows Start Menu (Optional)
1. Press **Windows Key**
2. Type "File Converter SEO"
3. Click to launch

## 🛠️ Customization

### Change Icon
1. Replace `app_icon.ico` with your own icon file
2. Re-run `Create_Desktop_Shortcut.vbs`

Or regenerate the default icon:
```powershell
.\.venv\Scripts\python.exe generate_icon.py
```

### Move Shortcut
You can move the desktop shortcut anywhere:
- Pin to Taskbar (right-click shortcut → Pin to Taskbar)
- Add to Quick Access
- Copy to any folder

### Change App Name
1. Right-click the desktop shortcut
2. Select "Rename"
3. Enter new name (e.g., "File Converter", "SEO Tool", etc.)

## 🔧 Advanced Options

### Silent Launch (No Terminal Window)
Create `File_Converter_SEO_Silent.vbs`:
```vbscript
Set WshShell = CreateObject("WScript.Shell")
WshShell.Run """File_Converter_SEO.bat""", 0, False
```
This hides the terminal window.

### Run on Startup
1. Press `Win + R`
2. Type `shell:startup`
3. Copy the desktop shortcut to the Startup folder

### Run with Custom Port
Edit `File_Converter_SEO.bat` and change the last line to:
```batch
streamlit run app.py --server.port 9000
```

### Pin to Taskbar
Right-click the desktop shortcut → **Pin to Taskbar**

Now you can launch with a single click from your taskbar!

## 🆘 Troubleshooting

### Shortcut Not Created
**Problem:** VBS script doesn't create shortcut  
**Solution:** 
1. Check if you have permission to write to Desktop
2. Try running `Create_Desktop_Shortcut.vbs` as Administrator
3. Manually create shortcut (see below)

### Manual Shortcut Creation
If the VBS script doesn't work:

1. Right-click on your Desktop
2. Select **New** → **Shortcut**
3. Browse to and select: `File_Converter_SEO.bat`
4. Click **Next**
5. Name it: "File Converter SEO"
6. Click **Finish**

To add the icon:
1. Right-click the shortcut → **Properties**
2. Click **Change Icon**
3. Click **Browse**
4. Navigate to app folder and select `app_icon.ico`
5. Click **OK** twice

### Icon Not Showing
**Problem:** Shortcut shows default icon  
**Solution:**
```powershell
# Regenerate the icon
.\.venv\Scripts\python.exe generate_icon.py

# Recreate the shortcut
Create_Desktop_Shortcut.vbs
```

### App Won't Start
**Problem:** Double-clicking does nothing  
**Solution:** Check these:

1. **Virtual environment exists:**
   ```
   .venv\Scripts\activate.bat
   ```

2. **Dependencies installed:**
   ```powershell
   .\.venv\Scripts\python.exe -m pip install -r requirements-prod.txt
   ```

3. **Check for errors:**
   Open PowerShell in app folder and run:
   ```powershell
   .\File_Converter_SEO.bat
   ```
   Look for error messages in the terminal.

### Port Already in Use
**Problem:** "Port 8501 is already in use"  
**Solution:**
```powershell
# Find and kill the process
netstat -ano | findstr :8501
taskkill /PID <PID> /F

# Or change the port in File_Converter_SEO.bat
```

## 📊 What Happens When You Launch

1. **Batch file runs** → `File_Converter_SEO.bat`
2. **Changes to app directory** → Ensures correct location
3. **Activates virtual environment** → `.venv\Scripts\activate.bat`
4. **Checks dependencies** → Installs if missing
5. **Starts Streamlit** → `streamlit run app.py`
6. **Opens browser** → http://localhost:8501
7. **Ready to use!** → Convert your files

## 🎨 Icon Details

The custom icon features:
- 📄 Blue document with fold
- ➡️ Red arrow (conversion symbol)
- 🏷️ "SEO" text at bottom
- Multiple sizes (16x16 to 256x256)
- Windows ICO format

Preview the icon by opening `app_icon.png` in any image viewer.

## 💡 Pro Tips

### Quick Access
Create shortcuts in multiple locations:
- Desktop (main shortcut)
- Taskbar (for quick access)
- Start Menu (for search)
- Quick Access toolbar

### Multiple Instances
You can run multiple instances on different ports:
1. Copy `File_Converter_SEO.bat` to `File_Converter_SEO_9000.bat`
2. Edit the new file to use port 9000
3. Create another shortcut pointing to the new batch file

### Share with Team
Package the entire folder and share:
1. Zip the app folder
2. Share with colleagues
3. They just need to:
   - Extract the folder
   - Double-click `Create_Desktop_Shortcut.vbs`
   - Start using!

## 🎯 Summary

| Action | Command |
|--------|---------|
| **Create shortcut** | Double-click `Create_Desktop_Shortcut.vbs` |
| **Launch app** | Double-click desktop shortcut |
| **Stop app** | Press `Ctrl+C` in terminal or close window |
| **Regenerate icon** | `.venv\Scripts\python generate_icon.py` |
| **Manual launch** | Double-click `File_Converter_SEO.bat` |

## 🎉 You're All Set!

Your app is now accessible from your desktop with a single click, just like any other Windows application!

**Desktop shortcut** ✅ **Custom icon** ✅ **One-click launch** ✅
