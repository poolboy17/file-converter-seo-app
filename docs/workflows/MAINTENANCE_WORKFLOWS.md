# Maintenance Workflows

Complete workflows for maintaining and monitoring the File Converter application.

## Table of Contents
1. [Dependency Updates](#dependency-updates)
2. [Security Patching](#security-patching)
3. [Performance Monitoring](#performance-monitoring)
4. [Log Management](#log-management)
5. [Backup and Recovery](#backup-and-recovery)
6. [Version Release](#version-release)

---

## Dependency Updates

### Workflow: Update Python Dependencies

**Frequency:** Monthly or when security updates available

**Steps:**

1. **Check for Updates**
   ```bash
   # Using pip
   pip list --outdated
   
   # Using uv
   uv pip list --outdated
   ```

2. **Review Updates**
   - Check CHANGELOG for each package
   - Identify breaking changes
   - Note security fixes
   - Assess compatibility

3. **Create Update Branch**
   ```bash
   git checkout -b chore/update-dependencies
   ```

4. **Update Dependencies**
   
   **Individual Package:**
   ```bash
   uv pip install --upgrade streamlit
   ```
   
   **All Packages:**
   ```bash
   uv pip install --upgrade-package "*"
   ```

5. **Update Lock File**
   ```bash
   uv lock
   ```

6. **Test Application**
   ```bash
   streamlit run app.py --server.port 5000
   ```
   
   Test checklist:
   - [ ] File upload works
   - [ ] All converters function
   - [ ] HTML generation works
   - [ ] SEO validation runs
   - [ ] Image extraction works
   - [ ] Download features work

7. **Run Automated Tests** (if available)
   ```bash
   pytest tests/
   ```

8. **Check for Deprecation Warnings**
   ```bash
   python -W default app.py 2>&1 | grep -i deprecat
   ```

9. **Update Documentation**
   
   Update `pyproject.toml`:
   ```toml
   [project]
   dependencies = [
       "streamlit>=1.29.0",  # Updated
       # ... other deps
   ]
   ```

10. **Commit Changes**
    ```bash
    git add pyproject.toml uv.lock
    git commit -m "chore: update dependencies
    
    - streamlit: 1.28.0 -> 1.29.0
    - pandas: 2.1.0 -> 2.1.1
    - pillow: 10.0.0 -> 10.1.0
    
    All tests passing, no breaking changes."
    
    git push origin chore/update-dependencies
    ```

11. **Create Pull Request**
    - List all updated packages
    - Note any breaking changes
    - Include test results

12. **Deploy After Merge**
    - Deploy to staging first
    - Monitor for issues
    - Deploy to production

**Expected Outcome:**
- Dependencies up-to-date
- Security vulnerabilities patched
- Application still functions correctly

**Time Estimate:** 30-60 minutes

---

## Security Patching

### Workflow: Apply Critical Security Patch

**Trigger:** Security advisory received

**Steps:**

1. **Assess Severity**
   - Read security advisory
   - Determine CVSS score
   - Identify affected versions
   - Check if your version affected

2. **Verify Impact**
   ```bash
   # Check installed version
   pip show package-name
   
   # Check for vulnerabilities
   pip audit
   # or
   safety check
   ```

3. **Create Hotfix Branch**
   ```bash
   git checkout main
   git pull
   git checkout -b hotfix/security-patch-packagename
   ```

4. **Apply Patch**
   ```bash
   # Update specific package
   uv pip install --upgrade package-name==safe-version
   ```

5. **Verify Fix**
   ```bash
   pip audit
   # Should show no vulnerabilities
   ```

6. **Test Critical Paths**
   - Test affected functionality
   - Run smoke tests
   - Check for regressions

7. **Fast-Track Review**
   - Create PR with "SECURITY" label
   - Get expedited review
   - Provide security advisory link

8. **Emergency Deploy**
   ```bash
   # After approval
   git checkout main
   git merge hotfix/security-patch-packagename
   git tag -a v1.0.1-security -m "Security patch for CVE-XXXX"
   git push origin main --tags
   ```

9. **Deploy Immediately**
   - Skip staging if critical
   - Deploy to production
   - Monitor closely

10. **Update SECURITY.md**
    ```markdown
    ## Security Updates
    
    ### 2025-10-XX - CVE-XXXX
    - Affected versions: 1.0.0
    - Fixed in: 1.0.1
    - Severity: High
    - Action: Update immediately
    ```

11. **Notify Users**
    - Create GitHub release
    - Post security advisory
    - Email notification (if applicable)
    - Update documentation

**Expected Outcome:**
- Vulnerability patched
- Application secure
- Users notified

**Time Estimate:** 1-4 hours (depending on severity)

---

## Performance Monitoring

### Workflow: Regular Performance Check

**Frequency:** Weekly

**Steps:**

1. **Monitor Resource Usage**
   
   **On Replit:**
   - Check resource usage in dashboard
   - Review memory consumption
   - Check CPU usage patterns
   
   **On VPS:**
   ```bash
   # CPU and memory
   htop
   
   # Disk usage
   df -h
   
   # Process details
   ps aux | grep streamlit
   ```

2. **Review Application Logs**
   ```bash
   # Streamlit logs
   tail -f /var/log/streamlit.log
   
   # System logs
   journalctl -u streamlit -f
   
   # Nginx access logs
   tail -f /var/log/nginx/access.log
   ```

3. **Check Error Rates**
   - Count errors in logs:
   ```bash
   grep -i error /var/log/streamlit.log | wc -l
   ```
   - Identify most common errors
   - Note any patterns

4. **Measure Response Times**
   
   Test key operations:
   ```bash
   # Upload and convert timing
   time curl -F "file=@test.docx" http://localhost:5000/upload
   ```

5. **Test File Conversion Speed**
   - Convert small file (1MB): Should be <5 seconds
   - Convert medium file (10MB): Should be <30 seconds
   - Convert large file (50MB): Should be <2 minutes

6. **Check Image Processing**
   - Test image extraction from DOCX
   - Verify optimization speed
   - Check download performance for WXR

7. **Review Database Performance** (if applicable)
   ```sql
   -- Check slow queries
   SELECT * FROM slow_query_log;
   ```

8. **Generate Performance Report**
   ```markdown
   ## Weekly Performance Report - YYYY-MM-DD
   
   ### Metrics
   - Average response time: XXms
   - Peak memory usage: XXX MB
   - Average CPU: XX%
   - Total conversions: XXX
   - Error rate: X.X%
   
   ### Issues Identified
   - Memory usage increased by 15%
   - Slow conversion for large WXR files
   
   ### Actions Taken
   - Optimized image processing
   - Added memory limits
   ```

9. **Identify Bottlenecks**
   - Slow converters
   - Image processing delays
   - Large file handling
   - Memory leaks

10. **Optimize if Needed**
    - Implement caching
    - Optimize algorithms
    - Add resource limits
    - Improve error handling

**Expected Outcome:**
- Performance baseline established
- Issues identified early
- Optimization opportunities noted

**Time Estimate:** 30-45 minutes

---

## Log Management

### Workflow: Log Rotation and Analysis

**Frequency:** Daily/Weekly

**Steps:**

1. **Configure Log Rotation**
   
   Create `/etc/logrotate.d/streamlit`:
   ```
   /var/log/streamlit/*.log {
       daily
       missingok
       rotate 14
       compress
       delaycompress
       notifempty
       create 0640 streamlit streamlit
       sharedscripts
       postrotate
           systemctl reload streamlit > /dev/null 2>&1
       endscript
   }
   ```

2. **Set Up Centralized Logging** (Optional)
   
   Configure rsyslog to send to central server:
   ```bash
   # /etc/rsyslog.d/streamlit.conf
   if $programname == 'streamlit' then @@log-server:514
   ```

3. **Analyze Logs Daily**
   
   **Error Analysis:**
   ```bash
   # Count errors by type
   grep ERROR /var/log/streamlit.log | \
     awk '{print $5}' | \
     sort | uniq -c | sort -rn
   ```
   
   **User Activity:**
   ```bash
   # Count conversions by file type
   grep "Converting" /var/log/streamlit.log | \
     awk '{print $6}' | \
     sort | uniq -c
   ```
   
   **Performance:**
   ```bash
   # Find slow conversions (>30 seconds)
   grep "Conversion completed" /var/log/streamlit.log | \
     awk '$8 > 30 {print $0}'
   ```

4. **Create Log Dashboard**
   
   Using ELK Stack or similar:
   - Set up Elasticsearch
   - Configure Logstash for ingestion
   - Create Kibana dashboards
   - Set up alerts

5. **Set Up Alerts**
   
   **Error Rate Alert:**
   ```bash
   # Check if error rate exceeds threshold
   errors=$(grep -c ERROR /var/log/streamlit.log)
   if [ $errors -gt 100 ]; then
       echo "High error rate: $errors errors" | \
         mail -s "Alert: High Error Rate" admin@example.com
   fi
   ```
   
   **Disk Space Alert:**
   ```bash
   # Alert if logs exceed 1GB
   log_size=$(du -sm /var/log/streamlit | awk '{print $1}')
   if [ $log_size -gt 1024 ]; then
       echo "Log size: ${log_size}MB" | \
         mail -s "Alert: Large Log Files" admin@example.com
   fi
   ```

6. **Archive Old Logs**
   ```bash
   # Compress logs older than 30 days
   find /var/log/streamlit -name "*.log" -mtime +30 -exec gzip {} \;
   
   # Move to archive storage
   find /var/log/streamlit -name "*.log.gz" -mtime +90 \
     -exec mv {} /backup/logs/ \;
   ```

7. **Generate Weekly Report**
   ```bash
   #!/bin/bash
   # weekly-log-report.sh
   
   echo "=== Weekly Log Report ==="
   echo "Period: $(date -d '7 days ago' +%Y-%m-%d) to $(date +%Y-%m-%d)"
   echo ""
   
   echo "Total Requests:"
   grep "GET\|POST" /var/log/nginx/access.log | wc -l
   
   echo "Total Conversions:"
   grep "Conversion completed" /var/log/streamlit.log | wc -l
   
   echo "Total Errors:"
   grep "ERROR" /var/log/streamlit.log | wc -l
   
   echo "Top Errors:"
   grep "ERROR" /var/log/streamlit.log | \
     awk '{print $5}' | sort | uniq -c | sort -rn | head -5
   ```

**Expected Outcome:**
- Logs rotated automatically
- Storage under control
- Issues detected early
- Trends identified

**Time Estimate:** 15-30 minutes weekly

---

## Backup and Recovery

### Workflow: Regular Backup Procedure

**Frequency:** Daily (automated)

**Steps:**

1. **Identify Backup Targets**
   - Application code
   - Configuration files
   - User uploads (if stored)
   - Database (if applicable)
   - Logs

2. **Create Backup Script**
   
   Create `/home/streamlit/backup.sh`:
   ```bash
   #!/bin/bash
   
   # Configuration
   BACKUP_DIR="/backup/file-converter"
   APP_DIR="/home/streamlit/file-converter-seo-app"
   DATE=$(date +%Y%m%d_%H%M%S)
   RETENTION_DAYS=30
   
   # Create backup directory
   mkdir -p $BACKUP_DIR
   
   # Backup application
   tar -czf $BACKUP_DIR/app-$DATE.tar.gz \
     $APP_DIR \
     --exclude='venv' \
     --exclude='__pycache__' \
     --exclude='.git'
   
   # Backup configuration
   tar -czf $BACKUP_DIR/config-$DATE.tar.gz \
     /etc/nginx/sites-available/streamlit \
     /etc/systemd/system/streamlit.service \
     /etc/streamlit/config.toml
   
   # Backup logs (last 7 days)
   find /var/log/streamlit -name "*.log" -mtime -7 \
     -exec tar -czf $BACKUP_DIR/logs-$DATE.tar.gz {} +
   
   # Remove old backups
   find $BACKUP_DIR -name "*.tar.gz" -mtime +$RETENTION_DAYS -delete
   
   # Upload to cloud storage (optional)
   # aws s3 sync $BACKUP_DIR s3://my-backups/file-converter/
   
   # Log completion
   echo "$(date): Backup completed successfully" >> /var/log/backup.log
   ```

3. **Make Script Executable**
   ```bash
   chmod +x /home/streamlit/backup.sh
   ```

4. **Schedule Automated Backup**
   ```bash
   crontab -e
   # Add:
   0 2 * * * /home/streamlit/backup.sh
   ```

5. **Test Backup**
   ```bash
   # Run backup manually
   ./backup.sh
   
   # Verify backup created
   ls -lh /backup/file-converter/
   ```

6. **Test Restore Procedure**
   
   **Recovery Script** (`/home/streamlit/restore.sh`):
   ```bash
   #!/bin/bash
   
   # Configuration
   BACKUP_FILE=$1
   RESTORE_DIR="/tmp/restore-$(date +%Y%m%d)"
   
   if [ -z "$BACKUP_FILE" ]; then
       echo "Usage: $0 <backup-file>"
       exit 1
   fi
   
   # Create restore directory
   mkdir -p $RESTORE_DIR
   
   # Extract backup
   tar -xzf $BACKUP_FILE -C $RESTORE_DIR
   
   # Stop application
   systemctl stop streamlit
   
   # Backup current state
   mv /home/streamlit/file-converter-seo-app \
      /home/streamlit/file-converter-seo-app.old
   
   # Restore from backup
   cp -r $RESTORE_DIR/home/streamlit/file-converter-seo-app \
      /home/streamlit/
   
   # Set permissions
   chown -R streamlit:streamlit /home/streamlit/file-converter-seo-app
   
   # Start application
   systemctl start streamlit
   
   # Verify
   sleep 5
   systemctl status streamlit
   
   echo "Restore completed. Check application status."
   echo "Previous version saved as: file-converter-seo-app.old"
   ```

7. **Document Recovery Procedure**
   
   Create `docs/RECOVERY.md`:
   ```markdown
   # Recovery Procedures
   
   ## Application Restore
   
   1. Identify backup file:
      ```bash
      ls -lh /backup/file-converter/
      ```
   
   2. Run restore script:
      ```bash
      sudo /home/streamlit/restore.sh /backup/file-converter/app-YYYYMMDD.tar.gz
      ```
   
   3. Verify application:
      ```bash
      curl http://localhost:5000/_stcore/health
      ```
   
   ## Configuration Restore
   
   Extract and restore config files:
   ```bash
   tar -xzf /backup/file-converter/config-YYYYMMDD.tar.gz -C /tmp
   sudo cp /tmp/etc/nginx/sites-available/streamlit /etc/nginx/sites-available/
   sudo systemctl reload nginx
   ```
   ```

8. **Monitor Backup Success**
   ```bash
   # Check last backup
   ls -lth /backup/file-converter/ | head -5
   
   # Verify backup log
   tail -20 /var/log/backup.log
   ```

9. **Set Up Offsite Backup** (Recommended)
   
   **AWS S3:**
   ```bash
   # Install AWS CLI
   pip install awscli
   
   # Configure
   aws configure
   
   # Sync backups
   aws s3 sync /backup/file-converter s3://my-backups/
   ```
   
   **Rsync to Remote Server:**
   ```bash
   rsync -avz /backup/file-converter/ \
     backup-server:/backups/file-converter/
   ```

**Expected Outcome:**
- Daily automated backups
- 30-day retention
- Tested restore procedure
- Offsite copies for disaster recovery

**Time Estimate:** 
- Initial setup: 1-2 hours
- Daily maintenance: Automated (0 time)
- Monthly testing: 15-30 minutes

---

## Version Release

### Workflow: Release New Version

**Frequency:** As needed (features/fixes ready)

**Steps:**

1. **Prepare Release**
   - All features complete
   - All tests passing
   - Documentation updated
   - CHANGELOG updated

2. **Determine Version Number**
   
   Follow [Semantic Versioning](https://semver.org):
   - **MAJOR** (X.0.0): Breaking changes
   - **MINOR** (1.X.0): New features (backward compatible)
   - **PATCH** (1.0.X): Bug fixes

3. **Update Version Numbers**
   
   **In `pyproject.toml`:**
   ```toml
   [project]
   name = "file-converter-seo-app"
   version = "1.1.0"  # Update this
   ```
   
   **In `config.yaml`:**
   ```yaml
   app:
     version: "1.1.0"  # Update this
   ```

4. **Update CHANGELOG.md**
   ```markdown
   ## [1.1.0] - 2025-10-15
   
   ### Added
   - PDF converter support
   - Bulk image download optimization
   - Progress indicators for long operations
   
   ### Changed
   - Improved SEO validation algorithm
   - Updated UI with better error messages
   
   ### Fixed
   - Image extraction from password-protected DOCX
   - CSV encoding detection for international characters
   ```

5. **Create Release Branch**
   ```bash
   git checkout main
   git pull origin main
   git checkout -b release/v1.1.0
   ```

6. **Commit Version Bump**
   ```bash
   git add pyproject.toml config.yaml CHANGELOG.md
   git commit -m "chore: bump version to 1.1.0"
   git push origin release/v1.1.0
   ```

7. **Run Full Test Suite**
   ```bash
   # Manual testing
   streamlit run app.py
   # Test all features
   
   # Automated tests (if available)
   pytest tests/
   ```

8. **Create Pull Request**
   - Title: "Release v1.1.0"
   - Include CHANGELOG excerpt
   - Request review from maintainers

9. **Merge to Main**
   ```bash
   # After approval
   git checkout main
   git merge release/v1.1.0
   ```

10. **Create Git Tag**
    ```bash
    git tag -a v1.1.0 -m "Release version 1.1.0
    
    Features:
    - PDF converter support
    - Bulk image optimization
    
    Fixes:
    - Image extraction improvements
    - CSV encoding detection"
    
    git push origin v1.1.0
    ```

11. **Create GitHub Release**
    - Go to repository → Releases
    - Click "Draft a new release"
    - Tag: v1.1.0
    - Title: "File Converter v1.1.0 - PDF Support"
    - Description: Copy from CHANGELOG
    - Attach build artifacts (if any)
    - Click "Publish release"

12. **Deploy to Production**
    ```bash
    # Pull latest
    git checkout main
    git pull origin main
    
    # Deploy
    ./deploy.sh production
    ```

13. **Verify Deployment**
    - Check application version displays correctly
    - Test new features
    - Monitor logs for errors
    - Check performance

14. **Announce Release**
    - Update README badges
    - Post on social media
    - Notify users via email
    - Update documentation site

15. **Monitor Post-Release**
    - Watch error rates
    - Check user feedback
    - Monitor performance
    - Be ready for hotfix if needed

**Expected Outcome:**
- New version released
- Users can upgrade
- Features documented
- Deployment successful

**Time Estimate:** 2-4 hours

---

## Maintenance Checklist

### Daily
- [ ] Review application logs
- [ ] Check error rates
- [ ] Monitor resource usage
- [ ] Verify backups ran

### Weekly
- [ ] Performance review
- [ ] Log analysis
- [ ] Security scan
- [ ] Test backup restore

### Monthly
- [ ] Update dependencies
- [ ] Review and optimize queries
- [ ] Clean old logs
- [ ] Update documentation
- [ ] Review user feedback

### Quarterly
- [ ] Major dependency updates
- [ ] Performance audit
- [ ] Security audit
- [ ] Disaster recovery drill
- [ ] Review and update procedures

---

**Last Updated:** October 8, 2025  
**Version:** 1.0.0
