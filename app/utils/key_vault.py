import os
import uuid

class MockKeyVault:
    _secrets = {
        'flask-secret': os.getenv('FLASK_SECRET', 'default-flask-secret-' + str(uuid.uuid4())),
        'csrf-secret': os.getenv('CSRF_SECRET', 'default-csrf-secret-' + str(uuid.uuid4())),
        'database-password': os.getenv('DB_PASSWORD', 'mock-db-password'),
        'api-key': os.getenv('API_KEY', 'mock-api-key-12345'),
        'encryption-key': os.getenv('ENCRYPTION_KEY', 'mock-encryption-key')
    }

    @classmethod
    def get_secret(cls, secret_name):
        """Get secret with environment variable fallback"""
        return cls._secrets.get(secret_name) or os.getenv(secret_name.upper().replace('-', '_'))

    @classmethod
    def set_secret(cls, secret_name, secret_value, persistent=False):
        """Set secret with optional persistence to environment"""
        cls._secrets[secret_name] = secret_value
        if persistent:
            os.environ[secret_name.upper().replace('-', '_')] = secret_value
        return True
    
    @classmethod
    def ensure_secrets(cls):
        """Ensure critical secrets exist"""
        if not cls._secrets.get('flask-secret'):
            cls._secrets['flask-secret'] = 'fallback-flask-secret-' + str(uuid.uuid4())
        if not cls._secrets.get('csrf-secret'):
            cls._secrets['csrf-secret'] = 'fallback-csrf-secret-' + str(uuid.uuid4())