import os
import uuid
from werkzeug.utils import secure_filename

def allowed_file(filename, allowed_extensions):
    """
    Check if file extension is allowed
    
    Args:
        filename: Name of the file
        allowed_extensions: Set of allowed extensions
        
    Returns:
        True if file is allowed, False otherwise
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

def generate_file_id():
    """
    Generate unique file ID
    
    Returns:
        Unique file ID string
    """
    return str(uuid.uuid4())

def save_uploaded_file(file, upload_folder):
    """
    Save uploaded file securely
    
    Args:
        file: File object from Flask request
        upload_folder: Folder to save file in
        
    Returns:
        Tuple of (file_id, file_path)
    """
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)
    
    file_id = generate_file_id()
    filename = secure_filename(file.filename)
    ext = filename.rsplit('.', 1)[1].lower()
    new_filename = f"{file_id}.{ext}"
    file_path = os.path.join(upload_folder, new_filename)
    
    file.save(file_path)
    return file_id, file_path

def get_file_extension(filename):
    """
    Get file extension
    
    Args:
        filename: Name of the file
        
    Returns:
        File extension
    """
    return filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
