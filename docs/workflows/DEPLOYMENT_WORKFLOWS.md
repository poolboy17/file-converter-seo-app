# Deployment Workflows

Complete workflows for deploying the File Converter application to various platforms.

## Table of Contents
1. [Replit Deployment](#replit-deployment)
2. [Docker Deployment](#docker-deployment)
3. [Heroku Deployment](#heroku-deployment)
4. [AWS Deployment](#aws-deployment)
5. [GitHub Pages (Static Export)](#github-pages-static-export)
6. [Custom VPS Deployment](#custom-vps-deployment)

---

## Replit Deployment

### Workflow: Deploy to Replit

**Use Case:** Quick deployment with zero configuration required.

**Prerequisites:**
- Replit account
- GitHub repository with code

**Steps:**

1. **Import Repository**
   - Log into Replit.com
   - Click "Create Repl"
   - Select "Import from GitHub"
   - Enter: `https://github.com/poolboy17/file-converter-seo-app`
   - Click "Import from GitHub"

2. **Configure Repl**
   - Replit auto-detects Python
   - Auto-installs dependencies from `pyproject.toml`
   - Wait for installation to complete

3. **Verify Configuration**
   
   Check `.streamlit/config.toml` exists:
   ```toml
   [server]
   headless = true
   address = "0.0.0.0"
   port = 5000
   ```

4. **Run Application**
   - Click "Run" button
   - Wait for Streamlit to start
   - Application opens in webview

5. **Test Deployment**
   - Upload test file
   - Perform conversion
   - Verify all features work
   - Test SEO optimization

6. **Get Public URL**
   - Replit provides automatic URL
   - Format: `https://your-repl-name.username.repl.co`
   - Share this URL with users

7. **Configure Custom Domain (Optional)**
   - Go to Repl settings
   - Click "Domains"
   - Add custom domain
   - Update DNS records

8. **Enable Always-On (Optional)**
   - Requires Replit subscription
   - Prevents repl from sleeping
   - Ensures 24/7 availability

**Expected Outcome:**
- Application deployed and accessible
- Public URL available
- Auto-scales with traffic

**Cost:** Free tier available, paid plans for always-on

**Time Estimate:** 5-10 minutes

---

## Docker Deployment

### Workflow: Deploy with Docker Container

**Use Case:** Containerized deployment for any cloud platform or local server.

**Prerequisites:**
- Docker installed
- DockerHub account (optional)
- Repository cloned locally

**Steps:**

1. **Create Dockerfile**
   
   Create `Dockerfile` in project root:
   ```dockerfile
   FROM python:3.11-slim
   
   # Set working directory
   WORKDIR /app
   
   # Copy requirements
   COPY pyproject.toml ./
   COPY uv.lock ./
   
   # Install uv and dependencies
   RUN pip install uv && \
       uv sync
   
   # Copy application code
   COPY . .
   
   # Expose Streamlit port
   EXPOSE 5000
   
   # Health check
   HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
     CMD curl -f http://localhost:5000/_stcore/health || exit 1
   
   # Run application
   CMD ["streamlit", "run", "app.py", "--server.port=5000", "--server.address=0.0.0.0"]
   ```

2. **Create .dockerignore**
   ```
   __pycache__
   *.pyc
   .git
   .gitignore
   venv/
   env/
   .venv/
   .pythonlibs/
   .local/
   .cache/
   *.md
   docs/
   ```

3. **Build Docker Image**
   ```bash
   docker build -t file-converter-app:latest .
   ```

4. **Test Locally**
   ```bash
   docker run -p 5000:5000 file-converter-app:latest
   ```
   
   Open `http://localhost:5000` and test

5. **Tag for Registry**
   ```bash
   docker tag file-converter-app:latest username/file-converter-app:1.0.0
   docker tag file-converter-app:latest username/file-converter-app:latest
   ```

6. **Push to DockerHub**
   ```bash
   docker login
   docker push username/file-converter-app:1.0.0
   docker push username/file-converter-app:latest
   ```

7. **Deploy to Cloud**
   
   **AWS ECS:**
   ```bash
   # Create task definition
   aws ecs register-task-definition --cli-input-json file://task-definition.json
   
   # Create service
   aws ecs create-service --cluster my-cluster --service-name file-converter \
     --task-definition file-converter:1 --desired-count 1
   ```
   
   **Google Cloud Run:**
   ```bash
   gcloud run deploy file-converter \
     --image username/file-converter-app:latest \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated
   ```
   
   **Azure Container Instances:**
   ```bash
   az container create \
     --resource-group myResourceGroup \
     --name file-converter \
     --image username/file-converter-app:latest \
     --dns-name-label file-converter-app \
     --ports 5000
   ```

8. **Configure Environment**
   - Set environment variables if needed
   - Configure memory/CPU limits
   - Set up load balancing

9. **Verify Deployment**
   - Access public URL
   - Test all features
   - Monitor logs
   - Check performance

**Expected Outcome:**
- Containerized application
- Scalable deployment
- Consistent across environments

**Time Estimate:** 30-60 minutes

---

## Heroku Deployment

### Workflow: Deploy to Heroku

**Use Case:** Simple PaaS deployment with automatic scaling.

**Prerequisites:**
- Heroku account
- Heroku CLI installed
- Git repository

**Steps:**

1. **Install Heroku CLI**
   ```bash
   # macOS
   brew install heroku/brew/heroku
   
   # Windows
   # Download from heroku.com/downloads
   
   # Linux
   curl https://cli-assets.heroku.com/install.sh | sh
   ```

2. **Login to Heroku**
   ```bash
   heroku login
   ```

3. **Create Heroku App**
   ```bash
   heroku create file-converter-app
   # Or use: heroku create (generates random name)
   ```

4. **Create Procfile**
   
   Create `Procfile` in root:
   ```
   web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
   ```

5. **Create runtime.txt**
   ```
   python-3.11.5
   ```

6. **Update .streamlit/config.toml**
   ```toml
   [server]
   headless = true
   enableCORS = false
   port = 5000
   
   [browser]
   gatherUsageStats = false
   ```

7. **Commit Files**
   ```bash
   git add Procfile runtime.txt .streamlit/config.toml
   git commit -m "Configure for Heroku deployment"
   ```

8. **Deploy to Heroku**
   ```bash
   git push heroku main
   ```

9. **Scale Dyno**
   ```bash
   heroku ps:scale web=1
   ```

10. **Open Application**
    ```bash
    heroku open
    ```

11. **View Logs**
    ```bash
    heroku logs --tail
    ```

12. **Configure Custom Domain (Optional)**
    ```bash
    heroku domains:add www.yourdomain.com
    # Follow instructions to update DNS
    ```

13. **Set Up SSL**
    ```bash
    heroku certs:auto:enable
    ```

**Expected Outcome:**
- Application live on Heroku
- Automatic HTTPS
- Easy scaling options

**Cost:** Free tier available, hobby tier $7/month

**Time Estimate:** 15-30 minutes

---

## AWS Deployment

### Workflow: Deploy to AWS Elastic Beanstalk

**Use Case:** Enterprise-grade deployment with AWS infrastructure.

**Prerequisites:**
- AWS account
- AWS CLI installed
- EB CLI installed

**Steps:**

1. **Install EB CLI**
   ```bash
   pip install awsebcli
   ```

2. **Initialize EB Application**
   ```bash
   eb init -p python-3.11 file-converter-app --region us-east-1
   ```

3. **Create .ebextensions**
   
   Create `.ebextensions/01_streamlit.config`:
   ```yaml
   option_settings:
     aws:elasticbeanstalk:container:python:
       WSGIPath: app:application
     aws:elasticbeanstalk:application:environment:
       PYTHONPATH: "/var/app/current:$PYTHONPATH"
   
   container_commands:
     01_install_dependencies:
       command: "pip install -r requirements.txt"
   ```

4. **Create requirements.txt** (if not exists)
   ```bash
   pip freeze > requirements.txt
   ```

5. **Create Elastic Beanstalk Environment**
   ```bash
   eb create file-converter-env \
     --instance_type t3.small \
     --envvars PORT=5000
   ```

6. **Configure Health Check**
   ```bash
   eb config
   # Add health check URL: /_stcore/health
   ```

7. **Deploy Application**
   ```bash
   eb deploy
   ```

8. **Open Application**
   ```bash
   eb open
   ```

9. **Configure Auto-Scaling**
   - Go to AWS Console
   - Navigate to Elastic Beanstalk
   - Configure capacity:
     - Min instances: 1
     - Max instances: 4
     - Scale up at: 70% CPU
     - Scale down at: 20% CPU

10. **Set Up CloudFront CDN**
    - Create CloudFront distribution
    - Point to EB environment
    - Configure caching rules

11. **Configure Custom Domain**
    - Go to Route 53
    - Create hosted zone
    - Add CNAME record to EB environment

12. **Enable HTTPS**
    - Request SSL certificate in ACM
    - Attach to load balancer
    - Redirect HTTP to HTTPS

**Expected Outcome:**
- Production-grade deployment
- Auto-scaling enabled
- CDN for better performance
- Custom domain with HTTPS

**Cost:** Varies based on usage (~$20-100/month)

**Time Estimate:** 1-2 hours

---

## GitHub Pages (Static Export)

### Workflow: Deploy Documentation Site

**Use Case:** Host project documentation and demo on GitHub Pages.

**Note:** This doesn't deploy the Streamlit app itself, but creates a static site for documentation.

**Steps:**

1. **Create Documentation Site**
   ```bash
   mkdir -p gh-pages
   cd gh-pages
   ```

2. **Copy Documentation**
   ```bash
   cp ../README.md ./index.md
   cp -r ../docs .
   cp ../CONTRIBUTING.md .
   cp ../LICENSE .
   ```

3. **Create _config.yml**
   ```yaml
   title: File Converter with SEO
   description: Multi-format document converter
   theme: jekyll-theme-cayman
   
   markdown: kramdown
   
   navigation:
     - title: Home
       url: /
     - title: Documentation
       url: /docs/
     - title: Workflows
       url: /docs/workflows/
     - title: Contributing
       url: /CONTRIBUTING
   ```

4. **Create index.md**
   ```markdown
   ---
   layout: default
   title: Home
   ---
   
   # File Converter with SEO Optimization
   
   [View on GitHub](https://github.com/poolboy17/file-converter-seo-app)
   
   [Documentation](docs/) | [Workflows](docs/workflows/) | [Contributing](CONTRIBUTING)
   
   ## Features
   
   - Convert DOCX, CSV, TXT, WXR to Markdown/HTML
   - SEO optimization with scoring
   - Static site generation
   - Batch processing
   
   ## Quick Start
   
   ```bash
   git clone https://github.com/poolboy17/file-converter-seo-app.git
   cd file-converter-seo-app
   pip install -r requirements.txt
   streamlit run app.py
   ```
   
   ## Demo
   
   [Try Demo on Replit](https://replit.com/@username/file-converter-app)
   ```

5. **Create gh-pages Branch**
   ```bash
   git checkout --orphan gh-pages
   git add .
   git commit -m "Initial GitHub Pages site"
   git push origin gh-pages
   ```

6. **Enable GitHub Pages**
   - Go to repository settings
   - Navigate to "Pages"
   - Source: Deploy from branch
   - Branch: gh-pages
   - Folder: / (root)
   - Click Save

7. **Wait for Deployment**
   - GitHub builds site (1-2 minutes)
   - Site available at: `https://username.github.io/file-converter-seo-app`

8. **Configure Custom Domain (Optional)**
   - Add CNAME file with your domain
   - Update DNS with GitHub IPs
   - Enable HTTPS in settings

**Expected Outcome:**
- Documentation site live
- Automatic updates on push
- Free hosting

**Time Estimate:** 20-30 minutes

---

## Custom VPS Deployment

### Workflow: Deploy to Ubuntu VPS

**Use Case:** Full control over infrastructure, self-hosted solution.

**Prerequisites:**
- VPS with Ubuntu 22.04
- Root/sudo access
- Domain name (optional)

**Steps:**

1. **Connect to VPS**
   ```bash
   ssh root@your-vps-ip
   ```

2. **Update System**
   ```bash
   apt update && apt upgrade -y
   ```

3. **Install Python 3.11**
   ```bash
   apt install python3.11 python3.11-venv python3-pip -y
   ```

4. **Install Nginx**
   ```bash
   apt install nginx -y
   systemctl enable nginx
   ```

5. **Create App User**
   ```bash
   adduser streamlit
   usermod -aG sudo streamlit
   su - streamlit
   ```

6. **Clone Repository**
   ```bash
   cd /home/streamlit
   git clone https://github.com/poolboy17/file-converter-seo-app.git
   cd file-converter-seo-app
   ```

7. **Create Virtual Environment**
   ```bash
   python3.11 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

8. **Create Systemd Service**
   
   Create `/etc/systemd/system/streamlit.service`:
   ```ini
   [Unit]
   Description=Streamlit File Converter
   After=network.target
   
   [Service]
   Type=simple
   User=streamlit
   WorkingDirectory=/home/streamlit/file-converter-seo-app
   Environment="PATH=/home/streamlit/file-converter-seo-app/venv/bin"
   ExecStart=/home/streamlit/file-converter-seo-app/venv/bin/streamlit run app.py --server.port=8501
   Restart=always
   
   [Install]
   WantedBy=multi-user.target
   ```

9. **Enable and Start Service**
   ```bash
   systemctl daemon-reload
   systemctl enable streamlit
   systemctl start streamlit
   systemctl status streamlit
   ```

10. **Configure Nginx**
    
    Create `/etc/nginx/sites-available/streamlit`:
    ```nginx
    server {
        listen 80;
        server_name yourdomain.com;
        
        location / {
            proxy_pass http://localhost:8501;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
            proxy_set_header Host $host;
            proxy_cache_bypass $http_upgrade;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }
    }
    ```

11. **Enable Nginx Site**
    ```bash
    ln -s /etc/nginx/sites-available/streamlit /etc/nginx/sites-enabled/
    nginx -t
    systemctl reload nginx
    ```

12. **Configure Firewall**
    ```bash
    ufw allow 80/tcp
    ufw allow 443/tcp
    ufw allow 22/tcp
    ufw enable
    ```

13. **Install SSL Certificate**
    ```bash
    apt install certbot python3-certbot-nginx -y
    certbot --nginx -d yourdomain.com
    # Follow prompts
    ```

14. **Set Up Auto-Renewal**
    ```bash
    certbot renew --dry-run
    # Add cron job
    crontab -e
    # Add: 0 0 * * * certbot renew --quiet
    ```

15. **Configure Backup**
    ```bash
    # Create backup script
    cat > /home/streamlit/backup.sh << 'EOF'
    #!/bin/bash
    tar -czf /home/streamlit/backups/app-$(date +%Y%m%d).tar.gz \
      /home/streamlit/file-converter-seo-app
    EOF
    
    chmod +x /home/streamlit/backup.sh
    
    # Add to cron (daily at 2 AM)
    0 2 * * * /home/streamlit/backup.sh
    ```

**Expected Outcome:**
- Application running on VPS
- Nginx reverse proxy
- SSL/HTTPS enabled
- Auto-start on reboot
- Automated backups

**Cost:** VPS hosting $5-20/month

**Time Estimate:** 1-2 hours

---

## Deployment Checklist

### Pre-Deployment
- [ ] All tests pass
- [ ] Documentation updated
- [ ] Environment variables configured
- [ ] Secret keys secured
- [ ] Database migrations ready (if applicable)
- [ ] Performance tested
- [ ] Security audit completed

### During Deployment
- [ ] Create deployment branch/tag
- [ ] Build application
- [ ] Run smoke tests
- [ ] Deploy to staging first
- [ ] Verify staging works
- [ ] Deploy to production
- [ ] Monitor deployment logs

### Post-Deployment
- [ ] Verify application accessible
- [ ] Test critical features
- [ ] Monitor error rates
- [ ] Check performance metrics
- [ ] Update status page
- [ ] Notify stakeholders
- [ ] Document deployment

---

**Last Updated:** October 8, 2025  
**Version:** 1.0.0
