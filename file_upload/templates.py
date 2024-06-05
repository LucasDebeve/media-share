from flask import Blueprint
import os
from datetime import datetime

bp = Blueprint('templates', __name__)

types = {
    'image': ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'svg'],
    'audio': ['mp3', 'wav', 'ogg', 'flac', 'aac'],
    'video': ['mp4', 'mkv', 'avi', 'mov', 'wmv', 'flv'],
    'présentation': ['ppt', 'pptx', 'odp'],
    'ocument': ['doc', 'docx', 'odt', 'pdf', 'txt'],
    'tableur': ['xls', 'xlsx', 'ods'],
    'archive': ['zip', 'rar', '7z', 'tar', 'gz'],
    'code': ['html', 'css', 'js', 'py', 'java', 'c', 'cpp', 'cs', 'php', 'rb', 'sh'],
    'executable': ['exe', 'msi', 'deb', 'rpm', 'apk'],
    'police': ['ttf', 'otf', 'woff', 'woff2'],
}

@bp.app_template_filter("file_size")
def file_size(filename: str):
    try:
        # Get file
        file = os.path.join('uploads', filename)
        # Get file size
        size = os.path.getsize(file)
        # Convert size to human readable format
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024:
                return f"{size:.2f} {unit}"
            size /= 1024
        return f"{size:.2f} PB"
    except Exception as e:
        return 'de taille inconnue'

@bp.app_template_filter("file_date")
def file_date(filename: str):
    try:
        # Get file
        file = os.path.join('uploads', filename)
        # Get file date
        date = os.path.getmtime(file)
        # Convert date to human readable format
        date = datetime.fromtimestamp(date).strftime('%d/%m/%Y %H:%M')
        return date
    except Exception as e:
        return 'de date inconnue'

@bp.app_template_filter("file_type")
def file_type(filename: str):
    try:
        # Get file
        file = os.path.join('uploads', filename)
        # Get file type
        file_type = os.path.splitext(file)[1]
        # Get file category
        for category, extensions in types.items():
            if file_type[1:] in extensions:
                return category
        return 'd\'un autre type'
    except Exception as e:
        return 'de type inconnu'

@bp.app_context_processor
def inject_now():
    return {'now': datetime.utcnow()}