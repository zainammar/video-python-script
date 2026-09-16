from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import random

# =====================================
# CONFIGURATION
# =====================================

WIDTH = 240
HEIGHT = 200
DPI = 72

# Folders and files
BACKGROUND_FOLDER = Path("background")
LOGO_FILE = Path("logo.png")
TEXT_FILE = Path("thub.txt")
OUTPUT_FOLDER = Path("output")

# Font settings
FONT_FILE = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_SIZE = 15

# Text color
TEXT_COLOR = (255, 255, 255)

# Logo size
LOGO_WIDTH = 55
LOGO_HEIGHT = 55

# Text position
TEXT_POSITION = "center"
# Dark Blue Overlay
OVERLAY_COLOR = (0, 35, 100, 120)
# =====================================
# CREATE OUTPUT FOLDER
# =====================================

OUTPUT_FOLDER.mkdir(exist_ok=True)

# =====================================
# LOAD BACKGROUND IMAGES
# =====================================

background_files = [
    file for file in BACKGROUND_FOLDER.iterdir()
    if file.suffix.lower() in [".jpg", ".jpeg", ".png", ".webp"]
]

if not background_files:
    raise FileNotFoundError(
        "Background folder mein koi image nahi mili!"
    )

# =====================================
# LOAD LOGO
# =====================================

if not LOGO_FILE.exists():
    raise FileNotFoundError("logo.png nahi mili!")

logo = Image.open(LOGO_FILE).convert("RGBA")
logo.thumbnail((LOGO_WIDTH, LOGO_HEIGHT))

# =====================================
# LOAD FONT
# =====================================

if not Path(FONT_FILE).exists():
    raise FileNotFoundError(
        f"Font file nahi mili: {FONT_FILE}"
    )

font = ImageFont.truetype(FONT_FILE, FONT_SIZE)

# =====================================
# READ TEXT FROM FILE
# =====================================

if not TEXT_FILE.exists():
    raise FileNotFoundError("thub.txt nahi mili!")

with open(TEXT_FILE, "r", encoding="utf-8") as file:
    names = [
        line.strip()
        for line in file
        if line.strip()
    ]

if not names:
    raise ValueError("thub.txt mein koi text nahi hai!")

# =====================================
# CREATE THUMBNAILS
# =====================================

for index, text in enumerate(names, start=1):

    # Random background
    background_path = random.choice(background_files)

    background = Image.open(background_path).convert("RGB")

    # Resize background to cover 240x200
    bg_ratio = max(
        WIDTH / background.width,
        HEIGHT / background.height
    )

    new_size = (
        int(background.width * bg_ratio),
        int(background.height * bg_ratio)
    )

    background = background.resize(
        new_size,
        Image.Resampling.LANCZOS
    )

    # Crop center
    left = (background.width - WIDTH) // 2
    top = (background.height - HEIGHT) // 2

    background = background.crop(
        (left, top, left + WIDTH, top + HEIGHT)
    )

    # Convert to RGBA
    canvas = background.convert("RGBA")

    draw = ImageDraw.Draw(canvas)

    # =================================
    # ADD LOGO
    # =================================

    logo_x = (WIDTH - logo.width) // 2
    logo_y = 15

    canvas.alpha_composite(
        logo,
        (logo_x, logo_y)
    )

    # =================================
    # ADD BOLD TEXT
    # =================================

    # Maximum text width
    max_text_width = WIDTH - 20

    # Simple text wrapping
    words = text.split()
    lines = []
    current_line = ""

    for word in words:
        test_line = (
            current_line + " " + word
        ).strip()

        bbox = draw.textbbox(
            (0, 0),
            test_line,
            font=font
        )

        if bbox[2] <= max_text_width:
            current_line = test_line
        else:
            if current_line:
                lines.append(current_line)

            current_line = word

    if current_line:
        lines.append(current_line)

    # Limit lines
    lines = lines[:3]

    # Calculate text height
    line_height = FONT_SIZE + 5
    total_height = len(lines) * line_height

    text_y = HEIGHT - total_height - 15

    # Draw text with shadow
    for line in lines:

        bbox = draw.textbbox(
            (0, 0),
            line,
            font=font
        )

        text_width = bbox[2] - bbox[0]

        text_x = (WIDTH - text_width) // 2

        # Shadow
        draw.text(
            (text_x + 2, text_y + 2),
            line,
            font=font,
            fill=(0, 0, 0, 180)
        )

        # Main text
        draw.text(
            (text_x, text_y),
            line,
            font=font,
            fill=TEXT_COLOR
        )

        text_y += line_height

    # =================================
    # SAVE IMAGE
    # =================================

    output_file = OUTPUT_FOLDER / f"thumbnail_{index}.png"

    canvas.convert("RGB").save(
        output_file,
        format="PNG",
        dpi=(DPI, DPI)
    )

    print(f"Created: {output_file}")

print("\nAll thumbnails created successfully! 🎉")