from flask import Blueprint, request, redirect, url_for, render_template,current_app
from werkzeug.utils import secure_filename

upload_bp = Blueprint('upload', __name__,
                        template_folder='templates')

@upload_bp.route('/', methods=['POST'])
def upload_file_POST():
    loading_flag = False
    # Сохраняет файл
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    # filename = secure_filename(file.filename)
    filename = "tempfile.mp4"
    filepath = f"{current_app.config['UPLOAD_FOLDER']}/{filename}"
    file.save(filepath)
    ###########################################################################
    return redirect(url_for('loading.loading',file=filename))

@upload_bp.route('/', methods=['GET'])
def upload_file_GET():
    return render_template('index.html')
