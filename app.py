from flask import Flask
import upload
import loading
import download

app = Flask(__name__)

# папка для сохранения загруженных файлов
UPLOAD_FOLDER = 'uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.register_blueprint(upload.upload_bp)
app.register_blueprint(loading.loading_bp)
app.register_blueprint(download.download_bp)


if __name__ == "__main__":
    app.run(debug=True)
