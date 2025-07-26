# File Organizer - User Guide

## Introduction

The File Organizer is a Python utility that helps you keep your directories clean and organized by automatically sorting files into categories based on their file types. This guide will walk you through how to use the tool effectively.

## Getting Started

### Prerequisites

- Python 3.6 or higher installed on your computer
- Basic familiarity with command line operations

### Installation

No installation is required. Simply download the `file_organizer.py` script to your computer.

## Basic Usage

### Organizing Files in the Current Directory

1. Open a command prompt or terminal
2. Navigate to the directory containing the `file_organizer.py` script
3. Run the script without any arguments to organize the current directory:

```bash
python file_organizer.py
```

4. The script will ask for confirmation before proceeding. Type `y` and press Enter to continue.
5. The script will organize all files in the current directory into category folders.

![Before Organization](screenshots/before_organization.svg)

*Before: Files of different types mixed together in a single directory*

![After Organization](screenshots/after_organization.svg)

*After: Files neatly organized into category folders*

### Organizing Files in a Specific Directory

To organize files in a directory other than the current one:

```bash
python file_organizer.py /path/to/directory
```

Replace `/path/to/directory` with the path to the directory you want to organize.

## Advanced Usage

### Dry Run Mode

If you want to see what changes the script would make without actually moving any files, use the dry run mode:

```bash
python file_organizer.py -d
```

This will show you which files would be moved and where, without making any actual changes.

### Recursive Mode

To organize files in subdirectories as well:

```bash
python file_organizer.py -r
```

This will process all subdirectories recursively, organizing files at all levels.

### Specifying a Target Directory

If you want to organize files from one directory but place the organized folders in a different directory:

```bash
python file_organizer.py /source/directory -t /target/directory
```

## File Categories

The File Organizer sorts files into the following categories based on their extensions:

- **Documents**: PDF, Word, Excel, PowerPoint, text files, etc.
- **Images**: JPG, PNG, GIF, SVG, etc.
- **Videos**: MP4, AVI, MKV, etc.
- **Audio**: MP3, WAV, FLAC, etc.
- **Archives**: ZIP, RAR, 7Z, etc.
- **Code**: Python, JavaScript, HTML, CSS, etc.
- **Others**: Any file type not matching the above categories

## Troubleshooting

### Common Issues

1. **Permission Errors**: If you encounter permission errors, try running the script with administrator privileges or check the file permissions.

2. **Files Not Moving**: Make sure the files are not currently in use by another program.

3. **Unexpected Categorization**: If a file is categorized incorrectly, check the file extension. The script categorizes files based on their extensions, not their content.

## Customization

You can customize the file type mappings by modifying the `FILE_TYPES` dictionary in the script. Open the script in a text editor and locate the following section:

```python
FILE_TYPES = {
    'Documents': ['.pdf', '.doc', '.docx', '.txt', '.rtf', '.odt', '.xls', '.xlsx', '.ppt', '.pptx', '.csv'],
    'Images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.svg', '.webp'],
    # ... other categories
}
```

Add or remove file extensions as needed to match your specific requirements.

## Conclusion

The File Organizer is a simple yet powerful tool for keeping your directories clean and organized. By automatically sorting files into appropriate categories, it helps you maintain a structured file system and find files more easily.

If you have any questions or suggestions, please refer to the README.md file or contact the developer.