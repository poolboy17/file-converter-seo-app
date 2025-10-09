import hashlib
import io
import urllib.error
import urllib.request

from PIL import Image


class ImageHandler:
    """Handle image extraction, downloading, and conversion."""

    def __init__(self):
        self.images = {}  # Map: image_hash -> local_filename
        self.image_data = {}  # Map: image_hash -> binary_data
        self.image_counter = 0

    def extract_docx_images(self, doc) -> dict[str, bytes]:
        """
        Extract embedded images from DOCX file.

        Args:
            doc: python-docx Document object

        Returns:
            Dict mapping image IDs to image binary data
        """
        images = {}

        try:
            # Access the document's image parts
            for rel in doc.part.rels.values():
                if "image" in rel.target_ref:
                    image_part = rel.target_part
                    image_id = rel.rId
                    image_data = image_part.blob

                    # Get the image format from the content type
                    content_type = image_part.content_type
                    ext = self._get_extension_from_content_type(content_type)

                    images[image_id] = {
                        "data": image_data,
                        "ext": ext,
                        "content_type": content_type,
                    }
        except Exception as e:
            print(f"Warning: Could not extract images from DOCX: {str(e)}")

        return images

    def download_image(
        self, url: str, timeout: int = 10
    ) -> tuple[bytes, str] | None:
        """
        Download an image from a URL.

        Args:
            url: Image URL
            timeout: Request timeout in seconds

        Returns:
            Tuple of (image_data, extension) or None if download failed
        """
        try:
            # Set a user agent to avoid blocks
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})

            with urllib.request.urlopen(req, timeout=timeout) as response:
                image_data = response.read()
                content_type = response.headers.get("Content-Type", "")
                ext = self._get_extension_from_content_type(content_type)

                # If extension not found from content type, try URL
                if not ext:
                    ext = self._get_extension_from_url(url)

                return (image_data, ext)

        except (urllib.error.URLError, urllib.error.HTTPError, Exception) as e:
            print(f"Warning: Could not download image from {url}: {str(e)}")
            return None

    def save_image(self, image_data: bytes, ext: str, prefix: str = "image") -> str:
        """
        Generate a filename for an image and store the mapping.

        Args:
            image_data: Binary image data
            ext: File extension (e.g., 'png', 'jpg')
            prefix: Filename prefix

        Returns:
            Generated filename
        """
        # Create a hash of the image data to avoid duplicates
        image_hash = hashlib.md5(image_data).hexdigest()[:8]

        # Check if we've already saved this image
        if image_hash in self.images:
            return self.images[image_hash]

        # Generate new filename
        self.image_counter += 1
        filename = f"{prefix}_{self.image_counter}_{image_hash}.{ext}"

        # Store mapping and data
        self.images[image_hash] = filename
        self.image_data[image_hash] = image_data

        return filename

    def optimize_image(
        self, image_data: bytes, max_width: int = 1200, quality: int = 85
    ) -> tuple[bytes, str]:
        """
        Optimize an image by resizing and compressing.

        Args:
            image_data: Binary image data
            max_width: Maximum width in pixels
            quality: JPEG quality (1-100)

        Returns:
            Tuple of (optimized_data, extension)
        """
        try:
            # Open image
            img = Image.open(io.BytesIO(image_data))

            # Convert RGBA to RGB if saving as JPEG
            if img.mode == "RGBA":
                # Create white background
                background = Image.new("RGB", img.size, (255, 255, 255))
                background.paste(img, mask=img.split()[3])  # Use alpha channel as mask
                img = background
            elif img.mode not in ("RGB", "L"):
                img = img.convert("RGB")

            # Resize if needed
            if img.width > max_width:
                ratio = max_width / img.width
                new_height = int(img.height * ratio)
                img = img.resize((max_width, new_height), Image.Resampling.LANCZOS)

            # Save to bytes
            output = io.BytesIO()
            img_format = "JPEG" if img.mode == "RGB" else "PNG"
            img.save(output, format=img_format, quality=quality, optimize=True)

            ext = "jpg" if img_format == "JPEG" else "png"
            return (output.getvalue(), ext)

        except Exception as e:
            print(f"Warning: Could not optimize image: {str(e)}")
            # Return original data with guessed extension
            return (image_data, "png")

    def _get_extension_from_content_type(self, content_type: str) -> str:
        """Get file extension from MIME content type."""
        content_type_map = {
            "image/jpeg": "jpg",
            "image/jpg": "jpg",
            "image/png": "png",
            "image/gif": "gif",
            "image/webp": "webp",
            "image/svg+xml": "svg",
            "image/bmp": "bmp",
            "image/tiff": "tiff",
        }
        return content_type_map.get(content_type.lower(), "png")

    def _get_extension_from_url(self, url: str) -> str:
        """Extract file extension from URL."""
        # Remove query parameters
        url_path = url.split("?")[0]

        # Get extension
        if "." in url_path:
            ext = url_path.split(".")[-1].lower()
            if ext in ["jpg", "jpeg", "png", "gif", "webp", "svg", "bmp"]:
                return "jpg" if ext == "jpeg" else ext

        return "jpg"  # Default

    def get_all_images(self) -> dict[str, str]:
        """Get all image mappings."""
        return self.images.copy()

    def reset(self):
        """Reset the image handler state."""
        self.images = {}
        self.image_data = {}
        self.image_counter = 0
