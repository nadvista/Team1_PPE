import os
from flask import Blueprint, send_file, render_template, current_app

download_bp = Blueprint('download', __name__,
                        template_folder='templates')

@download_bp.route('/download/', methods=['POST'])
def downloadPOST():
    path = os.path.join(current_app.root_path,
                        current_app.config['DOWNLOAD_FOLDER'], "tempfile.mp4")
    print(path)
    return send_file(path, as_attachment=True)

@download_bp.route('/download/', methods=['GET'])
def downloadGET():
    return render_template('videoplayer.html', filename=f"{current_app.config['DOWNLOAD_FOLDER']}/tempfile.mp4")
