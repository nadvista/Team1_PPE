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
    # И удаляем файл ( Не работает пока )
    try:
        delete_folder = 'static/'
        os.unlink(delete_folder, "tempfile.mp4")
    except:
        print("Failed Delete tempfile.mp4")
    print("ОТдыхаемм.......")
    sleep(10)
    ###########################################################################
    # Переносим размеченный файл
    try:
        file_source = 'Yolov5_DeepSort_Pytorch/runs/track/weights/best_osnet_ibn_x1_0_MSMT17/'
        file_destination = current_app.config['DOWNLOAD_FOLDER']
        get_files = os.listdir(file_source)
        for g in get_files:
            shutil.move(file_source + g, file_destination)
            print(g, "Transfered by", file_destination, "And ready for using")
    except:
        print("File already exists")
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

    ###########################################################################
    # Изменяем количесвто fps на 30
    # С помощью библиотеки moviepy
    file_path = "./static/tempfile.mp4"
    clip = VideoFileClip(file_path)
    clip.write_videofile(file_path, fps=30)
    clip.reader.close()
    ###########################################################################

    return redirect(url_for('download.download_page'))
