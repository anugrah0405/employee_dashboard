import os
import uuid
from datetime import datetime
from pathlib import Path
from flask import current_app
import logging

logger = logging.getLogger(__name__)

class MockBlobStorage:
    @staticmethod
    def upload_file(file_stream, filename):
        """Simulate Azure Blob Storage upload with enhanced validation"""
        try:
            # Validate inputs
            if not file_stream or not filename:
                raise ValueError("Invalid file stream or filename")
                
            # Prepare storage directory
            blob_dir = Path(current_app.config['BLOB_STORAGE_FOLDER'])
            blob_dir.mkdir(parents=True, exist_ok=True)
            
            # Generate unique filename
            file_ext = Path(filename).suffix
            new_filename = f"{uuid.uuid4().hex}{file_ext}"
            blob_path = blob_dir / new_filename
            
            # Save file
            if hasattr(file_stream, 'save'):
                file_stream.save(str(blob_path))
            else:
                with open(blob_path, 'wb') as f:
                    file_stream.seek(0)
                    f.write(file_stream.read())
            
            logger.info(f"File saved to mock blob storage: {blob_path}")
            
            return {
                'filename': new_filename,
                'original_filename': filename,
                'upload_date': datetime.utcnow().isoformat(),
                'size': blob_path.stat().st_size,
                'url': f"/blob/{new_filename}"
            }
            
        except Exception as e:
            logger.error(f"Blob storage error: {str(e)}")
            raise

    @staticmethod
    def get_file_url(filename):
        """Generate accessible URL for the file"""
        return f"/blob/{filename}"

    @staticmethod
    def delete_file(filename):
        """Delete file with validation"""
        try:
            blob_path = Path(current_app.config['BLOB_STORAGE_FOLDER']) / filename
            if blob_path.exists():
                blob_path.unlink()
                logger.info(f"Deleted blob: {filename}")
                return True
            return False
        except Exception as e:
            logger.error(f"Delete failed: {str(e)}")
            return False