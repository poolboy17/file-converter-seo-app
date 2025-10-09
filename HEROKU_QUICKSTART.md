# Heroku Quick Start

## 🚀 Deploy in 3 Steps

### 1. Install Heroku CLI
```bash
# Windows (via PowerShell)
winget install Heroku.HerokuCLI

# Or download from: https://devcenter.heroku.com/articles/heroku-cli
```

### 2. Login & Create App
```bash
heroku login
heroku create your-app-name
```

### 3. Deploy
```bash
git push heroku main
heroku open
```

## ⚡ Quick Commands

```bash
# View logs
heroku logs --tail

# Restart app
heroku restart

# Check status
heroku ps

# Open app in browser
heroku open

# Set environment variable
heroku config:set KEY=value

# View all config
heroku config

# Scale dynos
heroku ps:scale web=1

# Run commands remotely
heroku run bash
```

## 📦 Production Deployment

To use lighter production requirements:

```powershell
# Backup current requirements
cp requirements.txt requirements-dev.txt

# Switch to production
cp requirements-prod.txt requirements.txt

# Commit and deploy
git add requirements.txt
git commit -m "Switch to production dependencies"
git push heroku main

# Restore dev requirements locally
cp requirements-dev.txt requirements.txt
```

## 🔍 Troubleshooting

### Check build logs
```bash
heroku logs --tail
```

### View releases
```bash
heroku releases
heroku releases:info v12
```

### Rollback if needed
```bash
heroku rollback v11
```

## 💰 Cost Optimization

- **Eco Dynos**: $5/month (1000 hours)
- **Basic Dynos**: $7/month (no sleeping)
- **Standard**: $25+/month (production ready)

Free tier tips:
- App sleeps after 30 min inactivity
- Takes ~10s to wake up
- Good for demos/testing

## 🔐 Security

Required environment variables (already configured):
- `STREAMLIT_SERVER_HEADLESS=true`
- `STREAMLIT_BROWSER_GATHER_USAGE_STATS=false`

## 📱 VS Code Extensions Installed

The following extensions are now installed:

```vscode-extensions
pkosta2005.heroku-command,ivangabriele.vscode-heroku,benspaulding.procfile
```

### How to Use:
1. **Heroku CLI**: Press `Ctrl+Shift+P` → Type "Heroku" → Run commands
2. **Status Monitor**: See deployment status in status bar
3. **Procfile Support**: Syntax highlighting for Procfile

## 🎯 One-Click Deploy Button

Add this badge to your README.md:

```markdown
[![Deploy to Heroku](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)
```

## 📚 Full Documentation

See [HEROKU_DEPLOYMENT.md](./HEROKU_DEPLOYMENT.md) for complete guide.
