#!/usr/bin/env python3
"""
File Organizer - Automated File Organization Script

This script automatically organizes files in a specified directory by categorizing
them based on their file extensions. It creates organized folders for different
file types (documents, images, videos, audio, archives, etc.) and moves files
accordingly.

Usage:
    python file_organizer.py [directory_path]
    
If no directory is specified, it will organize files in the current directory.

Author: automation-scripts
License: MIT
"""

import os
import shutil
from pathlib import Path

# File category mappings
FILE_CATEGORIES = {
    'Documents': ['.pdf', '.doc', '.docx', '.txt', '.xlsx', '.xls', '.ppt', '.pptx', '.odt', '.ods'],
    'Images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.webp', '.ico'],
    'Videos': ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm'],
    'Audio': ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.m4a', '.wma'],
    'Archives': ['.zip', '.rar', '.7z', '.tar', '.gz', '.bz2'],
    'Code': ['.py', '.js', '.html', '.css', '.java', '.cpp', '.c', '.php', '.rb', '.go'],
    'Executables': ['.exe', '.msi', '.app', '.dmg', '.deb', '.rpm']
}

def get_category(file_extension):
    """Determine the category of a file based on its extension."""
    for category, extensions in FILE_CATEGORIES.items():
        if file_extension.lower() in extensions:
            return category
    return 'Others'

def organize_files(directory):
    """Organize files in the specified directory."""
    directory = Path(directory)
    
    if not directory.exists():
        print(f"Error: Directory '{directory}' does not exist.")
        return
    
    print(f"Organizing files in: {directory}\n")
    
    # Get all files in the directory
    files = [f for f in directory.iterdir() if f.is_file()]
    
    if not files:
        print("No files to organize.")
        return
    
    moved_count = 0
    
    for file in files:
        # Skip this script itself
        if file.name == Path(__file__).name:
            continue
        
        # Get file extension and category
        extension = file.suffix
        category = get_category(extension)
        
        # Create category folder if it doesn't exist
        category_folder = directory / category
        category_folder.mkdir(exist_ok=True)
        
        # Move file to category folder
        destination = category_folder / file.name
        
        # Handle file name conflicts
        counter = 1
        while destination.exists():
            name_without_ext = file.stem
            destination = category_folder / f"{name_without_ext}_{counter}{extension}"
            counter += 1
        
        try:
            shutil.move(str(file), str(destination))
            print(f"Moved: {file.name} -> {category}/")
            moved_count += 1
        except Exception as e:
            print(f"Error moving {file.name}: {e}")
    
    print(f"\nOrganization complete! Moved {moved_count} files.")

if __name__ == "__main__":
    import sys
    
    # Get directory from command line argument or use current directory
    if len(sys.argv) > 1:
        target_directory = sys.argv[1]
    else:
        target_directory = '.'
    
    organize_files(target_directory)
