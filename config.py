import os
from pathlib import Path
import uuid
from app.utils.key_vault import MockKeyVault

BASE_DIR = Path(__file__).parent.parent

class Config:
    # Secrets from Key Vault with environment fallback
    SECRET_KEY = MockKeyVault.get_secret('flask-secret') or 'dev-secret-' + str(uuid.uuid4())
    WTF_CSRF_SECRET_KEY = MockKeyVault.get_secret('csrf-secret') or 'csrf-secret-' + str(uuid.uuid4())
    
    # Database configuration
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{BASE_DIR/'instance'/'employees.db'}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # File upload settings
    UPLOAD_FOLDER = str(BASE_DIR / 'uploads' / 'excel_files')
    BLOB_STORAGE_FOLDER = str(BASE_DIR / 'uploads' / 'blob_storage')
    ALLOWED_EXTENSIONS = {'xlsx', 'xls'}
    
    # Create required directories
    for folder in [BASE_DIR/'instance', UPLOAD_FOLDER, BLOB_STORAGE_FOLDER]:
        os.makedirs(folder, exist_ok=True)