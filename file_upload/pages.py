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

settings = {
    'authorized_max_size': [
        {'value': 1024 * 1024, 'label': '1 Mo', 'sublabel': 'Parfait pour des documents ou des images de petite taille.'},
        {'value': 1024 * 1024 * 10, 'label': '10 Mo', 'sublabel': 'Idéal pour des présentations ou des fichiers audio compressés.'},
        {'value': 1024 * 1024 * 100, 'label': '100 Mo', 'sublabel': 'Convient pour des vidéos courtes ou des collections d\'images de haute qualité.'},
        {'value': 1024 * 1024 * 1024, 'label': '1 Go', 'sublabel': 'Tout juste assez pour un film en définition standard ou des logiciels de taille moyenne.'},
        {'value': 1024 * 1024 * 1024 * 2, 'label': '2 Go', 'sublabel': 'Convient pour des films en définition standard ou des collections de photos et vidéos.'},
        {'value': 1024 * 1024 * 1024 * 5, 'label': '5 Go', 'sublabel': 'Parfait pour des vidéos ou des fichiers audio de très grande taille.'},
    ],
    'max_file_size': 1024 * 1024 * 1024, # 1 GB
    'authorized_extensions': [
        "jpg", "jpeg", "png", "gif", "bmp", "svg",
        "mp3", "wav", "ogg", "flac", "aac",
        "mp4", "mkv", "avi", "mov", "wmv", "flv",
        "ppt", "pptx", "odp",
        "doc", "docx", "odt", "pdf", "txt",
        "xls", "xlsx", "ods",
        "zip", "rar", "7z", "tar", "gz",
        "html", "css", "js", "py", "java", "c", "cpp", "cs", "php", "rb", "sh",
        "exe", "msi", "deb", "rpm", "apk",
        "ttf", "otf", "woff", "woff2",
    ],
    'allowed_extensions': [
        "jpg", "jpeg", "png", "gif", "bmp", "svg",
        "mp3", "wav", "ogg", "flac", "aac",
        "mp4", "mkv", "avi", "mov", "wmv", "flv",
        "ppt", "pptx", "odp",
        "doc", "docx", "odt", "pdf", "txt",
        "xls", "xlsx", "ods",
        "zip", "rar", "7z", "tar", "gz",
        "html", "css", "js", "py", "java", "c", "cpp", "cs", "php", "rb", "sh",
        "exe", "msi", "deb", "rpm", "apk",
        "ttf", "otf", "woff", "woff2",
    ],
    'duration_days': 3,
    'keep_files': 'keep_',
}

@bp.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('Aucun fichier sélectionné', category='error')
            return redirect(request.url)
        file = request.files['file']
        # Upload file if it exists
        if file.filename == '':
            flash('Aucun fichier sélectionné', category='error')
            return redirect(request.url)
        if file and (len(settings['allowed_extensions']) == 0 or file.filename.split('.')[-1] in settings['allowed_extensions']):
            if file.content_length > settings['max_file_size']:
                flash('Fichier trop volumineux', category='error')
                return redirect(request.url)
            if request.form.get('temp') == 'on':
                filename = secure_filename(file.filename)
            else:
                filename = f"{settings['keep_files']}{secure_filename(file.filename)}"
            # Save file into uploads folder
            file.save(f'uploads/{filename}')
            flash('Fichier téléversé', category='success')
            return redirect(url_for('pages.home'))
    # Before uploading file, remove old files which are older than 3 day except file begin with 'keep_'
    for file in os.listdir('uploads'):
        if file.startswith(settings['keep_files']):
            continue
        if os.path.getmtime(f'uploads/{file}') < time.time() - (settings['duration_days'] * 24 * 60 * 60): # X days
                os.remove(f'uploads/{file}') # Remove file if it is older than X days

    # Get the GET parameter 'filename' and display the details of the file
    filename = request.args.get('filename')
    if filename:
        file = os.path.join('uploads', filename)
        if os.path.exists(file):
            return render_template("pages/home.html", files=os.listdir('uploads'), fileDetails=filename)
        else:
            flash('Fichier introuvable', category='error')
            return redirect(url_for('pages.home'))

    return render_template("pages/home.html", files=os.listdir('uploads'))

@bp.route('/delete/<filename>', methods=['GET', 'POST'])
def delete(filename):
    # Ask user to confirm deletion
    if request.method == 'POST':
        if request.form.get('confirm') == 'yes':
            os.remove(f'uploads/{filename}')
            flash('Fichier supprimé', category='success')
        else:
            flash('Suppression annulée', category='info')
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

@bp.route('/settings')
def settingsUpdate():
    return render_template("pages/settings.html", settings=settings)

@bp.route('/settings/update', methods=['POST'])
def update_settings():
    # Get the post data

    # Verify max_file_size is in list of allowed values 
    # 1Mo, 10Mo, 100Mo, 1Go, 2Go, 5Go
    if not request.form.get('max_file_size').isdigit() or int(request.form.get('max_file_size')) not in [size['value'] for size in settings['authorized_max_size']]:
        flash('Valeur de taille de fichier non autorisée : pas un nombre : ' + request.form.get('max_file_size'), category='error')
        return redirect(url_for('pages.settingsUpdate'))

    print(request.form.getlist('allowed_extensions'))

    # Verify allowed_extensions not contains empty value and all values are in authorized_extensions
    if '' in request.form.getlist('allowed_extensions') or not all([ext in settings['authorized_extensions'] for ext in request.form.getlist('allowed_extensions')]):
        flash('Valeur d\'extensions autorisées non autorisée', category='error')
        return redirect(url_for('pages.settingsUpdate'))

    # Verify duration_days is between 1 and 30
    if not request.form.get('duration_days').isdigit() or int(request.form.get('duration_days')) < 1 or int(request.form.get('duration_days')) > 30:
        flash('Valeur de durée non autorisée', category='error')
        return redirect(url_for('pages.settingsUpdate'))

    print(request.form.get('keep_files'))

    # Verify keep_files not contains empty value
    if request.form.get('keep_files') == '':
        flash('Valeur de fichiers à conserver non autorisée', category='error')
        return redirect(url_for('pages.settingsUpdate'))

    settings['max_file_size'] = int(request.form.get('max_file_size'))
    settings['allowed_extensions'] = request.form.getlist('allowed_extensions')
    settings['duration_days'] = int(request.form.get('duration_days'))
    settings['keep_files'] = request.form.get('keep_files')
    flash('Paramètres mis à jour', category='success')
    return redirect(url_for('pages.settingsUpdate'))

@bp.route('/help')
def help():
    return render_template("pages/help.html")