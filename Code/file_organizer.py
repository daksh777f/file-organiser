import os
import shutil
import datetime
import argparse
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# File type mappings
FILE_TYPES = {
    'Documents': ['.pdf', '.doc', '.docx', '.txt', '.rtf', '.odt', '.xls', '.xlsx', '.ppt', '.pptx', '.csv'],
    'Images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.svg', '.webp'],
    'Videos': ['.mp4', '.mov', '.avi', '.mkv', '.wmv', '.flv', '.webm', '.m4v', '.mpg', '.mpeg'],
    'Audio': ['.mp3', '.wav', '.ogg', '.flac', '.aac', '.wma', '.m4a'],
    'Archives': ['.zip', '.rar', '.7z', '.tar', '.gz', '.bz2'],
    'Code': ['.py', '.js', '.html', '.css', '.java', '.cpp', '.c', '.php', '.rb', '.go', '.ts', '.json', '.xml']
}


def get_category(file_path):
    """Determine the category of a file based on its extension."""
    file_ext = os.path.splitext(file_path)[1].lower()
    
    for category, extensions in FILE_TYPES.items():
        if file_ext in extensions:
            return category
    
    return "Others"


def create_category_folders(target_dir):
    """Create category folders if they don't exist."""
    # Get all categories including "Others"
    categories = list(FILE_TYPES.keys()) + ["Others"]
    
    for category in categories:
        category_path = os.path.join(target_dir, category)
        if not os.path.exists(category_path):
            os.makedirs(category_path)
            logging.info(f"Created folder: {category_path}")


def organize_files(source_dir, target_dir=None, recursive=False, dry_run=False):
    """Organize files from source directory into category folders."""
    # If target directory is not specified, use the source directory
    if target_dir is None:
        target_dir = source_dir
    
    # Create target directory if it doesn't exist
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    
    # Create category folders
    create_category_folders(target_dir)
    
    # Get all files in the source directory
    items = os.listdir(source_dir)
    
    # Track statistics
    stats = {
        'total_files': 0,
        'organized_files': 0,
        'skipped_files': 0,
        'categories': {}
    }
    
    for item in items:
        item_path = os.path.join(source_dir, item)
        
        # Skip the category folders themselves
        if os.path.isdir(item_path):
            category_folders = list(FILE_TYPES.keys()) + ["Others"]
            if item in category_folders:
                continue
            
            # Process subdirectories if recursive flag is set
            if recursive:
                logging.info(f"Processing subdirectory: {item_path}")
                sub_stats = organize_files(item_path, target_dir, recursive, dry_run)
                
                # Merge statistics
                stats['total_files'] += sub_stats['total_files']
                stats['organized_files'] += sub_stats['organized_files']
                stats['skipped_files'] += sub_stats['skipped_files']
                
                for category, count in sub_stats['categories'].items():
                    if category in stats['categories']:
                        stats['categories'][category] += count
                    else:
                        stats['categories'][category] = count
            continue
        
        stats['total_files'] += 1
        
        # Get the category for the file
        category = get_category(item_path)
        
        # Update category statistics
        if category in stats['categories']:
            stats['categories'][category] += 1
        else:
            stats['categories'][category] = 1
        
        # Create the destination path
        dest_dir = os.path.join(target_dir, category)
        dest_path = os.path.join(dest_dir, item)
        
        # Check if the file already exists in the destination
        if os.path.exists(dest_path):
            # Generate a unique filename by adding timestamp
            filename, extension = os.path.splitext(item)
            timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            new_filename = f"{filename}_{timestamp}{extension}"
            dest_path = os.path.join(dest_dir, new_filename)
        
        # Move the file
        if not dry_run:
            try:
                shutil.move(item_path, dest_path)
                logging.info(f"Moved: {item} to {dest_path}")
                stats['organized_files'] += 1
            except Exception as e:
                logging.error(f"Error moving {item}: {str(e)}")
                stats['skipped_files'] += 1
        else:
            logging.info(f"[DRY RUN] Would move: {item} to {dest_path}")
            stats['organized_files'] += 1
    
    return stats


def print_summary(stats):
    """Print a summary of the organization process."""
    print("\n" + "=" * 50)
    print("FILE ORGANIZATION SUMMARY")
    print("=" * 50)
    print(f"Total files processed: {stats['total_files']}")
    print(f"Files organized: {stats['organized_files']}")
    print(f"Files skipped: {stats['skipped_files']}")
    print("\nFiles by category:")
    
    for category, count in stats['categories'].items():
        print(f"  - {category}: {count} files")
    
    print("=" * 50)


def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Organize files into categories based on file type.")
    parser.add_argument(
        "source_dir", 
        nargs="?", 
        default=os.getcwd(),
        help="Directory containing files to organize (default: current directory)"
    )
    parser.add_argument(
        "-t", "--target", 
        dest="target_dir",
        help="Target directory where organized folders will be created (default: same as source)"
    )
    parser.add_argument(
        "-r", "--recursive", 
        action="store_true", 
        help="Process subdirectories recursively"
    )
    parser.add_argument(
        "-d", "--dry-run", 
        action="store_true", 
        help="Simulate the organization without moving files"
    )
    
    args = parser.parse_args()
    
    # Convert to absolute paths
    source_dir = os.path.abspath(args.source_dir)
    target_dir = os.path.abspath(args.target_dir) if args.target_dir else source_dir
    
    print(f"Source directory: {source_dir}")
    print(f"Target directory: {target_dir}")
    print(f"Recursive mode: {'Enabled' if args.recursive else 'Disabled'}")
    print(f"Dry run mode: {'Enabled' if args.dry_run else 'Disabled'}")
    
    # Confirm with user before proceeding
    if not args.dry_run:
        confirm = input("\nThis will organize files in the specified directory. Continue? (y/n): ")
        if confirm.lower() != 'y':
            print("Operation cancelled.")
            return
    
    # Organize the files
    stats = organize_files(source_dir, target_dir, args.recursive, args.dry_run)
    
    # Print summary
    print_summary(stats)


if __name__ == "__main__":
    main()