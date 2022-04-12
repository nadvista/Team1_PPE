import os
from flask import Flask, flash, request, redirect, url_for, render_template         
# объясняется ниже
from werkzeug.utils import secure_filename
from yaml import load

# папка для сохранения загруженных файлов
UPLOAD_FOLDER = 'uploads/'
# расширения файлов, которые разрешено загружать
# создаем экземпляр приложения
app = Flask(__name__)
# конфигурируем
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # проверим, передается ли в запросе файл 
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        print(file)
        # Если файл не выбран, то браузер может
        # отправить пустой файл без имени.
        if file.filename == '':
            return redirect(request.url)
        
        filename = secure_filename(file.filename)
        print(filename)
        file.save(f"{app.config['UPLOAD_FOLDER']}/{filename}")
        
        return redirect('/load')
    return render_template('index.html')



@app.route('/load', methods=['GET', 'POST'])
def loading():
    return render_template('loading.html')


@app.route('/download', methods=['GET', 'POST'])
def download():
    return render_template('videoplayer.html')

    
if __name__ == "__main__":
    app.run()