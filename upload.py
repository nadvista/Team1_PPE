from flask import Blueprint, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename

upload = Blueprint('upload', __name__,
                        template_folder='templates')

@upload.route('/', methods=['POST'])
def upload_file_POST():
    loading_flag = False
    # Сохраняет файл
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    filename = secure_filename(file.filename)
    filepath = f"{app.config['UPLOAD_FOLDER']}/{filename}"
    file.save(filepath)
    ###########################################################################
    return redirect(url_for('loading',file=filename))

@upload.route('/', methods=['GET'])
def upload_file_GET():
    return render_template('index.html')