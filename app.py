import os
import shutil
import datetime
import json
import logging
import zipfile
import tempfile
from pathlib import Path
from flask import Flask, render_template, request, jsonify, send_from_directory, send_file
from werkzeug.utils import secure_filename
import uuid

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
app.config['ORGANIZED_FOLDER'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'organized')
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB max upload size

# Create necessary directories
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['ORGANIZED_FOLDER'], exist_ok=True)

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


def organize_files(source_dir, target_dir=None, recursive=False):
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
                sub_stats = organize_files(item_path, target_dir, recursive)
                
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
        try:
            shutil.move(item_path, dest_path)
            logging.info(f"Moved: {item} to {dest_path}")
            stats['organized_files'] += 1
        except Exception as e:
            logging.error(f"Error moving {item}: {str(e)}")
            stats['skipped_files'] += 1
    
    return stats


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_files():
    if 'files[]' not in request.files:
        return jsonify({'error': 'No files part'}), 400
    
    files = request.files.getlist('files[]')
    
    if not files or files[0].filename == '':
        return jsonify({'error': 'No files selected'}), 400
    
    # Create a unique session folder for this upload
    session_id = str(uuid.uuid4())
    upload_folder = os.path.join(app.config['UPLOAD_FOLDER'], session_id)
    os.makedirs(upload_folder, exist_ok=True)
    
    # Save uploaded files
    for file in files:
        if file:
            filename = secure_filename(file.filename)
            file_path = os.path.join(upload_folder, filename)
            file.save(file_path)
    
    return jsonify({
        'success': True,
        'session_id': session_id,
        'message': f'Successfully uploaded {len(files)} files',
        'next': '/organize/' + session_id
    })


@app.route('/organize/<session_id>', methods=['GET'])
def organize_page(session_id):
    upload_folder = os.path.join(app.config['UPLOAD_FOLDER'], session_id)
    
    if not os.path.exists(upload_folder):
        return render_template('error.html', error='Session not found'), 404
    
    files = os.listdir(upload_folder)
    file_info = []
    
    for file in files:
        file_path = os.path.join(upload_folder, file)
        if os.path.isfile(file_path):
            category = get_category(file_path)
            size = os.path.getsize(file_path)
            file_info.append({
                'name': file,
                'category': category,
                'size': size
            })
    
    return render_template('organize.html', 
                           session_id=session_id, 
                           files=file_info, 
                           get_file_icon=get_file_icon,
                           get_category_icon=get_category_icon,
                           get_category_color=get_category_color,
                           format_size=format_size)


@app.route('/api/organize/<session_id>', methods=['POST'])
def organize_files_api(session_id):
    upload_folder = os.path.join(app.config['UPLOAD_FOLDER'], session_id)
    organized_folder = os.path.join(app.config['ORGANIZED_FOLDER'], session_id)
    
    if not os.path.exists(upload_folder):
        return jsonify({'error': 'Session not found'}), 404
    
    # Get parameters
    data = request.get_json()
    recursive = data.get('recursive', False) if data else False
    
    # Organize the files
    stats = organize_files(upload_folder, organized_folder, recursive)
    
    return jsonify({
        'success': True,
        'stats': stats,
        'download_url': f'/download/{session_id}'
    })


@app.route('/download/<session_id>', methods=['GET'])
def download_page(session_id):
    organized_folder = os.path.join(app.config['ORGANIZED_FOLDER'], session_id)
    
    if not os.path.exists(organized_folder):
        return render_template('error.html', error='Organized files not found'), 404
    
    # Get folder structure
    structure = {}
    for category in os.listdir(organized_folder):
        category_path = os.path.join(organized_folder, category)
        if os.path.isdir(category_path):
            structure[category] = []
            for file in os.listdir(category_path):
                file_path = os.path.join(category_path, file)
                if os.path.isfile(file_path):
                    structure[category].append({
                        'name': file,
                        'size': os.path.getsize(file_path)
                    })
    
    return render_template('download.html', 
                           session_id=session_id, 
                           structure=structure,
                           get_file_icon=get_file_icon,
                           get_category_icon=get_category_icon,
                           get_category_color=get_category_color,
                           format_size=format_size)


