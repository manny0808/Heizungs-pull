#!/usr/bin/env python3
"""Create simple PNG icon."""

from PIL import Image, ImageDraw

# Create 192x192 transparent image
img = Image.new('RGBA', (192, 192), (255, 255, 255, 0))
draw = ImageDraw.Draw(img)

# Colors
ORANGE = (255, 107, 0, 255)
DARK_ORANGE = (255, 61, 0, 255)
YELLOW = (255, 193, 7, 255)
GRAY = (55, 71, 79, 255)
DARK_GRAY = (38, 50, 56, 255)
GREEN = (76, 175, 80, 255)

# Heizungs housing
draw.rounded_rectangle([48, 64, 144, 160], radius=16, fill=GRAY, outline=DARK_GRAY, width=3)

# Ventilation lines
for y in [72, 88, 104, 120, 136]:
    draw.line([56, y, 136, y], fill=(84, 110, 122, 255), width=2)

# Flame
flame_points = [
    (96, 32), (80, 48), (64, 64), (96, 96),
    (128, 64), (112, 48), (96, 32)
]
draw.polygon(flame_points, fill=YELLOW)

# Heat aura
for r in [24, 32, 40]:
    draw.ellipse([96-r, 64-r, 96+r, 64+r], outline=(255, 107, 0, 64), width=2)

# Status LED
draw.ellipse([168, 56, 184, 72], fill=GREEN)

# Temperature indicator
draw.rounded_rectangle([64, 168, 128, 176], radius=8, fill=ORANGE)

# Save
png_path = "custom_components/heizungs_pull/icon.png"
img.save(png_path)
print(f"✅ Created {png_path} (192x192)")