from flask import (
    Blueprint, 
    render_template, 
    flash,
    redirect,
    url_for,
    request,
    send_from_directory)
from werkzeug.utils import secure_filename
import os
import time

bp = Blueprint('pages', __name__)

@bp.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part', category='error')
            return redirect(request.url)
        file = request.files['file']
        # Upload file if it exists
        if file.filename == '':
            flash('No selected file', category='error')
            return redirect(request.url)
        if file:
            filename = secure_filename(file.filename)
            # Save file into uploads folder
            file.save(f'uploads/{filename}')
            flash('File uploaded successfully', category='success')
            return redirect(url_for('pages.home'))
    # Before uploading file, remove old files which are older than 3 day except file begin with 'keep_'
    for file in os.listdir('uploads'):
        if file.startswith('keep_'):
            continue
        if os.path.getmtime(f'uploads/{file}') < time.time() - (3 * 24 * 60 * 60): # 3 days
                os.remove(f'uploads/{file}') # Remove file if it is older than 3 days

    # Get the GET parameter 'filename' and display the details of the file
    filename = request.args.get('filename')
    if filename:
        file = os.path.join('uploads', filename)
        if os.path.exists(file):
            return render_template("pages/home.html", files=os.listdir('uploads'), fileDetails=filename)
        else:
            flash('File not found', category='error')
            return redirect(url_for('pages.home'))
    print("ya rien")
    return render_template("pages/home.html", files=os.listdir('uploads'))

@bp.route('/delete/<filename>', methods=['GET', 'POST'])
def delete(filename):
    # Ask user to confirm deletion
    if request.method == 'POST':
        if request.form.get('confirm') == 'yes':
            os.remove(f'uploads/{filename}')
            flash('File deleted successfully', category='success')
        else:
            flash('Deletion cancelled', category='info')
        return redirect(url_for('pages.home'))
    return render_template("pages/delete.html", filename=filename)


@bp.route('/download/<filename>')
def download(filename):
    # Download the file if it exists
    return send_from_directory('../uploads', filename, as_attachment=True)

@bp.route('/show/<filename>')
def show(filename):
    # Download the file if it exists
    return send_from_directory('../uploads', filename, as_attachment=False)