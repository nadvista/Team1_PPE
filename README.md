Репозиторий с трекингом видео
    git clone --recurse-submodules https://github.com/mikel-brostrom/Yolov5_DeepSort_Pytorch.git
Установить все зависимости из репозитория
    pip install -qr requirements.txt
Разрезать видео на кадры
    ffmpeg -ss 00:00:00 -i test.avi -t 00:00:02 -c copy out.avi
Строка для трекинга 
    python track.py --yolo_model /content/Yolov5_DeepSort_Pytorch/yolov5/weights/crowdhuman_yolov5m.pt --source out.avi --save-vid
***
# ТЗ: #
* Gstreamer - встроить в проект 
* БД(PostgreSQL):
    1. счетчик объектов 
    2. время появления
    3. прочая статистика
* Flask backend
* unit test:
    1. желательно тестировать целый модуль а не функции по отдельности
* Написать документацию к проекту
* упаковать в докер