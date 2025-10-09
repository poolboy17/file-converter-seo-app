"""
Generate a custom icon for the File Converter SEO App
This script creates a simple icon file that can be used for the desktop shortcut.
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_app_icon():
    """Create a simple icon for the app"""
    
    # Create a 256x256 image with a gradient background
    size = 256
    img = Image.new('RGB', (size, size), color='white')
    draw = ImageDraw.Draw(img)
    
    # Draw gradient background (blue to purple)
    for i in range(size):
        r = int(100 + (i / size) * 100)  # 100 to 200
        g = int(50 + (i / size) * 50)    # 50 to 100
        b = int(200 + (i / size) * 55)   # 200 to 255
        draw.rectangle([(0, i), (size, i + 1)], fill=(r, g, b))
    
    # Draw rounded rectangle for document icon
    doc_left = size // 6
    doc_top = size // 8
    doc_right = size - doc_left
    doc_bottom = size - doc_top
    
    # Document shadow
    shadow_offset = 8
    draw.rounded_rectangle(
        [(doc_left + shadow_offset, doc_top + shadow_offset), 
         (doc_right + shadow_offset, doc_bottom + shadow_offset)],
        radius=20,
        fill=(0, 0, 0, 50)
    )
    
    # Document background
    draw.rounded_rectangle(
        [(doc_left, doc_top), (doc_right, doc_bottom)],
        radius=20,
        fill='white',
        outline=(70, 130, 180),
        width=4
    )
    
    # Draw document fold
    fold_size = 30
    fold_points = [
        (doc_right - fold_size, doc_top),
        (doc_right, doc_top + fold_size),
        (doc_right - fold_size, doc_top + fold_size),
        (doc_right - fold_size, doc_top)
    ]
    draw.polygon(fold_points, fill=(220, 220, 220), outline=(70, 130, 180))
    
    # Draw document lines
    line_left = doc_left + 20
    line_right = doc_right - 20
    line_spacing = 18
    start_y = doc_top + 50
    
    for i in range(6):
        y = start_y + (i * line_spacing)
        if i == 0 or i == 1:
            # Title lines - thicker
            draw.line([(line_left, y), (line_right - 40, y)], 
                     fill=(70, 130, 180), width=4)
        else:
            # Content lines
            draw.line([(line_left, y), (line_right, y)], 
                     fill=(150, 150, 150), width=2)
    
    # Draw arrow (conversion symbol)
    arrow_y = doc_bottom - 50
    arrow_left = doc_left + 40
    arrow_right = doc_right - 40
    arrow_mid = (arrow_left + arrow_right) // 2
    
    # Arrow shaft
    draw.line([(arrow_left, arrow_y), (arrow_right, arrow_y)], 
             fill=(255, 100, 100), width=6)
    
    # Arrow head
    arrow_head = [
        (arrow_right, arrow_y),
        (arrow_right - 15, arrow_y - 10),
        (arrow_right - 15, arrow_y + 10)
    ]
    draw.polygon(arrow_head, fill=(255, 100, 100))
    
    # Add text "SEO"
    try:
        # Try to use a nice font if available
        font = ImageFont.truetype("arial.ttf", 36)
    except:
        # Fall back to default font
        font = ImageFont.load_default()
    
    text = "SEO"
    # Get text bounding box
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    text_x = (size - text_width) // 2
    text_y = doc_bottom - 35
    
    # Draw text with shadow
    draw.text((text_x + 2, text_y + 2), text, fill=(0, 0, 0, 128), font=font)
    draw.text((text_x, text_y), text, fill=(255, 100, 100), font=font)
    
    # Save as ICO file (Windows icon format)
    icon_path = os.path.join(os.path.dirname(__file__), 'app_icon.ico')
    
    # Create multiple sizes for the icon
    icon_sizes = [(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)]
    images = []
    
    for icon_size in icon_sizes:
        resized = img.resize(icon_size, Image.Resampling.LANCZOS)
        images.append(resized)
    
    # Save as ICO with multiple sizes
    img.save(icon_path, format='ICO', sizes=[(s[0], s[1]) for s in icon_sizes])
    
    print(f"✅ Icon created successfully: {icon_path}")
    print(f"📁 Icon file size: {os.path.getsize(icon_path)} bytes")
    
    # Also save as PNG for preview
    png_path = os.path.join(os.path.dirname(__file__), 'app_icon.png')
    img.save(png_path, format='PNG')
    print(f"✅ Preview PNG created: {png_path}")
    
    return icon_path

if __name__ == "__main__":
    print("🎨 Creating File Converter SEO App icon...")
    print()
    
    try:
        icon_path = create_app_icon()
        print()
        print("✨ Icon generation complete!")
        print()
        print("Next steps:")
        print("1. Double-click 'Create_Desktop_Shortcut.vbs' to create your desktop shortcut")
        print("2. The shortcut will use the custom icon automatically")
        print()
    except Exception as e:
        print(f"❌ Error creating icon: {e}")
        print()
        print("The shortcut will use a default Windows icon instead.")
        print("You can still create the shortcut by running 'Create_Desktop_Shortcut.vbs'")
