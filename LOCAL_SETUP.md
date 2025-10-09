# Running the File Converter SEO App Locally

This guide shows you how to run the app on your Windows 11 desktop.

## 🚀 Quick Start (3 Ways to Run)

### Option 1: Double-Click Launcher (Easiest)
1. **Double-click** `run_app.bat` in Windows Explorer
2. The app will start and open in your browser automatically
3. Press `Ctrl+C` in the terminal to stop

### Option 2: PowerShell Launcher
1. **Right-click** `run_app.ps1` → Select **"Run with PowerShell"**
2. The app will start and open in your browser automatically
3. Press `Ctrl+C` in the terminal to stop

### Option 3: From VS Code Terminal
1. Open a terminal in VS Code
2. Run:
   ```powershell
   .\run_app.bat
   ```
3. Press `Ctrl+C` to stop

## 📱 Accessing the App

Once started, the app will automatically open in your default browser at:
- **Local URL:** http://localhost:8501
- **Network URL:** http://YOUR-IP:8501 (accessible from other devices on your network)

## 🛠️ What's Installed

The app uses these main dependencies (production-only):
- **Streamlit 1.50.0** - Web framework
- **BeautifulSoup4** - HTML/XML parsing
- **pandas** - Data processing
- **python-docx** - DOCX file handling
- **lxml** - XML processing
- **PyYAML** - YAML parsing
- **Pillow** - Image processing

## 📂 File Upload Limits

- **Maximum file size:** 50MB per file
- **Supported formats:** CSV, DOCX, TXT, WXR
- **Multiple files:** Yes, upload multiple files at once

## 🔧 Troubleshooting

### App Won't Start

**Problem:** "streamlit is not recognized"
**Solution:** Make sure virtual environment is activated:
```powershell
.\.venv\Scripts\activate
streamlit run app.py
```

### Port Already in Use

**Problem:** "Port 8501 is already in use"
**Solution:** Run on a different port:
```powershell
streamlit run app.py --server.port 8502
```

### Import Errors

**Problem:** "ModuleNotFoundError: No module named 'streamlit'"
**Solution:** Reinstall dependencies:
```powershell
.\.venv\Scripts\activate
pip install -r requirements-prod.txt
```

### Virtual Environment Issues

**Problem:** Virtual environment not working
**Solution:** Recreate it:
```powershell
# Delete old venv
Remove-Item -Recurse -Force .venv

# Create new venv
python -m venv .venv

# Activate it
.\.venv\Scripts\activate

# Install dependencies
pip install -r requirements-prod.txt
```

## 🎯 Tips & Tricks

### Run on Startup
1. Create a shortcut to `run_app.bat`
2. Press `Win + R`, type `shell:startup`, press Enter
3. Move the shortcut to the Startup folder

### Run in Background
```powershell
Start-Process -FilePath "run_app.bat" -WindowStyle Hidden
```

### Stop All Running Instances
```powershell
# Find Streamlit processes
Get-Process | Where-Object {$_.ProcessName -like "*python*"} | Select-Object Id, ProcessName, Path

# Stop specific process (replace PID with actual process ID)
Stop-Process -Id <PID>
```

### Access from Another Computer
1. Find your IP address:
   ```powershell
   ipconfig | Select-String "IPv4"
   ```
2. On the other computer, browse to: `http://YOUR-IP:8501`
3. **Note:** Make sure Windows Firewall allows port 8501

### Custom Port and Settings
```powershell
streamlit run app.py --server.port 9000 --server.address 0.0.0.0
```

## 📊 Performance

### Memory Usage
- **Idle:** ~200MB
- **Processing files:** ~500MB - 1GB (depends on file size)
- **Peak:** ~2GB (for very large files)

### Speed
- **CSV files:** Nearly instant (<1s for most files)
- **DOCX files:** 2-5 seconds (with images)
- **WXR files:** 5-10 seconds (large XML parsing)

## 🔒 Security Notes

When running locally:
- ✅ All data stays on your computer
- ✅ No internet connection required (after initial install)
- ✅ Files are processed in memory only
- ✅ No data is stored permanently (unless you download results)

## 🆚 Local vs Heroku

| Feature | Local (Desktop) | Heroku (Cloud) |
|---------|----------------|----------------|
| **Cost** | Free | $5-7/month |
| **Speed** | Fast | Slower (depends on dyno) |
| **Privacy** | Complete | Data sent to cloud |
| **Access** | Your computer only | Internet (anywhere) |
| **Persistence** | Run as needed | Always running |
| **Setup** | Already done! | Already deployed |

## 📝 Quick Commands Cheat Sheet

```powershell
# Start the app
.\run_app.bat

# Start with custom port
.\.venv\Scripts\activate
streamlit run app.py --server.port 9000

# Check if app is running
netstat -ano | findstr :8501

# View Streamlit help
streamlit --help

# Update dependencies
pip install --upgrade -r requirements-prod.txt

# Check installed packages
pip list

# Test app without browser
streamlit run app.py --server.headless true
```

## 🎨 Customization

### Change Theme
Edit `.streamlit/config.toml`:
```toml
[theme]
primaryColor = "#FF4B4B"
backgroundColor = "#0E1117"
secondaryBackgroundColor = "#262730"
textColor = "#FAFAFA"
font = "sans serif"
```

### Change Port
Edit `.streamlit/config.toml`:
```toml
[server]
port = 8502
```

## 📞 Need Help?

- **Documentation:** Check `README.md` and other docs in the `docs/` folder
- **Issues:** Open an issue on GitHub
- **Logs:** Check the terminal output for error messages

## 🎉 You're All Set!

Your app is ready to run locally on your Windows 11 desktop. Just double-click `run_app.bat` and start converting files!

**No internet required** • **No server costs** • **Complete privacy** • **Run anytime**
