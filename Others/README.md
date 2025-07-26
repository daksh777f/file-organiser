# File Organizer

A Python utility that automatically organizes files in a directory based on file types. This tool helps you keep your folders clean and organized by sorting files into appropriate categories.

## Features

- Automatically categorizes files based on their extensions
- Organizes files into predefined category folders (Documents, Images, Videos, etc.)
- Handles file name conflicts by adding timestamps
- Supports recursive organization of subdirectories
- Provides a dry-run mode to preview changes without moving files
- Generates detailed organization summary

## File Categories

The organizer sorts files into the following categories:

- **Documents**: PDF, Word, Excel, PowerPoint, text files, etc.
- **Images**: JPG, PNG, GIF, SVG, etc.
- **Videos**: MP4, AVI, MKV, etc.
- **Audio**: MP3, WAV, FLAC, etc.
- **Archives**: ZIP, RAR, 7Z, etc.
- **Code**: Python, JavaScript, HTML, CSS, etc.
- **Others**: Any file type not matching the above categories

## Installation

No installation is required. Simply download the `file_organizer.py` script to your computer.

### Requirements

- Python 3.6 or higher

## Usage

### Basic Usage

To organize files in the current directory:

```bash
python file_organizer.py
```

### Specify Source Directory

To organize files in a specific directory:

```bash
python file_organizer.py /path/to/source/directory
```

### Specify Target Directory

To organize files from one directory into another:

```bash
python file_organizer.py /path/to/source/directory -t /path/to/target/directory
```

### Recursive Mode

To organize files in subdirectories as well:

```bash
python file_organizer.py -r
```

### Dry Run Mode

To preview changes without actually moving files:

```bash
python file_organizer.py -d
```

### Full Command Options

```
python file_organizer.py [-h] [-t TARGET_DIR] [-r] [-d] [source_dir]

positional arguments:
  source_dir            Directory containing files to organize (default: current directory)

options:
  -h, --help            show this help message and exit
  -t TARGET_DIR, --target TARGET_DIR
                        Target directory where organized folders will be created (default: same as source)
  -r, --recursive       Process subdirectories recursively
  -d, --dry-run         Simulate the organization without moving files
```

## User Guide

### Step 1: Prepare Your Directory

Identify the directory you want to organize. For example, your Downloads folder might look like this:

![Before Organization](screenshots/before_organization.png)

### Step 2: Run the Script

Open a terminal or command prompt and navigate to where you saved the script. Run the script with your desired options:

```bash
python file_organizer.py /path/to/downloads -r
```

The script will ask for confirmation before proceeding:

```
Source directory: /path/to/downloads
Target directory: /path/to/downloads
Recursive mode: Enabled
Dry run mode: Disabled

This will organize files in the specified directory. Continue? (y/n): 
```

Type `y` and press Enter to continue.

### Step 3: Review the Results

After the script completes, it will display a summary of the organization:

```
==================================================
FILE ORGANIZATION SUMMARY
==================================================
Total files processed: 45
Files organized: 45
Files skipped: 0

Files by category:
  - Documents: 12 files
  - Images: 18 files
  - Videos: 5 files
  - Audio: 3 files
  - Archives: 4 files
  - Code: 2 files
  - Others: 1 files
==================================================
```

Your directory will now be organized into category folders:

![After Organization](screenshots/after_organization.png)

## Customization

You can customize the file type mappings by modifying the `FILE_TYPES` dictionary in the script. Add or remove file extensions to match your specific needs.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Inspired by the need for a simple, customizable file organization tool
- Thanks to all contributors and users for their feedback and suggestions