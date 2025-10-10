import os

import streamlit as st

from converters.csv_converter import CsvConverter
from converters.docx_converter import DocxConverter
from converters.txt_converter import TxtConverter
from converters.wxr_converter import WxrConverter
from utils.file_utils import create_download_zip, get_file_extension
from utils.frontmatter_generator import FrontmatterGenerator
from utils.image_handler import ImageHandler
from utils.logger import (
    setup_logger,
    log_file_info,
    log_conversion_start,
    log_conversion_success,
    log_conversion_error,
    log_zip_creation,
)


# Constants
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB limit
SUPPORTED_EXTENSIONS = ["docx", "csv", "txt", "wxr", "xml"]

# Initialize logger
logger = setup_logger("file_converter", "DEBUG")
logger.info("=" * 60)
logger.info("Application starting")
logger.info("=" * 60)

# Initialize converters with caching
@st.cache_resource
def get_converters():
    """Get cached converter instances for better performance."""
    logger.info("Initializing converters...")
    return {
        "docx": DocxConverter(),
        "csv": CsvConverter(),
        "txt": TxtConverter(),
        "wxr": WxrConverter(),
    }


converters = get_converters()
logger.info(f"Converters ready: {list(converters.keys())}")


def validate_files(uploaded_files):
    """Validate uploaded files before processing."""
    errors = []
    warnings = []

    for file in uploaded_files:
        # Check size
        if file.size > MAX_FILE_SIZE:
            errors.append(
                f"❌ **{file.name}**: File too large ({file.size / (1024*1024):.1f}MB). "
                f"Maximum size is 50MB."
            )
            continue

        # Check if file is empty
        if file.size == 0:
            errors.append(f"❌ **{file.name}**: File is empty.")
            continue

        # Check extension
        ext = get_file_extension(file.name)
        if ext not in SUPPORTED_EXTENSIONS:
            errors.append(
                f"❌ **{file.name}**: Unsupported format '.{ext}'. "
                f"Supported formats: {', '.join(SUPPORTED_EXTENSIONS)}"
            )
            continue

        # Check if file might be corrupted
        try:
            file.seek(0)
            file.read(100)  # Try reading first 100 bytes
            file.seek(0)  # Reset file pointer
        except Exception:
            errors.append(
                f"❌ **{file.name}**: File appears to be corrupted or unreadable."
            )
            continue

        # Warn about large files
        if file.size > 10 * 1024 * 1024:  # 10MB
            warnings.append(
                f"⚠️ **{file.name}**: Large file ({file.size / (1024*1024):.1f}MB). "
                f"Processing may take longer."
            )

    return errors, warnings


