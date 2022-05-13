from flask import Blueprint, redirect, url_for,current_app
import app_utils
import Yolov5_DeepSort_Pytorch.track

turbo = None
loading_bp = Blueprint('loading', __name__,
                        template_folder='templates')


@loading_bp.route('/load/<file>', methods=['GET', 'POST'])
def loading(file):
    filepath = f"{current_app.config['UPLOAD_FOLDER']}/{file}"
    app_utils.turbo_change_page(current_app,turbo,'loading.html','content')
    Yolov5_DeepSort_Pytorch.track.start(filepath)
    return redirect(url_for('download'))