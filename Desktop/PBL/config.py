import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your_secret_key_here')
    MONGO_URI = os.environ.get('MONGO_URI', 'mongodb://localhost:27017/')
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
    CERTIFICATES_FOLDER = os.path.join(UPLOAD_FOLDER, 'certificates')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB max upload
