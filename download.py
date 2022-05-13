from flask import Blueprint,current_app, render_template
import shutil
import os

download = Blueprint('download', __name__,
                        template_folder='templates')

@download.route('/download/', methods=['GET', 'POST'])
def download():
    filepath = f"{current_app.config['UPLOAD_FOLDER']}/tempfile.mp4"
    ###########################################################################
    # Переносим размеченный файл 
    try:
        file_source = 'Yolov5_DeepSort_Pytorch/runs/track/weights/best_osnet_ibn_x1_0_MSMT17/'
        file_destination = 'static'
        get_files = os.listdir(file_source)    
        for g in get_files:
            shutil.move(file_source + g, file_destination)
            print(g, "Transfered by", file_destination, "And rdy for using")
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
    # # Gstreamer here :))))))))    
    ###########################################################################
    return render_template('videoplayer.html', filename='static/tempfile.mp4')