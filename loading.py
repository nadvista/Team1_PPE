from time import sleep
from flask import Blueprint, redirect, url_for,current_app
import app_utils
import Yolov5_DeepSort_Pytorch.track
import shutil
import os
from moviepy.editor import *

turbo = None
loading_bp = Blueprint('loading', __name__,
                        template_folder='templates')


@loading_bp.route('/load/<file>', methods=['GET', 'POST'])
def loading(file):
    filepath = f"{current_app.config['UPLOAD_FOLDER']}/{file}"
    app_utils.turbo_change_page(current_app,turbo,'loading.html','content')
    Yolov5_DeepSort_Pytorch.track.start(filepath)

    filepath = f"{current_app.config['UPLOAD_FOLDER']}/tempfile.mp4"

    ###########################################################################
    # И удаляем файл
    try:
        delete_folder = 'static/'
        os.unlink(f"{delete_folder}tempfile.mp4")
    except:
        print("Failed Delete tempfile.mp4")
    ###########################################################################
    # Сохраняем размеченный файл с изменённой частотой кадров в /static
    try:
        file_source = './Yolov5_DeepSort_Pytorch/runs/track/weights/best_osnet_ibn_x1_0_MSMT17/'
        file_destination = './static/'

        file = VideoFileClip(file_source + 'tempfile.mp4')
        file.write_videofile(file_destination + 'tempfile.mp4', fps=30)
        file.reader.close()

        print(f'[INFO] "tempfile.mp4" from "{file_source}" transfered by "{file_destination}" and ready for using!')
    except:
        print("[O-ops!] Output file already exists.")
    ###########################################################################
    # И удаляем папку откуда взяли файл
    try:
        delete_folder = 'Yolov5_DeepSort_Pytorch/runs/track/weights/'
        delete_folders = os.listdir(delete_folder)
        for g in delete_folders:
            print("Delete: ", g)
            shutil.rmtree(delete_folder + g)
    except:
        print("Failed Delete")
    return redirect(url_for('download.download_page'))
