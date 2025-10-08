# Security Policy

## Supported Versions

Currently supported versions for security updates:

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |

## Reporting a Vulnerability

We take security vulnerabilities seriously. If you discover a security issue, please follow these steps:

### 1. Do Not Open a Public Issue

Please **do not** create a public GitHub issue for security vulnerabilities.

### 2. Report Privately

Send security reports to:
- Open a private security advisory on GitHub
- Or contact the maintainer directly through GitHub

### 3. Include Details

Provide as much information as possible:
- Type of vulnerability
- Affected component(s)
- Steps to reproduce
- Potential impact
- Suggested fix (if available)

### 4. Response Timeline

- **Initial Response**: Within 48 hours
- **Severity Assessment**: Within 5 business days
- **Fix Timeline**: Depends on severity
  - Critical: 7 days
  - High: 14 days
  - Medium: 30 days
  - Low: Next release cycle

## Security Measures

### Data Handling

**File Processing:**
- All files processed in memory
- No permanent storage of user data
- Files discarded after conversion
- No logging of file contents

**User Privacy:**
- No personal information collected
- No analytics or tracking
- No cookies or session storage
- No external API calls with user data

### Input Validation

**File Uploads:**
- File type verification by extension
- Size limits enforced
- Malicious content scanning
- Safe file name handling

**Image Processing:**
- URL validation before download
- File type verification
- Size limits on downloads
- Content sanitization

**HTML Generation:**
- XSS prevention through sanitization
- No code execution in templates
- Safe attribute handling
- Content escaping

### Dependencies

**Security Updates:**
- Regular dependency updates
- Automated vulnerability scanning
- Quick response to CVEs
- Minimal dependency footprint

**Current Dependencies:**
- Streamlit (web framework)
- python-docx (document parsing)
- pandas (data processing)
- BeautifulSoup4 (HTML/XML parsing)
- Pillow (image processing)
- PyYAML (YAML processing)
- markdown (Markdown conversion)

All dependencies are from trusted sources and regularly updated.

## Security Best Practices

### For Users

**Safe Usage:**
1. Download from official repository only
2. Verify file integrity if distributed
3. Run in isolated environment if processing sensitive files
4. Review generated HTML before deployment
5. Use strong passwords if deploying with authentication

**When Deploying:**
1. Use HTTPS for web deployment
2. Enable authentication if exposing publicly
3. Implement rate limiting
4. Monitor for unusual activity
5. Keep Python and dependencies updated

### For Contributors

**Code Security:**
1. Never commit secrets or API keys
2. Validate all user inputs
3. Sanitize all outputs
4. Use safe file operations
5. Follow secure coding guidelines

**Dependencies:**
1. Use known, trusted packages
2. Pin dependency versions
3. Review security advisories
4. Update regularly
5. Minimize new dependencies

## Known Limitations

### Not Addressed
- DDoS protection (deploy behind reverse proxy)
- Rate limiting (implement at deployment level)
- User authentication (not included in core app)

### Deployment Recommendations
- Use a reverse proxy (nginx, Apache)
- Implement rate limiting
- Add authentication layer if needed
- Use HTTPS/TLS
- Regular security audits

## Security Disclosure

### Public Disclosure Timeline

After a fix is released:
1. **Immediate**: Security advisory published
2. **24 hours**: Detailed disclosure
3. **7 days**: Full technical details

### Credit

Security researchers who responsibly disclose vulnerabilities will be:
- Credited in security advisories
- Mentioned in CHANGELOG
- Recognized in README acknowledgments

## Security Checklist for Deployment

- [ ] Latest version installed
- [ ] Dependencies updated
- [ ] HTTPS enabled
- [ ] Authentication configured (if public)
- [ ] Rate limiting enabled
- [ ] Firewall rules configured
- [ ] Logs monitored
- [ ] Backup strategy in place
- [ ] Security headers configured
- [ ] File upload limits set

## Compliance

This application:
- Does not store personal data (GDPR compliant by design)
- Processes files locally (no data transfer)
- No tracking or analytics
- Open source for transparency

## Additional Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Python Security Best Practices](https://python.readthedocs.io/en/stable/library/security_warnings.html)
- [Streamlit Security](https://docs.streamlit.io/library/advanced-features/security)

## Contact

For security concerns:
- GitHub Security Advisories (preferred)
- Open an issue with `[SECURITY]` prefix
- Contact maintainer through GitHub

---

**Last Updated**: October 8, 2025
