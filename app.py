from flask import Flask
import upload,loading,download

app = Flask(__name__)

# папка для сохранения загруженных файлов
UPLOAD_FOLDER = 'uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.register_blueprint(upload.upload)
app.register_blueprint(loading.loading)
app.register_blueprint(download.download)


if __name__ == "__main__":
    app.run(debug=True)