# Helper functions for templates
def get_file_icon(filename):
    """Get Bootstrap icon class for a file based on its extension."""
    ext = filename.split('.')[-1].lower() if '.' in filename else ''
    
    icon_map = {
        # Documents
        'pdf': 'bi bi-file-earmark-pdf',
        'doc': 'bi bi-file-earmark-word',
        'docx': 'bi bi-file-earmark-word',
        'txt': 'bi bi-file-earmark-text',
        'rtf': 'bi bi-file-earmark-text',
        'xls': 'bi bi-file-earmark-excel',
        'xlsx': 'bi bi-file-earmark-excel',
        'ppt': 'bi bi-file-earmark-slides',
        'pptx': 'bi bi-file-earmark-slides',
        
        # Images
        'jpg': 'bi bi-file-earmark-image',
        'jpeg': 'bi bi-file-earmark-image',
        'png': 'bi bi-file-earmark-image',
        'gif': 'bi bi-file-earmark-image',
        'svg': 'bi bi-file-earmark-image',
        
        # Videos
        'mp4': 'bi bi-file-earmark-play',
        'mov': 'bi bi-file-earmark-play',
        'avi': 'bi bi-file-earmark-play',
        'mkv': 'bi bi-file-earmark-play',
        
        # Audio
        'mp3': 'bi bi-file-earmark-music',
        'wav': 'bi bi-file-earmark-music',
        'ogg': 'bi bi-file-earmark-music',
        
        # Archives
        'zip': 'bi bi-file-earmark-zip',
        'rar': 'bi bi-file-earmark-zip',
        '7z': 'bi bi-file-earmark-zip',
        
        # Code
        'py': 'bi bi-file-earmark-code',
        'js': 'bi bi-file-earmark-code',
        'html': 'bi bi-file-earmark-code',
        'css': 'bi bi-file-earmark-code',
        'java': 'bi bi-file-earmark-code',
        'json': 'bi bi-file-earmark-code'
    }
    
    return icon_map.get(ext, 'bi bi-file-earmark')


def get_category_icon(category):
    """Get Bootstrap icon class for a category."""
    icon_map = {
        'Documents': 'bi bi-file-earmark-text',
        'Images': 'bi bi-file-earmark-image',
        'Videos': 'bi bi-file-earmark-play',
        'Audio': 'bi bi-file-earmark-music',
        'Archives': 'bi bi-file-earmark-zip',
        'Code': 'bi bi-file-earmark-code',
        'Others': 'bi bi-file-earmark'
    }
    
    return icon_map.get(category, 'bi bi-file-earmark')


def get_category_color(category):
    """Get Bootstrap color class for a category."""
    color_map = {
        'Documents': 'primary',
        'Images': 'success',
        'Videos': 'warning',
        'Audio': 'danger',
        'Archives': 'info',
        'Code': 'purple',
        'Others': 'secondary'
    }
    
    return color_map.get(category, 'secondary')


def format_size(size_bytes):
    """Format file size in human-readable format."""
    if size_bytes == 0:
        return "0B"
    
    size_names = ("B", "KB", "MB", "GB", "TB")
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024
        i += 1
    
    return f"{size_bytes:.2f} {size_names[i]}"


@app.route('/api/files/<session_id>/<category>/<filename>', methods=['GET'])
def get_file(session_id, category, filename):
    file_path = os.path.join(app.config['ORGANIZED_FOLDER'], session_id, category, filename)
    
    if not os.path.exists(file_path):
        return jsonify({'error': 'File not found'}), 404
    
    directory = os.path.join(app.config['ORGANIZED_FOLDER'], session_id, category)
    return send_from_directory(directory, filename, as_attachment=True)


@app.route('/api/categories', methods=['GET'])
def get_categories():
    categories = list(FILE_TYPES.keys()) + ["Others"]
    return jsonify({
        'categories': categories,
        'file_types': FILE_TYPES
    })


@app.route('/api/download-all/<session_id>', methods=['GET'])
def download_all_files(session_id):
    organized_folder = os.path.join(app.config['ORGANIZED_FOLDER'], session_id)
    
    if not os.path.exists(organized_folder):
        return jsonify({'error': 'Organized files not found'}), 404
    
    # Create a temporary file to store the zip
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.zip')
    temp_file.close()
    
    # Create a zip file containing all organized files
    with zipfile.ZipFile(temp_file.name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(organized_folder):
            for file in files:
                file_path = os.path.join(root, file)
                # Calculate the relative path for the file in the zip
                rel_path = os.path.relpath(file_path, organized_folder)
                zipf.write(file_path, rel_path)
    
    return send_file(
        temp_file.name,
        mimetype='application/zip',
        as_attachment=True,
        download_name=f'organized_files_{session_id}.zip'
    )


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)