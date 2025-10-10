import io
import os
import zipfile
from datetime import datetime

from utils.logger import setup_logger

# Initialize logger
logger = setup_logger("file_utils", "DEBUG")


def get_file_extension(filename):
    """Get file extension from filename."""
    return os.path.splitext(filename)[1][1:].lower()


def create_download_zip(
    converted_files: list[dict],
    output_format: str,
    image_handler=None,
    ssg_structure: str | None = None,
):
    """
    Create a ZIP file containing all converted files.

    Args:
        converted_files: List of converted file data
        output_format: Output format ("Markdown", "HTML", or "Both")
        image_handler: Optional ImageHandler with extracted images
        ssg_structure: SSG type for folder structure
                      ("hugo", "jekyll", "astro", or None for flat)

    Returns:
        io.BytesIO: ZIP file buffer
    """
    logger.info(
        f"Creating ZIP: {len(converted_files)} files, "
        f"structure={ssg_structure}"
    )
    zip_buffer = io.BytesIO()

    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
        # Set base path based on SSG structure
        if ssg_structure == "hugo":
            base_dir = "content/posts/"
            logger.debug(
                f"Using Hugo structure with individual folders: {base_dir}"
            )
        elif ssg_structure == "jekyll":
            base_dir = "_posts/"
            logger.debug(
                f"Using Jekyll structure with individual folders: {base_dir}"
            )
        elif ssg_structure == "astro":
            base_dir = "src/content/blog/"
            logger.debug(
                f"Using Astro structure with individual folders: {base_dir}"
            )
        else:
            base_dir = ""
            logger.debug("Using flat structure with individual folders")

        for file_data in converted_files:
            base_name = sanitize_filename(
                os.path.splitext(file_data["original_name"])[0]
            )
            logger.debug(f"Processing: {file_data['original_name']}")

            # Create individual folder for each article
            article_folder = f"{base_dir}{base_name}/"

            # Add markdown file in its own folder
            if output_format in ["Markdown", "Both"]:
                markdown_filename = f"{article_folder}index.md"
                zip_file.writestr(markdown_filename, file_data["markdown_content"])
                logger.debug(f"  → Added: {markdown_filename}")

            # Add HTML file in article folder
            if output_format in ["HTML", "Both"] and file_data["html_content"]:
                html_filename = f"{article_folder}index.html"
                zip_file.writestr(html_filename, file_data["html_content"])
                logger.debug(f"  → Added: {html_filename}")

            # Add metadata file in article folder
            metadata = create_file_metadata(file_data)
            metadata_filename = f"{article_folder}metadata.txt"
            zip_file.writestr(metadata_filename, metadata)
            logger.debug(f"  → Added: {metadata_filename}")

        # Add extracted/downloaded images to their respective article folders
        if image_handler and hasattr(image_handler, "images"):
            images = image_handler.get_all_images()
            logger.info(f"Processing {len(images)} images")
            if images:
                # Group images by article if possible, otherwise put in shared assets
                for image_hash, filename in images.items():
                    # Get the image data - we need to store it in the handler
                    if (
                        hasattr(image_handler, "image_data")
                        and image_hash in image_handler.image_data
                    ):
                        image_data = image_handler.image_data[image_hash]

                        # Try to determine which article this image belongs to
                        # For now, put all images in a shared assets folder
                        # (could be enhanced to parse markdown and
                        # associate images)
                        if ssg_structure:
                            img_path = f"assets/images/{filename}"
                        else:
                            img_path = f"assets/{filename}"

                        zip_file.writestr(img_path, image_data)
                        logger.debug(f"  → Added image: {img_path}")
                    else:
                        logger.warning(f"  ⚠ Missing image data for: {filename}")
        else:
            logger.info("No image handler or no images to process")

    zip_buffer.seek(0)
    logger.info(
        f"ZIP creation complete. Buffer size: "
        f"{len(zip_buffer.getvalue())} bytes"
    )
    return zip_buffer


def create_file_metadata(file_data: dict) -> str:
    """Create a metadata summary for a converted file."""
    metadata_lines = [
        "File Conversion Metadata",
        "========================",
        "",
        f"Original filename: {file_data['original_name']}",
        f"File type: {file_data['file_type'].upper()}",
        f"Conversion date: {datetime.now().isoformat()}",
        "",
        "Content statistics:",
        f"- Markdown length: {len(file_data['markdown_content'])} characters",
        f"- Markdown lines: {len(file_data['markdown_content'].splitlines())}",
    ]

    if file_data["html_content"]:
        metadata_lines.extend(
            [
                f"- HTML length: {len(file_data['html_content'])} characters",
                f"- HTML lines: {len(file_data['html_content'].splitlines())}",
            ]
        )

    # Add file-specific metadata
    if file_data["file_type"] == "csv":
        # Count tables in markdown
        table_count = file_data["markdown_content"].count("|")
        if table_count > 0:
            metadata_lines.append(f"- Estimated table cells: {table_count}")

    elif file_data["file_type"] == "docx":
        # Count headings
        heading_count = len(
            [
                line
                for line in file_data["markdown_content"].splitlines()
                if line.strip().startswith("#")
            ]
        )
        metadata_lines.append(f"- Headings found: {heading_count}")

    elif file_data["file_type"] == "wxr":
        # Count posts/pages
        post_separators = file_data["markdown_content"].count("---")
        metadata_lines.append(
            f"- Estimated posts/pages: {max(1, post_separators // 2)}"
        )

    return "\n".join(metadata_lines)


def sanitize_filename(filename):
    """Sanitize filename for safe file system usage."""
    # Remove or replace problematic characters
    import re

    # Replace problematic characters with underscores
    filename = re.sub(r'[<>:"/\\|?*]', "_", filename)

    # Remove control characters
    filename = re.sub(r"[\x00-\x1f\x7f]", "", filename)

    # Limit length
    if len(filename) > 255:
        name, ext = os.path.splitext(filename)
        filename = name[: 255 - len(ext)] + ext

    # Ensure it doesn't start with a dot (hidden file)
    if filename.startswith("."):
        filename = "_" + filename[1:]

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
    text = re.sub(r"\r\n?", "\n", text)

    # Remove excessive whitespace
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"[ \t]{2,}", " ", text)

    # Remove trailing whitespace from lines
    text = "\n".join(line.rstrip() for line in text.split("\n"))

    # Ensure text ends with a newline
    if text and not text.endswith("\n"):
        text += "\n"

    return text
