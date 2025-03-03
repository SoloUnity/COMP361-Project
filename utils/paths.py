import os
import sys

def resource_path(relative_path):
    try:
        # For pyinstaller
        base_path = sys._MEIPASS
    except Exception:
        # For main.py
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)

# Directories
GUI_DIR = "gui"
IMAGES_DIR = os.path.join(GUI_DIR, "images")
FONTS_DIR = os.path.join(GUI_DIR, "Inter")
TEXT_FILES_DIR = os.path.join(GUI_DIR, "text_files")
DATABASE_DIR = os.path.join("database", "sqlite")

# Fonts
REGULAR = resource_path(os.path.join(FONTS_DIR, "Inter-VariableFont_opsz,wght.ttf"))
ITALIC = resource_path(os.path.join(FONTS_DIR, "Inter-Italic-VariableFont_opsz,wght.ttf"))

# Db
DATABASE = resource_path(os.path.join(DATABASE_DIR, "mars_rover_sim.db"))

def get_image(image_name):
    return resource_path(os.path.join(IMAGES_DIR, image_name))

def get_font(font_name):
    return resource_path(os.path.join(FONTS_DIR, font_name))

def get_text_file(file_name):
    return resource_path(os.path.join(TEXT_FILES_DIR, file_name))