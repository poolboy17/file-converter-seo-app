import os

import streamlit as st

from converters.csv_converter import CsvConverter
from converters.docx_converter import DocxConverter
from converters.txt_converter import TxtConverter
from converters.wxr_converter import WxrConverter
from utils.file_utils import create_download_zip, get_file_extension
from utils.frontmatter_generator import FrontmatterGenerator
from utils.image_handler import ImageHandler

# Constants
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB limit
SUPPORTED_EXTENSIONS = ["docx", "csv", "txt", "wxr"]


# Initialize converters with caching
@st.cache_resource
def get_converters():
    """Get cached converter instances for better performance."""
    return {
        "docx": DocxConverter(),
        "csv": CsvConverter(),
        "txt": TxtConverter(),
        "wxr": WxrConverter(),
    }


converters = get_converters()


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
    st.markdown(
        "Convert DOCX, CSV, TXT, and WXR files to clean Markdown"
    )

    # Help section
    with st.expander("ℹ️ How to Use This Tool", expanded=False):
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
        "**Supported formats**: DOCX, CSV, TXT, WXR | "
        "**Max file size**: 50MB per file"
    )

    uploaded_files = st.file_uploader(
        "Choose files to convert",
        type=["docx", "csv", "txt", "wxr"],
        accept_multiple_files=True,
        help="Supported formats: DOCX, CSV, TXT, WXR",
    )

    if uploaded_files:
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
        tab1, tab2, tab3 = st.tabs(
            ["📋 File List", "👀 Preview", "📥 Download"]
        )

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
                    st.write(f".{file_ext}")
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

                try:
                    file_ext = get_file_extension(file.name)

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

                    else:
                        st.error(f"❌ Unsupported file type: {file_ext}")

                except PermissionError:
                    st.error(
                        f"❌ **Permission denied**: Cannot read {file.name}. "
                        f"Please check file permissions."
                    )
                except MemoryError:
                    st.error(
                        f"❌ **Memory error**: {file.name} is too large to process. "
                        f"Try a smaller file."
                    )
                except UnicodeDecodeError:
                    # Handle encoding errors first (subclass of ValueError)
                    st.error(
                        f"❌ **Encoding error** in {file.name}: "
                        f"File contains invalid characters. Try saving with UTF-8."
                    )
                except ValueError as ve:
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

                    if st.button("📦 Create ZIP Archive"):
                        with st.spinner("📦 Creating ZIP archive..."):
                            try:
                                # Get image handler from session state
                                image_handler = st.session_state.get(
                                    "image_handler", None
                                )
                                zip_buffer = create_download_zip(
                                    converted_files, "Markdown", image_handler
                                )
                                st.success("✅ ZIP archive ready!")
                            except Exception as e:
                                st.error("❌ **Error creating ZIP archive**")
                                with st.expander("Show Error Details"):
                                    st.code(str(e))
                                st.stop()

                        st.download_button(
                            label="📥 Download ZIP Archive",
                            data=zip_buffer.getvalue(),
                            file_name="converted_files.zip",
                            mime="application/zip",
                        )


    else:
        st.info("👆 Please upload one or more files to get started")

        # Show supported formats
        st.markdown("### Supported File Formats")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.markdown(
                "**DOCX**\n- Word documents\n- Preserves formatting\n- Extracts text and structure"
            )

        with col2:
            st.markdown(
                "**CSV**\n- Comma-separated values\n- Converts to tables\n- Maintains data structure"
            )

        with col3:
            st.markdown(
                "**TXT**\n- Plain text files\n- Preserves line breaks\n- Basic formatting"
            )

        with col4:
            st.markdown(
                "**WXR**\n- WordPress export\n- Extracts posts/pages\n- Preserves metadata"
            )


if __name__ == "__main__":
    main()
