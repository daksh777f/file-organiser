# File Organizer Web Application

## Overview

The File Organizer Web Application is a Flask-based web interface for the File Organizer tool. It allows users to upload files, organize them into categories, and download the organized files, all through an intuitive web interface.

## Features

- **File Upload**: Drag and drop or browse to select multiple files for upload
- **File Organization**: Automatically categorize files based on their types
- **Category Management**: Files are sorted into predefined categories (Documents, Images, Videos, Audio, Archives, Code, Others)
- **Download Options**: Download individual files or all organized files as a ZIP archive
- **Responsive Design**: Works on desktop and mobile devices
- **User-Friendly Interface**: Intuitive UI with progress indicators and clear instructions

## Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### Setup

1. Clone or download this repository
2. Navigate to the project directory
3. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Running the Application

### Local Development

To run the application locally:

```bash
python app.py
```

Or:

```bash
flask run --host=0.0.0.0 --port=5000
```

The application will be available at http://localhost:5000

### Deployment

For production deployment, it's recommended to use a production WSGI server like Gunicorn or uWSGI behind a reverse proxy like Nginx.

Example with Gunicorn:

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## Usage

1. **Upload Files**:
   - Drag and drop files onto the upload area or click to browse
   - Select multiple files if needed
   - Click "Upload Files" to begin the upload process

2. **Organize Files**:
   - Review the files to be organized
   - Toggle the "Process subdirectories recursively" option if needed
   - Click "Organize Files" to start the organization process

3. **Download Organized Files**:
   - View the organization summary
   - Download individual files by clicking on their names
   - Use the search and filter options to find specific files
   - Download all organized files as a ZIP archive

## Customization

### File Type Mappings

You can customize the file type mappings in the `app.py` file by modifying the `FILE_TYPES` dictionary:

```python
FILE_TYPES = {
    'Documents': ['.pdf', '.doc', '.docx', '.txt', ...],
    'Images': ['.jpg', '.jpeg', '.png', ...],
    # Add or modify categories and extensions as needed
}
```

### Styling

The application uses Bootstrap 5 for styling. You can customize the appearance by modifying the CSS in the `static/css/style.css` file.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- [Flask](https://flask.palletsprojects.com/) - The web framework used
- [Bootstrap](https://getbootstrap.com/) - For responsive design
- [Bootstrap Icons](https://icons.getbootstrap.com/) - For the icon set