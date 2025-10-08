# User Workflows

Complete step-by-step workflows for using the File Converter application.

## Table of Contents
1. [Basic File Conversion](#basic-file-conversion)
2. [Batch File Processing](#batch-file-processing)
3. [HTML Generation with SEO](#html-generation-with-seo)
4. [Static Site Generation](#static-site-generation)
5. [WordPress Export Migration](#wordpress-export-migration)
6. [Troubleshooting](#troubleshooting)

---

## Basic File Conversion

### Workflow: Convert Single Document to Markdown

**Use Case:** Convert a Word document to clean Markdown format.

**Steps:**

1. **Launch Application**
   ```
   Navigate to: http://localhost:5000
   ```

2. **Upload File**
   - Click "Browse files" button
   - Select your DOCX file
   - Wait for upload confirmation (green checkmark)

3. **Configure Output**
   - Output Format: Select "Markdown"
   - Leave other options as default

4. **Convert**
   - Click "Convert All Files" button
   - Wait for processing (progress indicator shows status)

5. **Download**
   - Navigate to "Download" tab
   - Click download button next to your file
   - Save the `.md` file to your computer

**Expected Outcome:** Clean Markdown file with preserved formatting and structure.

**Time Estimate:** 10-30 seconds depending on file size.

---

## Batch File Processing

### Workflow: Convert Multiple Documents at Once

**Use Case:** Convert a folder of mixed document types to a single format.

**Prerequisites:**
- Multiple files (DOCX, CSV, TXT, or WXR)
- All files should be under 50MB each

**Steps:**

1. **Prepare Files**
   - Collect all documents to convert
   - Ensure they're in supported formats

2. **Upload Multiple Files**
   - Click "Browse files"
   - Hold Ctrl (Windows/Linux) or Cmd (Mac)
   - Select multiple files
   - Click "Open"

3. **Review File List**
   - Navigate to "File List" tab
   - Verify all files uploaded correctly
   - Check file types and sizes

4. **Configure Settings**
   - Output Format: Choose "Both" (Markdown + HTML)
   - Select HTML template: "Modern"
   - Choose color scheme: "Blue"

5. **Batch Convert**
   - Click "Convert All Files"
   - Monitor progress bar
   - Wait for all conversions to complete

6. **Create Archive**
   - Navigate to "Download" tab
   - Click "📦 Create ZIP Archive"
   - Click "📥 Download ZIP Archive"

7. **Extract and Review**
   - Extract ZIP file on your computer
   - Review converted files
   - Check markdown/ and html/ folders

**Expected Outcome:** ZIP archive containing all converted files in organized folders.

**Time Estimate:** 1-5 minutes for 10-20 files.

**Tips:**
- Process large batches in groups of 50 files
- Keep total upload size under 200MB
- Name files clearly before upload

---

## HTML Generation with SEO

### Workflow: Create SEO-Optimized HTML Pages

**Use Case:** Convert documents to HTML with professional SEO optimization for publishing.

**Steps:**

1. **Upload Document**
   - Upload your source file (any supported format)

2. **Enable SEO Features**
   - In sidebar, ensure "Enable SEO enhancements" is checked ✓
   - This is enabled by default

3. **Configure HTML Output**
   - Output Format: Select "HTML"
   - HTML Template: Choose "Modern"
   - Color Scheme: Select "Blue" (or your preference)
   - Font: Choose "Sans-serif"

4. **Convert with SEO**
   - Click "Convert All Files"
   - Wait for processing
   - SEO enhancements applied automatically

5. **Review SEO Report**
   - Navigate to "SEO Report" tab
   - Check your SEO Score (0-100)
   - Review your Grade (A-F)
   - Read Issues (critical problems)
   - Review Warnings (improvements)
   - Check Successes (what's working)
   - Read Recommendations

6. **Improve Score (if needed)**
   - If score is low, review issues
   - Common fixes:
     - Ensure document has headings
     - Add descriptive content (300+ words)
     - Include meaningful text
   - Re-convert after improvements

7. **Download Optimized HTML**
   - Navigate to "Download" tab
   - Download your HTML file
   - Open in browser to verify

8. **Publish**
   - Upload HTML to your web server
   - Images are embedded or linked
   - HTML includes all SEO meta tags
   - Ready for search engine indexing

**Expected Outcome:** Professional HTML page with:
- Meta tags (title, description, keywords)
- Open Graph tags (Facebook sharing)
- Twitter Card tags
- Schema.org structured data
- Semantic HTML5 structure
- Image lazy loading
- Secure link attributes

**SEO Score Targets:**
- **90-100 (A)**: Excellent - publish as-is
- **80-89 (B)**: Good - minor tweaks optional
- **70-79 (C)**: Fair - review warnings
- **60-69 (D)**: Poor - fix critical issues
- **Below 60 (F)**: Critical - major improvements needed

**Time Estimate:** 2-5 minutes including SEO review.

---

## Static Site Generation

### Workflow: Create Complete Static Website

**Use Case:** Convert multiple documents into a navigable website with index page.

**Prerequisites:**
- Multiple related documents (blog posts, articles, pages)
- Basic understanding of static sites

**Steps:**

1. **Upload All Content**
   - Upload all documents that will become pages
   - Can be mixed formats (DOCX, CSV, TXT, WXR)

2. **Configure Site Settings**
   - Output Format: "HTML" or "Both"
   - Template: Choose consistent style
   - Color Scheme: Select site theme
   - Font: Pick readable option
   - Enable SEO: Keep checked ✓

3. **Add Frontmatter (Optional)**
   - Check "Add Frontmatter"
   - Select SSG type: "Jekyll", "Hugo", or "Astro"
   - This adds metadata headers to files

4. **Convert All Files**
   - Click "Convert All Files"
   - Wait for batch processing
   - Review SEO reports for each page

5. **Generate Static Site**
   - Navigate to "Download" tab
   - Scroll to "Static Site Generator" section
   - Enter Site Name: "My Blog" (or your choice)
   - Click "🌐 Generate Static Site"

6. **Download Site**
   - Click "📥 Download Static Site"
   - Save ZIP file (e.g., `my_blog_site.zip`)

7. **Extract and Review**
   ```
   Extract ZIP to get:
   my_blog_site/
   ├── index.html          # Homepage with navigation
   ├── pages/              # Individual content pages
   │   ├── article1.html
   │   ├── article2.html
   │   └── article3.html
   └── assets/            # Resources
       ├── style.css      # Site styling
       └── images/        # All images
   ```

8. **Test Locally**
   - Open `index.html` in browser
   - Click navigation links
   - Verify all pages load
   - Check images display
   - Test on mobile view

9. **Deploy Website**
   
   **Option A: GitHub Pages**
   ```bash
   git init
   git add .
   git commit -m "Initial site"
   git push origin main
   # Enable GitHub Pages in repository settings
   ```

   **Option B: Netlify**
   - Drag and drop the folder to netlify.com
   - Site goes live immediately
   - Get shareable URL

   **Option C: Traditional Hosting**
   - FTP upload entire folder to web host
   - Point domain to folder
   - Site is live

**Expected Outcome:** 
- Complete static website
- Navigation index page
- All pages interlinked
- Consistent styling
- SEO-optimized
- Ready to deploy

**Customization Options:**
- Edit `assets/style.css` for custom colors
- Modify `index.html` for custom homepage
- Add additional pages manually
- Include custom images/logos

**Time Estimate:** 5-10 minutes for 10 pages.

---

## WordPress Export Migration

### Workflow: Migrate WordPress Blog to Static Site

**Use Case:** Export WordPress content and convert to clean Markdown/HTML.

**Prerequisites:**
- WordPress site with admin access
- WXR export file from WordPress

**Steps:**

1. **Export from WordPress**
   - Log into WordPress admin
   - Go to Tools → Export
   - Select "All content"
   - Click "Download Export File"
   - Save `wordpress-export.xml` (WXR file)

2. **Upload to Converter**
   - Open File Converter application
   - Upload the WXR file
   - File recognized as WordPress export

3. **Configure Conversion**
   - Output Format: "Both" (Markdown + HTML)
   - Enable SEO enhancements ✓
   - Add Frontmatter: Check ✓
   - Select SSG: Choose your target (Jekyll/Hugo/Astro)

4. **Convert WordPress Export**
   - Click "Convert All Files"
   - Converter extracts:
     - All posts
     - All pages
     - Post metadata (dates, authors, categories)
     - Featured images
     - Inline images
   - Download remote images automatically

5. **Review Converted Content**
   - Navigate to "File List" tab
   - See all posts/pages extracted
   - Check image count
   - Review any warnings

6. **Check SEO Scores**
   - Navigate to "SEO Report" tab
   - Review each post's SEO score
   - Identify posts needing improvement
   - Note common issues across posts

7. **Generate Static Site**
   - Go to "Download" tab
   - Enter Site Name: "My WordPress Blog"
   - Click "Generate Static Site"
   - Download complete site

8. **Migrate to New Platform**

   **For Jekyll:**
   ```bash
   # Extract ZIP
   unzip my_wordpress_blog_site.zip
   
   # Create Jekyll site
   jekyll new my-blog
   cd my-blog
   
   # Copy converted files
   cp -r ../my_wordpress_blog_site/pages/* _posts/
   cp -r ../my_wordpress_blog_site/assets/images images/
   
   # Build and serve
   jekyll serve
   ```

   **For Hugo:**
   ```bash
   # Create Hugo site
   hugo new site my-blog
   cd my-blog
   
   # Copy files
   cp -r ../my_wordpress_blog_site/pages/* content/posts/
   cp -r ../my_wordpress_blog_site/assets/images static/images/
   
   # Add theme and build
   hugo server
   ```

   **For Astro:**
   ```bash
   # Create Astro site
   npm create astro@latest my-blog
   cd my-blog
   
   # Copy files
   cp -r ../my_wordpress_blog_site/pages/* src/pages/posts/
   cp -r ../my_wordpress_blog_site/assets/images public/images/
   
   # Run dev server
   npm run dev
   ```

9. **Verify Migration**
   - Check all posts converted
   - Verify images load
   - Test internal links
   - Review formatting
   - Check metadata (dates, authors)

10. **Deploy New Site**
    - Build for production
    - Deploy to hosting platform
    - Set up custom domain
    - Configure redirects from old URLs

**Expected Outcome:**
- Complete blog migration
- All posts preserved
- Images downloaded and optimized
- SEO metadata intact
- Ready for static hosting

**Common Issues:**

| Issue | Solution |
|-------|----------|
| Missing images | Check original WordPress image URLs are accessible |
| Broken formatting | Review original post HTML, may need manual cleanup |
| Missing metadata | Ensure WordPress export included all data |
| Large file size | Export in smaller date ranges |

**Time Estimate:** 
- Small blog (10-50 posts): 5-15 minutes
- Medium blog (50-200 posts): 15-45 minutes
- Large blog (200+ posts): 45+ minutes

---

## Troubleshooting

### Common Issues and Solutions

#### Issue: File Upload Fails

**Symptoms:** File doesn't upload, error message appears

**Solutions:**
1. Check file size (must be under 50MB)
2. Verify file extension is supported (docx, csv, txt, wxr)
3. Try different browser
4. Refresh page and try again
5. Check internet connection

---

#### Issue: Conversion Produces Empty Output

**Symptoms:** Markdown/HTML file is blank or very short

**Solutions:**
1. Open original file to verify it has content
2. Check if file is password-protected (not supported)
3. For DOCX: Ensure it's not a template file
4. Try converting file in different format first
5. Check for file corruption

---

#### Issue: Images Not Appearing

**Symptoms:** Converted file shows missing images, broken links

**Solutions:**
1. **For DOCX files:**
   - Ensure images are embedded, not linked
   - Check image formats are standard (PNG, JPEG)
   
2. **For WXR files:**
   - Verify image URLs are publicly accessible
   - Check your internet connection
   - Try re-uploading with better connection

3. **General:**
   - Download ZIP archive (includes all images)
   - Check assets/images folder
   - Verify relative paths are correct

---

#### Issue: Low SEO Score

**Symptoms:** SEO Report shows grade D or F

**Solutions:**
1. Add descriptive title to document
2. Include more content (aim for 300+ words)
3. Use proper heading structure (H1, H2, H3)
4. Add descriptive text, not just bullet points
5. Review specific issues in SEO Report tab

---

#### Issue: HTML Styling Looks Wrong

**Symptoms:** Colors, fonts, or layout incorrect

**Solutions:**
1. Try different template (Modern, Minimal, Classic, Dark)
2. Change color scheme in sidebar
3. Select different font option
4. Download and edit CSS in ZIP archive
5. View in different browser (some older browsers not supported)

---

#### Issue: Static Site Links Don't Work

**Symptoms:** Clicking links in index.html doesn't navigate to pages

**Solutions:**
1. Ensure you extracted entire ZIP archive
2. Maintain folder structure (don't move files)
3. Open index.html from extracted folder, not inside ZIP
4. For web deployment, upload all files and folders
5. Check browser console for errors (F12)

---

#### Issue: Download Button Not Working

**Symptoms:** Clicking download doesn't start download

**Solutions:**
1. Check browser's download settings
2. Disable popup blocker for this site
3. Try different browser
4. Clear browser cache
5. Check available disk space

---

### Performance Issues

#### Slow Conversion

**If conversion takes very long:**

1. **Large Files:**
   - Split large documents into smaller parts
   - Process in smaller batches
   - Reduce image count/size in source

2. **Many Files:**
   - Process in batches of 20-30 files
   - Close other browser tabs
   - Ensure stable internet for WXR files

3. **Image Processing:**
   - Large images take longer to optimize
   - Many images increase processing time
   - This is normal for image-heavy documents

---

### Getting Additional Help

**If you still have issues:**

1. Check the [README](../../README.md) for detailed documentation
2. Review [ARCHITECTURE](../../ARCHITECTURE.md) for technical details
3. Search existing [GitHub Issues](https://github.com/poolboy17/file-converter-seo-app/issues)
4. Open a new issue with:
   - File type you're converting
   - Error messages (screenshot)
   - Steps to reproduce
   - Expected vs actual behavior

---

**Last Updated:** October 8, 2025  
**Version:** 1.0.0
