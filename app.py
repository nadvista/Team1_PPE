from json import load
from flask import Flask
import upload
import loading
import download
from turbo_flask import Turbo


app = Flask(__name__)
turbo_app = Turbo(app)
loading.turbo = turbo_app


# папка для сохранения загруженных файлов
UPLOAD_FOLDER = 'uploads/'
DOWNLOAD_FOLDER = 'static/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER
app.register_blueprint(upload.upload_bp)
app.register_blueprint(loading.loading_bp)
app.register_blueprint(download.download_bp)

if __name__ == "__main__":
    app.run(use_reloader=False, debug=True)
