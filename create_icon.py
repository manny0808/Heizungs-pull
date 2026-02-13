#!/usr/bin/env python3
"""Create PNG icon from SVG."""

import cairosvg
import os

# Convert SVG to PNG
svg_path = "custom_components/heizungs_pull/icon.svg"
png_path = "custom_components/heizungs_pull/icon.png"

try:
    # Convert SVG to PNG (192x192)
    cairosvg.svg2png(
        url=svg_path,
        write_to=png_path,
        output_width=192,
        output_height=192
    )
    print(f"✅ Created {png_path} (192x192)")
except ImportError:
    print("⚠️  cairosvg not installed. Install with: pip install cairosvg")
    print("Creating placeholder PNG...")
    # Create simple placeholder
    from PIL import Image, ImageDraw
    img = Image.new('RGBA', (192, 192), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    
    # Draw simple icon
    draw.rectangle([48, 48, 144, 144], fill=(255, 107, 0, 255))
    draw.ellipse([72, 72, 120, 120], fill=(255, 61, 0, 255))
    
    img.save(png_path)
    print(f"✅ Created placeholder {png_path}")
except Exception as e:
    print(f"❌ Error creating icon: {e}")
    print("Please create icon.png manually (192x192)")