from flask import Blueprint
import os
from datetime import datetime

bp = Blueprint('templates', __name__)

@bp.app_template_filter("file_size")
def file_size(filename: str):
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

@bp.app_template_filter("file_date")
def file_date(filename: str):
    # Get file
    file = os.path.join('uploads', filename)
    # Get file date
    date = os.path.getmtime(file)
    # Convert date to human readable format
    date = datetime.fromtimestamp(date).strftime('%d-%m-%Y à %H:%M')
    return date

@bp.app_context_processor
def inject_now():
    return {'now': datetime.utcnow()}