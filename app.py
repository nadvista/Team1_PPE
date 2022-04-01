import os
from flask import Flask, flash, request, redirect, url_for, render_template         
# объясняется ниже
from werkzeug.utils import secure_filename

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
            # После перенаправления на страницу загрузки
            # покажем сообщение пользователю 
            flash('Не могу прочитать файл')
            return redirect(request.url)
        file = request.files['file']
        # Если файл не выбран, то браузер может
        # отправить пустой файл без имени.
        if file.filename == '':
            flash('Нет выбранного файла')
            return redirect(request.url)
        filename = secure_filename(file.filename)
        print(filename)
        file.save(f"{app.config['UPLOAD_FOLDER']}/{filename}")
        return redirect(url_for('upload_file', name=filename))
    return render_template('index.html')

if __name__ == "__main__":
    app.run()