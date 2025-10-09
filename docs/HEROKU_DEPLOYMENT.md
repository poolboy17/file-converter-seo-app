# Heroku Deployment Guide

This guide covers deploying the File Converter SEO App to Heroku.

## Prerequisites

1. **Heroku Account**: Sign up at [heroku.com](https://www.heroku.com/)
2. **Heroku CLI**: Install from [devcenter.heroku.com/articles/heroku-cli](https://devcenter.heroku.com/articles/heroku-cli)
3. **Git**: Ensure your code is in a Git repository

## Deployment Files

The following files are configured for Heroku deployment:

- **`Procfile`**: Defines the command to start the app
- **`runtime.txt`**: Specifies Python version (3.12.3)
- **`setup.sh`**: Configures Streamlit for Heroku environment
- **`requirements-prod.txt`**: Production dependencies only (lighter than full requirements.txt)
- **`.slugignore`**: Excludes unnecessary files from deployment (tests, docs, etc.)
- **`app.json`**: App metadata for Heroku Button deployment
- **`heroku.yml`**: Alternative deployment configuration

## Quick Deployment Steps

### Method 1: Heroku CLI (Recommended)

1. **Login to Heroku**:
   ```bash
   heroku login
   ```

2. **Create a new Heroku app**:
   ```bash
   heroku create your-app-name
   # Or let Heroku generate a name:
   # heroku create
   ```

3. **Deploy to Heroku**:
   ```bash
   git push heroku main
   ```

4. **Open your app**:
   ```bash
   heroku open
   ```

### Method 2: GitHub Integration

1. Go to your [Heroku Dashboard](https://dashboard.heroku.com/)
2. Click **"New"** → **"Create new app"**
3. Enter app name and region
4. Under **"Deployment method"**, select **"GitHub"**
5. Connect your GitHub repository
6. Enable **"Automatic deploys"** from main branch
7. Click **"Deploy Branch"**

### Method 3: Heroku Button

Add this to your README.md to enable one-click deployment:

```markdown
[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)
```

## Configuration

### Using Production Requirements

By default, Heroku uses `requirements.txt`. To use the lighter production requirements:

```bash
# Rename files temporarily
mv requirements.txt requirements-dev.txt
mv requirements-prod.txt requirements.txt

# Deploy
git add .
git commit -m "Switch to production requirements"
git push heroku main

# Restore files if needed
mv requirements.txt requirements-prod.txt
mv requirements-dev.txt requirements.txt
```

### Environment Variables

Set environment variables using Heroku CLI:

```bash
heroku config:set STREAMLIT_SERVER_HEADLESS=true
heroku config:set STREAMLIT_BROWSER_GATHER_USAGE_STATS=false
```

Or via the Heroku Dashboard → Settings → Config Vars

### Custom Domain

To use a custom domain:

```bash
heroku domains:add www.yourdomain.com
```

Follow the DNS configuration instructions provided.

## Monitoring & Maintenance

### View Logs

```bash
# View recent logs
heroku logs --tail

# View last 100 lines
heroku logs -n 100
```

### Restart the App

```bash
heroku restart
```

### Scale Dynos

```bash
# Scale to 1 web dyno
heroku ps:scale web=1

# Scale down (sleep mode)
heroku ps:scale web=0
```

### Check App Status

```bash
heroku ps
```

## VS Code Extensions for Heroku

Install these extensions for better Heroku development experience:

1. **Heroku CLI Integration** (`ms-azuretools.vscode-azurefunctions`)
2. **Heroku Logs** (`manojkumar.heroku`)
3. **Heroku Postgres** (`ckolkman.vscode-postgres`)

Install via VS Code or command line:
```bash
code --install-extension ms-azuretools.vscode-azurefunctions
```

## Troubleshooting

### Build Failed

1. Check Heroku logs: `heroku logs --tail`
2. Verify Python version in `runtime.txt` matches your local version
3. Ensure all dependencies are in `requirements.txt`

### App Crashes on Startup

1. Check logs for errors: `heroku logs --tail`
2. Verify `Procfile` is correct
3. Test locally with: `streamlit run app.py`

### Port Binding Issues

Heroku assigns a dynamic port via `$PORT` environment variable. The `Procfile` is already configured to use this:

```
--server.port=$PORT --server.address=0.0.0.0
```

### Memory Issues

If your app exceeds memory limits:

1. Upgrade to a higher dyno tier
2. Optimize memory usage in converters
3. Add `.slugignore` to reduce slug size

### Slow Performance

1. Upgrade dyno type: `heroku ps:type web=standard-1x`
2. Enable caching in Streamlit (already implemented)
3. Consider using Heroku Redis for session storage

## Cost Optimization

### Free Tier

Heroku's Eco dynos ($5/month) provide:
- 1000 dyno hours/month
- Automatic sleep after 30 mins of inactivity
- Good for testing/small projects

### Production Recommendations

For production apps:
- **Basic Dyno** ($7/month): No sleeping, better performance
- **Standard Dynos** ($25+/month): More memory, better CPU
- Add Heroku Postgres if you need database
- Consider Heroku Redis for caching

## Security Best Practices

1. **Never commit secrets**: Use environment variables
2. **Use HTTPS**: Heroku provides SSL by default
3. **Set secure headers**: Configure in `setup.sh`
4. **Regular updates**: Keep dependencies up to date
5. **Monitor logs**: Set up log alerts for errors

## Performance Optimization

1. **Enable Streamlit caching**: Already implemented with `@st.cache_resource`
2. **Optimize file sizes**: Use `.slugignore` to reduce deployment size
3. **Minimize dependencies**: Use `requirements-prod.txt` in production
4. **Use CDN**: For static assets (images, CSS)

## Continuous Deployment

### Automatic Deploys from GitHub

1. Go to Heroku Dashboard → Deploy tab
2. Connect GitHub repository
3. Enable "Automatic deploys"
4. Optional: Enable "Wait for CI to pass" if using GitHub Actions

### Pre-deployment Checks

Add to `.github/workflows/heroku-deploy.yml`:

```yaml
name: Deploy to Heroku

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: akhileshns/heroku-deploy@v3.12.14
        with:
          heroku_api_key: ${{secrets.HEROKU_API_KEY}}
          heroku_app_name: "your-app-name"
          heroku_email: "your-email@example.com"
```

## Additional Resources

- [Heroku Python Support](https://devcenter.heroku.com/articles/python-support)
- [Streamlit Deployment Guide](https://docs.streamlit.io/streamlit-community-cloud/get-started/deploy-an-app)
- [Heroku CLI Commands](https://devcenter.heroku.com/articles/heroku-cli-commands)
- [Heroku Pricing](https://www.heroku.com/pricing)

## Support

For issues specific to this app:
- Open an issue on GitHub
- Check logs: `heroku logs --tail`
- Review Heroku status: [status.heroku.com](https://status.heroku.com/)

For Heroku-specific issues:
- [Heroku Dev Center](https://devcenter.heroku.com/)
- [Heroku Support](https://help.heroku.com/)
