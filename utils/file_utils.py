import os
import zipfile
import io
from datetime import datetime
from typing import List, Dict

def get_file_extension(filename):
    """Get file extension from filename."""
    return os.path.splitext(filename)[1][1:].lower()

def create_download_zip(converted_files: List[Dict], output_format: str, image_handler=None):
    """
    Create a ZIP file containing all converted files.
    
    Args:
        converted_files: List of converted file data
        output_format: Output format ("Markdown", "HTML", or "Both")
        image_handler: Optional ImageHandler with extracted images
        
    Returns:
        io.BytesIO: ZIP file buffer
    """
    zip_buffer = io.BytesIO()
    
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for file_data in converted_files:
            base_name = os.path.splitext(file_data['original_name'])[0]
            
            # Add markdown file
            if output_format in ["Markdown", "Both"]:
                markdown_filename = f"{base_name}.md"
                zip_file.writestr(markdown_filename, file_data['markdown_content'])
            
            # Add HTML file
            if output_format in ["HTML", "Both"] and file_data['html_content']:
                html_filename = f"{base_name}.html"
                zip_file.writestr(html_filename, file_data['html_content'])
            
            # Add metadata file
            metadata = create_file_metadata(file_data)
            metadata_filename = f"{base_name}_metadata.txt"
            zip_file.writestr(metadata_filename, metadata)
        
        # Add extracted/downloaded images to assets folder
        if image_handler and hasattr(image_handler, 'images'):
            images = image_handler.get_all_images()
            if images:
                for image_hash, filename in images.items():
                    # Get the image data - we need to store it in the handler
                    if hasattr(image_handler, 'image_data') and image_hash in image_handler.image_data:
                        image_data = image_handler.image_data[image_hash]
                        zip_file.writestr(f"assets/{filename}", image_data)
    
    zip_buffer.seek(0)
    return zip_buffer

def create_file_metadata(file_data: Dict) -> str:
    """Create a metadata summary for a converted file."""
    metadata_lines = [
        f"File Conversion Metadata",
        f"========================",
        f"",
        f"Original filename: {file_data['original_name']}",
        f"File type: {file_data['file_type'].upper()}",
        f"Conversion date: {datetime.now().isoformat()}",
        f"",
        f"Content statistics:",
        f"- Markdown length: {len(file_data['markdown_content'])} characters",
        f"- Markdown lines: {len(file_data['markdown_content'].splitlines())}",
    ]
    
    if file_data['html_content']:
        metadata_lines.extend([
            f"- HTML length: {len(file_data['html_content'])} characters",
            f"- HTML lines: {len(file_data['html_content'].splitlines())}",
        ])
    
    # Add file-specific metadata
    if file_data['file_type'] == 'csv':
        # Count tables in markdown
        table_count = file_data['markdown_content'].count('|')
        if table_count > 0:
            metadata_lines.append(f"- Estimated table cells: {table_count}")
    
    elif file_data['file_type'] == 'docx':
        # Count headings
        heading_count = len([line for line in file_data['markdown_content'].splitlines() if line.strip().startswith('#')])
        metadata_lines.append(f"- Headings found: {heading_count}")
    
    elif file_data['file_type'] == 'wxr':
        # Count posts/pages
        post_separators = file_data['markdown_content'].count('---')
        metadata_lines.append(f"- Estimated posts/pages: {max(1, post_separators // 2)}")
    
    return '\n'.join(metadata_lines)

def sanitize_filename(filename):
    """Sanitize filename for safe file system usage."""
    # Remove or replace problematic characters
    import re
    
    # Replace problematic characters with underscores
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    
    # Remove control characters
    filename = re.sub(r'[\x00-\x1f\x7f]', '', filename)
    
    # Limit length
    if len(filename) > 255:
        name, ext = os.path.splitext(filename)
        filename = name[:255-len(ext)] + ext
    
    # Ensure it doesn't start with a dot (hidden file)
    if filename.startswith('.'):
        filename = '_' + filename[1:]
    
    return filename

def format_file_size(size_bytes):
    """Format file size in human readable format."""
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    
    return f"{size_bytes:.1f} {size_names[i]}"

def validate_file_type(filename, allowed_extensions):
    """Validate if file type is allowed."""
    ext = get_file_extension(filename)
    return ext in allowed_extensions

def clean_text_content(text):
    """Clean text content for better markdown conversion."""
    if not text:
        return ""
    
    import re
    
    # Normalize line endings
    text = re.sub(r'\r\n?', '\n', text)
    
    # Remove excessive whitespace
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = re.sub(r'[ \t]{2,}', ' ', text)
    
    # Remove trailing whitespace from lines
    text = '\n'.join(line.rstrip() for line in text.split('\n'))
    
    # Ensure text ends with a newline
    if text and not text.endswith('\n'):
        text += '\n'
    
    return text
