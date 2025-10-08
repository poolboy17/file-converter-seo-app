import streamlit as st
import io
import zipfile
import os
from typing import List, Tuple, Dict
from converters.docx_converter import DocxConverter
from converters.csv_converter import CsvConverter
from converters.txt_converter import TxtConverter
from converters.wxr_converter import WxrConverter
from utils.html_generator import HtmlGenerator
from utils.file_utils import get_file_extension, create_download_zip
from utils.frontmatter_generator import FrontmatterGenerator
from utils.static_site_generator import StaticSiteGenerator
from utils.image_handler import ImageHandler

# Initialize converters
converters = {
    'docx': DocxConverter(),
    'csv': CsvConverter(),
    'txt': TxtConverter(),
    'wxr': WxrConverter()
}

def main():
    st.set_page_config(
        page_title="File to Markdown Converter",
        page_icon="📄",
        layout="wide"
    )
    
    st.title("📄 File to Markdown Converter")
    st.markdown("Convert DOCX, CSV, TXT, and WXR files to clean markdown and static HTML")
    
    # Sidebar for options
    st.sidebar.header("Conversion Options")
    output_format = st.sidebar.selectbox(
        "Output Format",
        ["Markdown", "HTML", "Both"]
    )
    
    include_metadata = st.sidebar.checkbox("Include metadata", value=True)
    
    # Frontmatter options
    st.sidebar.subheader("Frontmatter Options")
    add_frontmatter = st.sidebar.checkbox("Add SSG frontmatter", value=False, help="Add frontmatter for static site generators")
    ssg_type = None
    if add_frontmatter:
        ssg_type = st.sidebar.selectbox(
            "Static Site Generator",
            ["Jekyll", "Hugo", "Astro"],
            help="Choose your static site generator"
        )
    
    # HTML Template options
    st.sidebar.subheader("HTML Template & Styling")
    html_template = st.sidebar.selectbox(
        "Template",
        ["Modern", "Minimal", "Classic", "Dark"],
        help="Choose HTML template style"
    )
    
    color_scheme = st.sidebar.selectbox(
        "Color Scheme",
        ["Blue", "Green", "Purple", "Orange", "Dark"],
        help="Choose color scheme"
    )
    
    font_option = st.sidebar.selectbox(
        "Font Family",
        ["Default", "Sans-serif", "Serif", "Monospace"],
        help="Choose font family"
    )
    
    font_family = None
    if font_option == "Sans-serif":
        font_family = '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif'
    elif font_option == "Serif":
        font_family = 'Georgia, "Times New Roman", Times, serif'
    elif font_option == "Monospace":
        font_family = '"Courier New", Courier, monospace'
    
    # SEO Options
    st.sidebar.subheader("SEO Optimization")
    enable_seo = st.sidebar.checkbox("Enable SEO enhancements", value=True, 
                                      help="Automatically enhance HTML with meta tags, Open Graph, structured data, and SEO best practices")
    
    # File upload section
    st.header("Upload Files")
    uploaded_files = st.file_uploader(
        "Choose files to convert",
        type=['docx', 'csv', 'txt', 'wxr'],
        accept_multiple_files=True,
        help="Supported formats: DOCX, CSV, TXT, WXR"
    )
    
    if uploaded_files:
        st.success(f"Uploaded {len(uploaded_files)} file(s)")
        
        # Process files
        converted_files = []
        
        # Create tabs for different views
        tab1, tab2, tab3, tab4 = st.tabs(["📋 File List", "👀 Preview", "📥 Download", "🎯 SEO Report"])
        
        with tab1:
            st.subheader("Files to Convert")
            for i, file in enumerate(uploaded_files):
                col1, col2, col3 = st.columns([3, 1, 1])
                with col1:
                    st.write(f"**{file.name}**")
                with col2:
                    st.write(f"{file.size} bytes")
                with col3:
                    file_ext = get_file_extension(file.name)
                    st.write(f".{file_ext}")
        
        # Convert button
        if st.button("🔄 Convert All Files", type="primary"):
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # Create image handler for extracting/downloading images
            image_handler = ImageHandler()
            
            for i, file in enumerate(uploaded_files):
                status_text.text(f"Converting {file.name}...")
                
                try:
                    file_ext = get_file_extension(file.name)
                    
                    if file_ext in converters:
                        # Convert to markdown with image extraction/downloading
                        if file_ext in ['docx', 'wxr']:
                            markdown_content = converters[file_ext].convert(file, include_metadata, image_handler)
                        else:
                            markdown_content = converters[file_ext].convert(file, include_metadata)
                        
                        # Apply SSG frontmatter if requested
                        if add_frontmatter and ssg_type:
                            frontmatter_gen = FrontmatterGenerator()
                            # Extract existing metadata from markdown
                            metadata = frontmatter_gen.extract_metadata_from_markdown(markdown_content)
                            # Generate new frontmatter with filename fallback
                            new_frontmatter = frontmatter_gen.generate(ssg_type.lower(), metadata, file.name)
                            # Replace old frontmatter with new one
                            if markdown_content.startswith('---'):
                                parts = markdown_content.split('---', 2)
                                if len(parts) >= 3:
                                    markdown_content = new_frontmatter + '\n\n' + parts[2].strip()
                            else:
                                # Add frontmatter to content without it
                                markdown_content = new_frontmatter + '\n\n' + markdown_content
                        
                        # Generate HTML if requested
                        html_content = None
                        seo_report = None
                        if output_format in ["HTML", "Both"]:
                            html_generator = HtmlGenerator(
                                template=html_template.lower(),
                                color_scheme=color_scheme.lower(),
                                font_family=font_family,
                                enable_seo=enable_seo
                            )
                            html_content = html_generator.generate(markdown_content, file.name)
                            
                            # Validate SEO if enabled
                            if enable_seo:
                                seo_report = html_generator.validate_seo(html_content, file.name)
                        
                        converted_files.append({
                            'original_name': file.name,
                            'markdown_content': markdown_content,
                            'html_content': html_content,
                            'file_type': file_ext,
                            'seo_report': seo_report
                        })
                        
                    else:
                        st.error(f"Unsupported file type: {file_ext}")
                        
                except Exception as e:
                    st.error(f"Error converting {file.name}: {str(e)}")
                
                progress_bar.progress((i + 1) / len(uploaded_files))
            
            status_text.text("Conversion complete!")
            st.session_state.converted_files = converted_files
            st.session_state.image_handler = image_handler
        
        # Display converted files if available
        if 'converted_files' in st.session_state and st.session_state.converted_files:
            converted_files = st.session_state.converted_files
            
            with tab2:
                st.subheader("Preview Converted Content")
                
                if converted_files:
                    selected_file = st.selectbox(
                        "Select file to preview:",
                        [f['original_name'] for f in converted_files]
                    )
                    
                    selected_content = next(
                        (f for f in converted_files if f['original_name'] == selected_file), 
                        None
                    )
                    
                    if selected_content:
                        preview_format = st.radio("Preview format:", ["Markdown", "HTML"], horizontal=True)
                        
                        if preview_format == "Markdown":
                            st.markdown("**Markdown Content:**")
                            st.code(selected_content['markdown_content'], language='markdown')
                            st.markdown("**Rendered Preview:**")
                            st.markdown(selected_content['markdown_content'])
                        else:
                            if selected_content['html_content']:
                                st.markdown("**HTML Content:**")
                                st.code(selected_content['html_content'], language='html')
                                st.markdown("**Rendered Preview:**")
                                import streamlit.components.v1 as components
                                components.html(selected_content['html_content'], height=400)
                            else:
                                st.warning("HTML content not generated. Select 'HTML' or 'Both' in conversion options.")
            
            with tab3:
                st.subheader("Download Converted Files")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**Individual Downloads:**")
                    for file_data in converted_files:
                        st.markdown(f"**{file_data['original_name']}**")
                        
                        # Markdown download
                        if output_format in ["Markdown", "Both"]:
                            markdown_filename = f"{os.path.splitext(file_data['original_name'])[0]}.md"
                            st.download_button(
                                label="📄 Download Markdown",
                                data=file_data['markdown_content'],
                                file_name=markdown_filename,
                                mime='text/markdown',
                                key=f"md_{file_data['original_name']}"
                            )
                        
                        # HTML download
                        if output_format in ["HTML", "Both"] and file_data['html_content']:
                            html_filename = f"{os.path.splitext(file_data['original_name'])[0]}.html"
                            st.download_button(
                                label="🌐 Download HTML",
                                data=file_data['html_content'],
                                file_name=html_filename,
                                mime='text/html',
                                key=f"html_{file_data['original_name']}"
                            )
                        
                        st.markdown("---")
                
                with col2:
                    st.markdown("**Batch Download:**")
                    
                    if st.button("📦 Create ZIP Archive"):
                        # Get image handler from session state if available
                        image_handler = st.session_state.get('image_handler', None)
                        zip_buffer = create_download_zip(converted_files, output_format, image_handler)
                        
                        st.download_button(
                            label="📥 Download ZIP Archive",
                            data=zip_buffer.getvalue(),
                            file_name="converted_files.zip",
                            mime='application/zip'
                        )
                    
                    st.markdown("---")
                    
                    st.markdown("**Static Site Generator:**")
                    
                    if output_format in ["HTML", "Both"]:
                        site_name = st.text_input("Site Name:", value="My Converted Documents", key="site_name")
                        
                        if st.button("🌐 Generate Static Site", type="primary"):
                            # Generate static site with selected template and styling
                            site_generator = StaticSiteGenerator(
                                template=html_template.lower(),
                                color_scheme=color_scheme.lower(),
                                font_family=font_family
                            )
                            # Get image handler from session state if available
                            image_handler = st.session_state.get('image_handler', None)
                            site_zip = site_generator.generate_site(converted_files, site_name, image_handler)
                            
                            st.success("Static site generated successfully!")
                            st.download_button(
                                label="📥 Download Static Site",
                                data=site_zip.getvalue(),
                                file_name=f"{site_name.lower().replace(' ', '_')}_site.zip",
                                mime='application/zip',
                                help="Download a complete static website with navigation"
                            )
                    else:
                        st.info("Select 'HTML' or 'Both' output format to generate a static site")
            
            with tab4:
                st.subheader("SEO Analysis Report")
                
                if converted_files:
                    # Check if any files have SEO reports
                    files_with_seo = [f for f in converted_files if f.get('seo_report')]
                    
                    if files_with_seo:
                        selected_file = st.selectbox(
                            "Select file to view SEO report:",
                            [f['original_name'] for f in files_with_seo],
                            key="seo_file_select"
                        )
                        
                        selected_data = next(
                            (f for f in files_with_seo if f['original_name'] == selected_file), 
                            None
                        )
                        
                        if selected_data and selected_data.get('seo_report'):
                            report = selected_data['seo_report']
                            score = report['score']
                            
                            # Display SEO score with color coding
                            col1, col2, col3 = st.columns([1, 2, 1])
                            with col1:
                                st.metric("SEO Score", f"{score}/100")
                            with col2:
                                from utils.seo_validator import get_seo_grade
                                grade = get_seo_grade(score)
                                grade_color = {
                                    'A': '🟢', 'B': '🟡', 'C': '🟠', 'D': '🔴', 'F': '⚫'
                                }
                                st.markdown(f"### Grade: {grade_color.get(grade, '')} {grade}")
                            
                            st.markdown("---")
                            
                            # Display issues, warnings, and successes
                            col1, col2, col3 = st.columns(3)
                            
                            with col1:
                                st.markdown("### ❌ Issues")
                                if report['issues']:
                                    for issue in report['issues']:
                                        st.error(issue)
                                else:
                                    st.success("No critical issues!")
                            
                            with col2:
                                st.markdown("### ⚠️ Warnings")
                                if report['warnings']:
                                    for warning in report['warnings']:
                                        st.warning(warning)
                                else:
                                    st.info("No warnings")
                            
                            with col3:
                                st.markdown("### ✅ Successes")
                                if report['successes']:
                                    for success in report['successes']:
                                        st.success(success)
                            
                            # Display recommendations
                            if report['recommendations']:
                                st.markdown("---")
                                st.markdown("### 💡 Recommendations")
                                for i, rec in enumerate(report['recommendations'], 1):
                                    st.markdown(f"{i}. {rec}")
                    else:
                        st.info("Enable SEO enhancements and generate HTML to see SEO reports")
                else:
                    st.info("Convert files first to view SEO reports")
    
    else:
        st.info("👆 Please upload one or more files to get started")
        
        # Show supported formats
        st.markdown("### Supported File Formats")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown("**DOCX**\n- Word documents\n- Preserves formatting\n- Extracts text and structure")
        
        with col2:
            st.markdown("**CSV**\n- Comma-separated values\n- Converts to tables\n- Maintains data structure")
        
        with col3:
            st.markdown("**TXT**\n- Plain text files\n- Preserves line breaks\n- Basic formatting")
        
        with col4:
            st.markdown("**WXR**\n- WordPress export\n- Extracts posts/pages\n- Preserves metadata")

if __name__ == "__main__":
    main()
