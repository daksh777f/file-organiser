/**
 * Main JavaScript for File Organizer Web App
 */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Initialize popovers
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
    
    // Add fade-in animation to main content
    const mainContent = document.querySelector('.content-wrapper');
    if (mainContent) {
        mainContent.classList.add('fade-in');
    }
    
    // Handle file type icons
    window.getFileIcon = function(filename) {
        const ext = filename.split('.').pop().toLowerCase();
        
        const iconMap = {
            // Documents
            'pdf': 'bi bi-file-earmark-pdf',
            'doc': 'bi bi-file-earmark-word',
            'docx': 'bi bi-file-earmark-word',
            'txt': 'bi bi-file-earmark-text',
            'rtf': 'bi bi-file-earmark-text',
            'xls': 'bi bi-file-earmark-excel',
            'xlsx': 'bi bi-file-earmark-excel',
            'ppt': 'bi bi-file-earmark-slides',
            'pptx': 'bi bi-file-earmark-slides',
            
            // Images
            'jpg': 'bi bi-file-earmark-image',
            'jpeg': 'bi bi-file-earmark-image',
            'png': 'bi bi-file-earmark-image',
            'gif': 'bi bi-file-earmark-image',
            'svg': 'bi bi-file-earmark-image',
            
            // Videos
            'mp4': 'bi bi-file-earmark-play',
            'mov': 'bi bi-file-earmark-play',
            'avi': 'bi bi-file-earmark-play',
            'mkv': 'bi bi-file-earmark-play',
            
            // Audio
            'mp3': 'bi bi-file-earmark-music',
            'wav': 'bi bi-file-earmark-music',
            'ogg': 'bi bi-file-earmark-music',
            
            // Archives
            'zip': 'bi bi-file-earmark-zip',
            'rar': 'bi bi-file-earmark-zip',
            '7z': 'bi bi-file-earmark-zip',
            
            // Code
            'py': 'bi bi-file-earmark-code',
            'js': 'bi bi-file-earmark-code',
            'html': 'bi bi-file-earmark-code',
            'css': 'bi bi-file-earmark-code',
            'java': 'bi bi-file-earmark-code',
            'json': 'bi bi-file-earmark-code'
        };
        
        return iconMap[ext] || 'bi bi-file-earmark';
    };
    
    // Format file size
    window.formatFileSize = function(bytes) {
        if (bytes === 0) return '0 Bytes';
        
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    };
    
    // Get category icon
    window.getCategoryIcon = function(category) {
        const iconMap = {
            'Documents': 'bi bi-file-earmark-text',
            'Images': 'bi bi-file-earmark-image',
            'Videos': 'bi bi-file-earmark-play',
            'Audio': 'bi bi-file-earmark-music',
            'Archives': 'bi bi-file-earmark-zip',
            'Code': 'bi bi-file-earmark-code',
            'Others': 'bi bi-file-earmark'
        };
        
        return iconMap[category] || 'bi bi-file-earmark';
    };
    
    // Handle back to top button
    const backToTopButton = document.getElementById('back-to-top');
    if (backToTopButton) {
        window.addEventListener('scroll', function() {
            if (window.pageYOffset > 300) {
                backToTopButton.classList.add('show');
            } else {
                backToTopButton.classList.remove('show');
            }
        });
        
        backToTopButton.addEventListener('click', function(e) {
            e.preventDefault();
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });
    }
    
    // Handle file search
    const fileSearch = document.getElementById('file-search');
    if (fileSearch) {
        fileSearch.addEventListener('input', function() {
            const searchTerm = this.value.toLowerCase();
            const fileItems = document.querySelectorAll('.file-item');
            
            fileItems.forEach(function(item) {
                const fileName = item.getAttribute('data-filename').toLowerCase();
                if (fileName.includes(searchTerm)) {
                    item.style.display = '';
                } else {
                    item.style.display = 'none';
                }
            });
        });
    }
    
    // Handle category filter
    const categoryFilters = document.querySelectorAll('.category-filter');
    if (categoryFilters.length > 0) {
        categoryFilters.forEach(function(filter) {
            filter.addEventListener('click', function(e) {
                e.preventDefault();
                
                // Remove active class from all filters
                categoryFilters.forEach(function(f) {
                    f.classList.remove('active');
                });
                
                // Add active class to clicked filter
                this.classList.add('active');
                
                const category = this.getAttribute('data-category');
                const fileItems = document.querySelectorAll('.file-item');
                
                fileItems.forEach(function(item) {
                    if (category === 'all' || item.getAttribute('data-category') === category) {
                        item.style.display = '';
                    } else {
                        item.style.display = 'none';
                    }
                });
            });
        });
    }
    
    // Handle file selection
    const fileCheckboxes = document.querySelectorAll('.file-checkbox');
    const selectAllCheckbox = document.getElementById('select-all');
    const bulkActionButton = document.getElementById('bulk-action-btn');
    
    if (fileCheckboxes.length > 0 && selectAllCheckbox && bulkActionButton) {
        // Select all checkbox
        selectAllCheckbox.addEventListener('change', function() {
            const isChecked = this.checked;
            
            fileCheckboxes.forEach(function(checkbox) {
                checkbox.checked = isChecked;
            });
            
            updateBulkActionButton();
        });
        
        // Individual checkboxes
        fileCheckboxes.forEach(function(checkbox) {
            checkbox.addEventListener('change', function() {
                updateSelectAllCheckbox();
                updateBulkActionButton();
            });
        });
        
        function updateSelectAllCheckbox() {
            const checkedCount = document.querySelectorAll('.file-checkbox:checked').length;
            selectAllCheckbox.checked = checkedCount === fileCheckboxes.length;
            selectAllCheckbox.indeterminate = checkedCount > 0 && checkedCount < fileCheckboxes.length;
        }
        
        function updateBulkActionButton() {
            const checkedCount = document.querySelectorAll('.file-checkbox:checked').length;
            
            if (checkedCount > 0) {
                bulkActionButton.disabled = false;
                bulkActionButton.textContent = `Download Selected (${checkedCount})`;
            } else {
                bulkActionButton.disabled = true;
                bulkActionButton.textContent = 'Download Selected';
            }
        }
    }
});