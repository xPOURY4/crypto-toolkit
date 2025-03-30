import os
import uuid
from typing import List, Optional, Union
from pathlib import Path

from fastapi import UploadFile, HTTPException, status
from PIL import Image

from app.core.config import settings


def is_valid_file_extension(filename: str, allowed_extensions: List[str]) -> bool:
    """Check if the file has an allowed extension."""
    return filename.split(".")[-1].lower() in allowed_extensions


def get_unique_filename(filename: str) -> str:
    """Generate a unique filename to prevent overwriting."""
    file_extension = filename.split(".")[-1]
    return f"{uuid.uuid4()}.{file_extension}"


def create_upload_directory(directory: str) -> None:
    """Create the upload directory if it doesn't exist."""
    os.makedirs(directory, exist_ok=True)


def save_upload_file(
    upload_file: UploadFile,
    directory: str = settings.UPLOAD_FOLDER,
    allowed_extensions: Optional[List[str]] = None,
    is_image: bool = True,
    max_size: int = settings.MAX_CONTENT_LENGTH,
) -> str:
    """
    Save an uploaded file to the specified directory.
    
    Args:
        upload_file: The uploaded file
        directory: The directory to save the file to
        allowed_extensions: List of allowed file extensions
        is_image: Whether the file is an image (will be validated)
        max_size: Maximum file size in bytes
        
    Returns:
        The path to the saved file
    """
    # Default to global settings if not specified
    if allowed_extensions is None:
        allowed_extensions = settings.ALLOWED_EXTENSIONS
    
    # Validate file extension
    if not is_valid_file_extension(upload_file.filename, allowed_extensions):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File type not allowed. Allowed types: {', '.join(allowed_extensions)}",
        )
    
    # Get file content
    content = upload_file.file.read()
    
    # Validate file size
    if len(content) > max_size:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File too large. Maximum size: {max_size // 1024 // 1024}MB",
        )
    
    # Validate image if required
    if is_image:
        try:
            Image.open(upload_file.file)
            upload_file.file.seek(0)  # Reset file position
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid image file",
            )
    
    # Create directory if it doesn't exist
    create_upload_directory(directory)
    
    # Generate unique filename
    unique_filename = get_unique_filename(upload_file.filename)
    file_path = os.path.join(directory, unique_filename)
    
    # Save file
    with open(file_path, "wb") as f:
        f.write(content)
    
    return file_path


def delete_file(file_path: str) -> bool:
    """Delete a file if it exists."""
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            return True
        return False
    except Exception:
        return False 