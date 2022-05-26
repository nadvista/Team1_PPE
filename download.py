import os
from flask import Blueprint, send_file, render_template, current_app

download_bp = Blueprint('download', __name__,
                        template_folder='templates')

@download_bp.route('/downloadvideo/')
def download_video():
    path = os.path.join(current_app.root_path,
                        current_app.config['DOWNLOAD_FOLDER'], "tempfile.mp4")
    return send_file(path, as_attachment=True)


@download_bp.route('/downloaddb/')
def download_db():
    path = os.path.join(current_app.root_path,
                        current_app.config['DOWNLOAD_FOLDER'], "ИМЯФАЙЛА!!!")
    return send_file(path, as_attachment=True)

@download_bp.route('/download/')
def download_page():
    ###########################################################################
    # # Gstreamer here :))))))))
    ###########################################################################
    return render_template('videoplayer.html', filename=f"{current_app.config['DOWNLOAD_FOLDER']}/tempfile.mp4")