def main():
    st.set_page_config(
        page_title="File to Markdown Converter", page_icon="📄", layout="wide"
    )

    st.title("📄 File to Markdown Converter")
    st.markdown("Convert DOCX, CSV, TXT, and WXR files to clean Markdown")

    # Help section - expanded by default on first visit
    if "help_shown" not in st.session_state:
        st.session_state.help_shown = True
        help_expanded = True
    else:
        help_expanded = False

    with st.expander("ℹ️ How to Use This Tool", expanded=help_expanded):
        st.markdown(
            """
        ### Quick Start Guide

        1. **📤 Upload Files**: Upload DOCX, CSV, TXT, or WXR files (max 50MB each)
        2. **⚙️ Configure Options**: Customize conversion settings in the sidebar
        3. **🔄 Convert**: Click the 'Convert All Files' button
        4. **📊 Review**: Check the File List and Preview tabs
        5. **⬇️ Download**: Get individual Markdown files or ZIP archive

        ### Supported Features
        - **Multiple Formats**: Convert 4 different file types to Markdown
        - **SSG Frontmatter**: Add Jekyll, Hugo, or Astro frontmatter
        - **Image Extraction**: Extract and optimize images from DOCX/WXR files
        - **Batch Processing**: Convert multiple files simultaneously

        ### Tips
        - 💡 Large files (>10MB) may take longer to process
        - 💡 Add frontmatter for static site generators (Jekyll, Hugo, Astro)
        - 💡 Use the Preview tab to check output before downloading
        """
        )

    # Sidebar for options
    st.sidebar.header("⚙️ Configuration")

    # Quick Presets at top
    st.sidebar.markdown("### ⚡ Quick Presets")
    preset = st.sidebar.selectbox(
        "Load Preset:",
        ["Custom", "Jekyll Blog", "Hugo Docs", "Astro Site", "Plain Markdown"],
        help="Load pre-configured settings for common use cases",
    )

    # Reset button
    if st.sidebar.button(
        "🔄 Reset All", help="Clear all uploaded files and reset state"
    ):
        # Clear all session state keys (list() needed for safe deletion)
        for key in list(st.session_state.keys()):  # noqa: SIM118
            del st.session_state[key]
        st.rerun()

    st.sidebar.markdown("---")

    # Conversion Options in expander
    with st.sidebar.expander("📝 Conversion Options", expanded=True):
        include_metadata = st.checkbox("Include metadata", value=True)

    # Frontmatter options in expander
    with st.sidebar.expander("📋 Frontmatter Options", expanded=False):
        add_frontmatter = st.checkbox(
            "Add SSG frontmatter",
            value=False,
            help="Add frontmatter for static site generators",
        )
        ssg_type = None
        if add_frontmatter:
            ssg_type = st.selectbox(
                "Static Site Generator",
                ["Jekyll", "Hugo", "Astro"],
                help="Choose your static site generator",
                key="ssg_type",
            )

    # Apply preset configurations
    if preset == "Jekyll Blog":
        add_frontmatter = True
        ssg_type = "Jekyll"
        st.sidebar.success("✅ Jekyll Blog preset loaded")
    elif preset == "Hugo Docs":
        add_frontmatter = True
        ssg_type = "Hugo"
        st.sidebar.success("✅ Hugo Docs preset loaded")
    elif preset == "Astro Site":
        add_frontmatter = True
        ssg_type = "Astro"
        st.sidebar.success("✅ Astro Site preset loaded")
    elif preset == "Plain Markdown":
        add_frontmatter = False
        st.sidebar.success("✅ Plain Markdown preset loaded")

    # File upload section
    st.markdown("---")
    st.header("📤 Upload Files")
    st.info(
        "**Supported formats**: DOCX, CSV, TXT, WXR/XML (WordPress exports) | "
        "**Max file size**: 50MB per file"
    )

    uploaded_files = st.file_uploader(
        "Choose files to convert",
        type=["docx", "csv", "txt", "wxr", "xml"],
        accept_multiple_files=True,
        help="Supported formats: DOCX, CSV, TXT, WXR, XML (WordPress exports)",
        label_visibility="visible",
    )

    # Always show the interface, even without files
    if uploaded_files and len(uploaded_files) > 0:
        # Validate files
        validation_errors, validation_warnings = validate_files(uploaded_files)

        # Display validation errors
        if validation_errors:
            st.error("**⛔ Cannot proceed - Please fix these errors:**")
            for error in validation_errors:
                st.markdown(error)
            st.stop()

        # Display validation warnings
        if validation_warnings:
            st.warning("**⚠️ Warnings:**")
            for warning in validation_warnings:
                st.markdown(warning)

        st.success(f"✅ Uploaded {len(uploaded_files)} file(s)")

        # Process files
        converted_files = []

        # Create tabs for different views
        tab1, tab2, tab3 = st.tabs(["📋 File List", "👀 Preview", "📥 Download"])

        with tab1:
            st.subheader("Files to Convert")

            # Store files in session state for deletion tracking
            if "uploaded_files_list" not in st.session_state:
                st.session_state.uploaded_files_list = list(uploaded_files)

            files_to_remove = []

            for idx, file in enumerate(uploaded_files):
                col1, col2, col3, col4, col5 = st.columns([3, 1, 1, 1, 1])
                with col1:
                    st.write(f"**{file.name}**")
                with col2:
                    st.write(f"{file.size / 1024:.1f} KB")
                with col3:
                    file_ext = get_file_extension(file.name)
                    # Display XML as WXR for clarity
                    display_ext = "wxr (WordPress)" if file_ext == "xml" else file_ext
                    st.write(f".{display_ext}")
                with col4:
                    # Preview button
                    if st.button("👁️", key=f"preview_{idx}", help="Preview file"):
                        with st.expander(f"📄 Preview: {file.name}", expanded=True):
                            try:
                                file.seek(0)
                                # Read first 1000 chars for preview
                                content = file.read(1000).decode(
                                    "utf-8", errors="ignore"
                                )
                                if len(content) == 1000:
                                    content += "\n\n... (preview truncated)"
                                st.code(
                                    content,
                                    language=file_ext if file_ext != "wxr" else "xml",
                                )
                                file.seek(0)  # Reset file pointer
                            except Exception as e:
                                st.error(f"Cannot preview: {str(e)}")
                with col5:
                    # Delete button
                    if st.button("🗑️", key=f"delete_{idx}", help="Remove file"):
                        files_to_remove.append(file.name)

            # Handle file deletion
            if files_to_remove:
                st.warning(f"🗑️ Removed {len(files_to_remove)} file(s)")
                st.rerun()

        # Convert button
        if st.button("🔄 Convert All Files", type="primary"):
            progress_bar = st.progress(0)
            status_text = st.empty()

            # Create image handler for extracting/downloading images
            image_handler = ImageHandler()

            for i, file in enumerate(uploaded_files):
                status_text.text(f"Converting {file.name}...")

                # Log file details
                log_file_info(logger, file, f"File {i+1}/{len(uploaded_files)}")

                try:
                    file_ext = get_file_extension(file.name)
                    log_conversion_start(logger, file.name, file_ext)

                    # Treat XML files as WXR (WordPress exports)
                    if file_ext == "xml":
                        logger.debug(f"  → Treating {file.name} as WXR (WordPress)")
                        file_ext = "wxr"

                    if file_ext in converters:
                        # Convert to markdown with image extraction/downloading
                        if file_ext in ["docx", "wxr"]:
                            markdown_content = converters[file_ext].convert(
                                file, include_metadata, image_handler
                            )
                        else:
                            markdown_content = converters[file_ext].convert(
                                file, include_metadata
                            )

                        # Apply SSG frontmatter if requested
                        if add_frontmatter and ssg_type:
                            frontmatter_gen = FrontmatterGenerator()
                            # Extract existing metadata from markdown
                            metadata = frontmatter_gen.extract_metadata_from_markdown(
                                markdown_content
                            )
                            # Generate new frontmatter with filename fallback
                            new_frontmatter = frontmatter_gen.generate(
                                ssg_type.lower(), metadata, file.name
                            )
                            # Replace old frontmatter with new one
                            if markdown_content.startswith("---"):
                                parts = markdown_content.split("---", 2)
                                if len(parts) >= 3:
                                    markdown_content = (
                                        new_frontmatter + "\n\n" + parts[2].strip()
                                    )
                            else:
                                # Add frontmatter to content without it
                                markdown_content = (
                                    new_frontmatter + "\n\n" + markdown_content
                                )

                        converted_files.append(
                            {
                                "original_name": file.name,
                                "markdown_content": markdown_content,
                                "file_type": file_ext,
                            }
                        )

                        # Log success
                        log_conversion_success(
                            logger, file.name, len(markdown_content)
                        )

                    else:
                        logger.error(f"Unsupported file type: {file_ext}")
                        st.error(f"❌ Unsupported file type: {file_ext}")

                except PermissionError as e:
                    log_conversion_error(logger, file.name, e)
                    st.error(
                        f"❌ **Permission denied**: Cannot read {file.name}. "
                        f"Please check file permissions."
                    )
                except MemoryError as e:
                    log_conversion_error(logger, file.name, e)
                    st.error(
                        f"❌ **Memory error**: {file.name} is too large to process. "
                        f"Try a smaller file."
                    )
                except UnicodeDecodeError as e:
                    # Handle encoding errors first (subclass of ValueError)
                    log_conversion_error(logger, file.name, e)
                    st.error(
                        f"❌ **Encoding error** in {file.name}: "
                        f"File contains invalid characters. Try saving with UTF-8."
                    )
                except ValueError as ve:
                    log_conversion_error(logger, file.name, ve)
                    st.error(f"❌ **Invalid format** in {file.name}: {str(ve)}")
                    with st.expander("Show Error Details"):
                        st.code(str(ve))
                except Exception as e:
                    st.error(f"❌ **Unexpected error** converting {file.name}")
                    with st.expander("Show Error Details"):
                        st.code(str(e))
                        st.caption(
                            "If this error persists, the file may be corrupted "
                            "or in an unsupported format variation."
                        )

                progress_bar.progress((i + 1) / len(uploaded_files))

            status_text.success("✅ Conversion complete!")
            st.session_state.converted_files = converted_files
            st.session_state.image_handler = image_handler

        # Display converted files if available
        if "converted_files" in st.session_state and st.session_state.converted_files:
            converted_files = st.session_state.converted_files

            with tab2:
                st.subheader("Preview Converted Content")

                if converted_files:
                    selected_file = st.selectbox(
                        "Select file to preview:",
                        [f["original_name"] for f in converted_files],
                    )

                    selected_content = next(
                        (
                            f
                            for f in converted_files
                            if f["original_name"] == selected_file
                        ),
                        None,
                    )

                    if selected_content:
                        st.markdown("### 📝 Markdown Content")
                        with st.expander("View Source", expanded=False):
                            st.code(
                                selected_content["markdown_content"],
                                language="markdown",
                            )
                        st.markdown("### Rendered Preview")
                        st.markdown(selected_content["markdown_content"])

            with tab3:
                st.subheader("Download Converted Files")
                st.info(
                    "💡 **Where are files saved?** Click the download buttons "
                    "below to save files to your browser's download folder "
                    "(usually `Downloads/` or `My Documents/Downloads/`)"
                )

                col1, col2 = st.columns(2)

                with col1:
                    st.markdown("**Individual Downloads:**")
                    for file_data in converted_files:
                        st.markdown(f"**{file_data['original_name']}**")

                        # Markdown download
                        markdown_filename = (
                            f"{os.path.splitext(file_data['original_name'])[0]}.md"
                        )
                        st.download_button(
                            label="📄 Download Markdown",
                            data=file_data["markdown_content"],
                            file_name=markdown_filename,
                            mime="text/markdown",
                            key=f"md_{file_data['original_name']}",
                        )

                        st.markdown("---")

                with col2:
                    st.markdown("**Batch Download:**")

                    # Choose SSG structure
                    ssg_choice = st.selectbox(
                        "Folder structure:",
                        ["Flat (root)", "Hugo", "Jekyll", "Astro"],
                        help="Each article gets its own folder with index.md",
                    )

                    if st.button("📦 Create ZIP Archive"):
                        with st.spinner("📦 Creating ZIP archive..."):
                            try:
                                # Get image handler from session state
                                image_handler = st.session_state.get(
                                    "image_handler", None
                                )
                                logger.debug(
                                    f"Image handler found: {image_handler is not None}"
                                )

                                # Map choice to structure parameter
                                ssg_map = {
                                    "Hugo": "hugo",
                                    "Jekyll": "jekyll",
                                    "Astro": "astro",
                                    "Flat (root)": None,
                                }
                                ssg_struct = ssg_map.get(ssg_choice)

                                log_zip_creation(
                                    logger, len(converted_files), ssg_struct
                                )

                                zip_buffer = create_download_zip(
                                    converted_files,
                                    "Markdown",
                                    image_handler,
                                    ssg_structure=ssg_struct,
                                )
                                logger.info(
                                    f"ZIP created successfully: "
                                    f"{len(converted_files)} files"
                                )

                                # Store in session state for download button
                                st.session_state.zip_buffer = zip_buffer
                                st.session_state.ssg_choice = ssg_choice

                                st.success(
                                    f"✅ ZIP ready! {len(converted_files)} "
                                    f"articles in separate folders"
                                )
                            except Exception as e:
                                logger.error("ZIP creation failed")
                                logger.exception(e)
                                st.error("❌ **Error creating ZIP archive**")
                                with st.expander("Show Error Details"):
                                    st.code(str(e))
                                st.stop()

                    # Show download button if ZIP has been created
                    if "zip_buffer" in st.session_state:
                        st.download_button(
                            label="📥 Download ZIP Archive",
                            data=st.session_state.zip_buffer.getvalue(),
                            file_name="converted_files.zip",
                            mime="application/zip",
                        )

                        # Show folder structure info
                        ssg_choice_display = st.session_state.get(
                            "ssg_choice", ssg_choice
                        )
                        if ssg_choice_display == "Hugo":
                            st.caption(
                                "📁 `content/posts/<article-name>/index.md` - "
                                "Each article in its own folder\n"
                                "📁 `assets/images/` - Image assets"
                            )
                        elif ssg_choice_display == "Jekyll":
                            st.caption(
                                "📁 `_posts/<article-name>/index.md` - "
                                "Each article in its own folder\n"
                                "📁 `assets/images/` - Image assets"
                            )
                        elif ssg_choice_display == "Astro":
                            st.caption(
                                "📁 `src/content/blog/<article-name>/index.md` - "
                                "Each article in its own folder\n"
                                "📁 `assets/images/` - Image assets"
                            )
                        else:
                            st.caption(
                                "📁 `<article-name>/index.md` - "
                                "Each article in its own folder\n"
                                "📁 `assets/` - Image assets"
                            )

    else:
        # Show workflow guide prominently
        st.success("✨ **Ready to Convert!** Upload files above to begin")

        # Workflow steps
        st.markdown("### 📋 Conversion Workflow")
        st.markdown(
            """
        <div style="background-color: #f0f2f6; padding: 20px;
        border-radius: 10px; margin: 10px 0;">
        <h4>Follow these steps:</h4>
        <ol style="font-size: 16px; line-height: 1.8;">
            <li>📤 <b>Upload files</b> using the file uploader above</li>
            <li>⚙️ <b>Configure options</b> in the sidebar (optional)</li>
            <li>🔄 <b>Click "Convert All Files"</b> button (appears after upload)</li>
            <li>👀 <b>Preview results</b> in the Preview tab</li>
            <li>📥 <b>Download</b> individual files or ZIP archive</li>
        </ol>
        </div>
        """,
            unsafe_allow_html=True,
        )

        st.markdown("---")

        # Show supported formats
        st.markdown("### 📂 Supported File Formats")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.markdown(
                "**DOCX**\n"
                "- Word documents\n"
                "- Preserves formatting\n"
                "- Extracts text and structure"
            )

        with col2:
            st.markdown(
                "**CSV**\n"
                "- Comma-separated values\n"
                "- Converts to tables\n"
                "- Maintains data structure"
            )

        with col3:
            st.markdown(
                "**TXT**\n"
                "- Plain text files\n"
                "- Preserves line breaks\n"
                "- Basic formatting"
            )

        with col4:
            st.markdown(
                "**WXR/XML**\n"
                "- WordPress exports (.xml)\n"
                "- Extracts posts/pages\n"
                "- Preserves metadata"
            )


if __name__ == "__main__":
    main()
