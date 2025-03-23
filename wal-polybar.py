#!/usr/bin/env python3
import json
import os
import argparse

# Define default paths; if you have different paths, specify
DEFAULT_PYWAL_CACHE_PATH = os.path.expanduser("~/.cache/wal/colors.json")
DEFAULT_POLYBAR_TEMPLATE_PATH = os.path.expanduser("~/.config/polybar/config.ini")
DEFAULT_POLYBAR_CONFIG_PATH = os.path.expanduser("~/.config/polybar/config.ini")

def load_pywal_colors(cache_path):
    """Load colors from pywal cache."""
    try:
        with open(cache_path, 'r') as file:
            colors_data = json.load(file)
            return colors_data
    except Exception as e:
        print(f"Error loading pywal colors: {e}")
        return None

def update_polybar_config(template_path, config_path, colors_data):
    """Update polybar config with pywal colors."""
    try:
        with open(template_path, 'r') as template_file:
            config_template = template_file.read()
        
        # Replace placeholders with actual colors
        for i in range(16):
            placeholder = f"${{wal.color{i}}}"
            color_value = colors_data["colors"][f"color{i}"]
            config_template = config_template.replace(placeholder, color_value)
        
        # Handle other colors
        special_colors = {
            "background": colors_data["special"]["background"],
            "foreground": colors_data["special"]["foreground"],
            "cursor": colors_data["special"]["cursor"]
        }
        
        for special_key, special_value in special_colors.items():
            placeholder = f"${{wal.{special_key}}}"
            config_template = config_template.replace(placeholder, special_value)
        
        # Write updated
        with open(config_path, 'w') as output_file:
            output_file.write(config_template)
            
        print(f"Polybar configuration updated successfully at {config_path}")
        return True
    except Exception as e:
        print(f"Error updating polybar config: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Update polybar config with pywal colors")
    parser.add_argument("-c", "--colors", help="Path to pywal colors.json file", 
                        default=DEFAULT_PYWAL_CACHE_PATH)
    parser.add_argument("-t", "--template", help="Path to polybar config template", 
                        default=DEFAULT_POLYBAR_TEMPLATE_PATH)
    parser.add_argument("-o", "--output", help="Path for output polybar config", 
                        default=DEFAULT_POLYBAR_CONFIG_PATH)
    args = parser.parse_args()
    
    # Load colors
    colors_data = load_pywal_colors(args.colors)
    if not colors_data:
        return 1
    
    # Update config
    success = update_polybar_config(args.template, args.output, colors_data)
    if not success:
        return 1
    
    print("Polybar configuration has been updated with pywal colors!")
    return 0

if __name__ == "__main__":
    exit(main())
